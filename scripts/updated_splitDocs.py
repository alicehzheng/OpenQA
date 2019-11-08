# Split wiki dump xml into a separate xml for each article.
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse, ElementTree
import os   
import json
import sys

ET.register_namespace("", "http://www.mediawiki.org/xml/export-0.10/")

ROOTDIR = "/projects/tir2/users/kfusion/"

def main():
    # tree = ElementTree()
    count = 0
    articles_path = os.path.join(ROOTDIR, "data/articles")
    if not os.path.isdir(articles_path):
        os.mkdir(articles_path)


    title_to_id = dict()
    id_to_title = dict()    
    
    wiki_xml_local_filename = "enwiki-20190601-pages-articles-multistream.xml"
    wiki_xml_absolute_filename = os.path.join(ROOTDIR, "IndexWikipedia", wiki_xml_local_filename)
    
    with open(wiki_xml_absolute_filename, encoding="latin-1") as dump_file:
        for event, elem in iterparse(dump_file, events=("start", "end")):
            if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}mediawiki':
                root = elem
            elif event == 'end':    
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                    title_elem = elem.find('{http://www.mediawiki.org/xml/export-0.10/}title').text
                    new_title = str(title_elem).replace("/", "_slash_").replace(".", "_dot_").replace(" ", "_space_")
                    id_elem = elem.find('{http://www.mediawiki.org/xml/export-0.10/}id').text
                    title_to_id[new_title] = id_elem
                    id_to_title[id_elem] = new_title

                    print(count, "      ", title_elem)
                    ET.ElementTree(elem).write(os.path.join(articles_path, id_elem + ".xml"))
                    count += 1
                root.clear()

    with open(os.path.join(ROOTDIR, "data/id_to_title.json"), "w") as dump_file:
        json.dump(id_to_title, dump_file)

    with open(os.path.join(ROOTDIR, "data/title_to_id.json"), "w") as dump_file:
        json.dump(title_to_id, dump_file)

if __name__ == "__main__":
    main()
