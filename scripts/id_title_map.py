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

    chunk_size = 4194304
    chunk_number = 0
    
    with open(wiki_xml_absolute_filename, encoding="latin-1") as dump_file:
        while True:
            chunk_number += 1
            print(chunk_number)
            data = dump_file.read(chunk_size)
            if len(data) == 0:
                break

            start_idx = 0
            while True:
                title_start = data.find("<title>", start_idx) + 7  # len("<title>")
                if title_start == 6:
                    dump_file.seek((chunk_size*chunk_number)-10, 0)
                    break

                title_end = data.find("</title>", title_start)
                if title_end == -1:
                    dump_file.seek((chunk_size*chunk_number)-100, 0)
                    break

                title = data[title_start:title_end]

                id_start = data.find("<id>", title_end) + 4  # len("<id>")
                if id_start == 3:
                    dump_file.seek((chunk_size*chunk_number)-120, 0)
                    break

                id_end = data.find("</id>", id_start)
                if id_end == -1:
                    dump_file.seek((chunk_size*chunk_number)-130, 0)
                    break

                id = data[id_start:id_end]

                title_to_id[title] = id 
                id_to_title[id] = title

                # print(title, id)

                start_idx = id_end

            # break



    with open(os.path.join(ROOTDIR, "data/id_to_title.json"), "w") as dump_file:
        json.dump(id_to_title, dump_file)

    with open(os.path.join(ROOTDIR, "data/title_to_id.json"), "w") as dump_file:
        json.dump(title_to_id, dump_file)

if __name__ == "__main__":
    main()
