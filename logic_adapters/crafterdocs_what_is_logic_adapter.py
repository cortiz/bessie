from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement

from elasticsearch import Elasticsearch, RequestsHttpConnection

import nltk

import pprint


class CrafterWhatIsSearchLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(CrafterWhatIsSearchLogicAdapter, self).__init__(**kwargs)
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('maxent_ne_chunker')
        nltk.download('words')

        if kwargs.get("aws"):
            print(kwargs.get("aws"))
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
        user_input = statement.text.lower()
        words = ['what', 'is']
        if all(x in user_input.split() for x in words):
            return True
        else:
            return False

    def process(self, statement):
        tokens = nltk.word_tokenize(statement.text)
        tagged = nltk.pos_tag(tokens)
        query = ""
        for tag in tagged:
            if tag[1].startswith("NN") or tag[1].startswith("JJ"):
                query += " "+tag[0]
        print(tagged)
        res = self.es.search(index="bessie", body=
        {
            "query": {
                "bool":{
                    "must": {
                        "match" : {
                            "title" : "{}".format(query)
                        }
                    },
                    "filter": {
                        "term": {
                            "type": "def"
                        }
                    }
                }
            },
            "from" : 0, "size" : 1
        })
        if "hits" in res and res["hits"]["total"] >0:
            searchR = res["hits"]["hits"][0];

            result = {
                "answer":searchR["_source"]["content"],
                "cat":searchR["_source"]["category"],
                "id":searchR["_id"]
            }
            response_statement = Statement('{}<br/><br/>more info at https://docs.craftercms.org/en/3.0/{}'
                                           .format(result.get("answer"),result.get("id").replace(".xml",".html")))
            response_statement.confidence = 1
        else:
            response_statement = Statement("I don't now yet")
            response_statement.confidence = 0
        return response_statement
