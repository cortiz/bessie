from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

from elasticsearch import Elasticsearch, RequestsHttpConnection

import nltk

import pprint
class CrafterDocsSearchLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(CrafterDocsSearchLogicAdapter, self).__init__(**kwargs)
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')
        if kwargs.get("aws"):
            self.es = Elasticsearch(
                hosts=[{'host': kwargs.get("aws"), 'port': 443}],
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection
            )
        else:
            self.es = Elasticsearch()

        self.pp = pprint.PrettyPrinter(indent=4)

    def can_process(self, statement):
        return True

    def process(self, statement):
        tokens = nltk.word_tokenize(statement.text)
        tagged = nltk.pos_tag(tokens)
        print(tagged)
        query = ""
        for tag in tagged:
            if tag[1].startswith("V"):
                query += " "+tag[0]
            elif tag[1].startswith("NN"):
                query += " "+tag[0]
            elif tag[1].startswith("DT"):
                query += " "+tag[0]
        q = {
            "query": {
                "multi_match" : {
                    "query" : query,
                    "fields" : [ "title^2", "content" ]
                }
            },"from" : 0, "size" : 1
        }
        print("Will search for {}".format(q))
        res = self.es.search(index="bessie", body=q)
        if "hits" in res and res["hits"]["total"] >0:
            searchR = res["hits"]["hits"][0];
            result = {
                "answer":searchR["_source"]["content"],
                "cat":searchR["_source"]["category"],
                "id":searchR["_id"]
            }
            response_statement = Statement('{}<br/><br/> more info <br/></br> https://docs.craftercms.org/en/3.0/{}'
                                           .format(result.get("answer"),result.get("id").replace(".xml",".html")))
            response_statement.confidence = 1
        else:
            print("Dont Know ?")
            response_statement = Statement("I don't now yet")
            response_statement.confidence = 0.5
        return response_statement

