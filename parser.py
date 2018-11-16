import os
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch, RequestsHttpConnection
from lxml import etree
from sys import argv

def projects(root_location, es):

    for root, dirs, files in os.walk("{}/developers/projects/"):
        for x in files:
            if x.split(".")[-1] == "xml":
                abs_path = os.path.abspath(os.path.join(root, x))
                if not "api" in abs_path:
                    xmlDoc = etree.parse(abs_path)
                    xml_doc_root = xmlDoc.getroot()
                    subsections = xml_doc_root.xpath("//document/section")
                    cat = os.path.dirname(abs_path).replace("/home/cortiz/dev/cortiz/cdcb/docs/build/xml/", "")
                    print("Indexing {}/{}".format(cat, x))
                    for subsection in subsections:
                        title = subsection.xpath("title/text()")
                        content = BeautifulSoup(etree.tostring(subsection),features="lxml").get_text() \
                            .replace("\n\n\n\n\n","\n\n\n") .replace("\n\n\n\n\n\n","\n\n\n")
                        to_index = {
                            "title":title,
                            "content":content,
                            "category":cat,
                            "type":"def"
                        }
                        es.index(index="bessie", doc_type='doc', id="{}/{}".format(cat,x), body=to_index)


def main(root_location, es):
    folders = ["content-authors/","developers/","getting-started/","site-administrators/","system-administrators/"]
    for folder in folders:
        for root, dirs, files in os.walk("{}/{}".format(root_location,folder)):
            for x in files:
                if x.split(".")[-1] == "xml":
                    abs_path = os.path.abspath(os.path.join(root, x))
                    if not "api" in abs_path and x not in ["index.xml","list-form-controls.xml"]:
                        xmlDoc = etree.parse(abs_path)
                        xml_doc_root = xmlDoc.getroot()
                        subsections = xml_doc_root.xpath("//document/section/section")
                        cat = os.path.dirname(abs_path).replace("/home/cortiz/dev/cortiz/cdcb/docs/build/xml/", "")
                        print("Indexing {}/{}".format(cat, x))
                        for subsection in subsections:
                            title = subsection.xpath("title/text()")
                            content = BeautifulSoup(etree.tostring(subsection),features="lxml").get_text()\
                                .replace("\n\n\n\n\n","\n\n\n") .replace("\n\n\n\nho\n\n","\n\n\n")
                            to_index = {
                                "title":title,
                                "content":content,
                                "category":cat,
                                "type":"doc"
                            }
                            es.index(index="bessie", doc_type='doc', id="{}/{}".format(cat,x), body=to_index)


if __name__ == '__main__':
    if len(argv)>1:
        if len(argv)>2:
            es = Elasticsearch(
                hosts=[{'host': argv[2], 'port': 443}],
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection
            )
        else:
            es = Elasticsearch()

        root_location = argv[1]
        projects(root_location,es)
        main(root_location,es)
    else:
        print("Location of documents needed")
