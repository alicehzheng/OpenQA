# Split wiki dump xml into a separate xml for each article.
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import iterparse, ElementTree
import os   
import json
import sys
import re
from collections import defaultdict

ET.register_namespace("", "http://www.mediawiki.org/xml/export-0.10/")

ROOTDIR = "/projects/tir2/users/kfusion/"


def main():
    # count = 0
    # articles_path = os.path.join(ROOTDIR, "data/articles")
    # if not os.path.isdir(articles_path):
    #     os.mkdir(articles_path)

    doc_to_links = defaultdict(list)  # key: docid, value: list of links, links: (text, article) 
    
    wiki_xml_local_filename = "enwiki-20190601-pages-articles-multistream.xml"
    wiki_xml_absolute_filename = os.path.join(ROOTDIR, "IndexWikipedia", wiki_xml_local_filename)

    chunk_size = 4194304
    chunk_number = 0
    
    with open(wiki_xml_absolute_filename, encoding="latin-1") as dump_file:
        while True:
            chunk_number += 1

            data = dump_file.read(chunk_size)
            if len(data) == 0:
                break

            page_start = 0
            start_idx = 0
            while True:
                prev_page = page_start
                page_start = data.find("<page", start_idx)
                if page_start == -1:
                    dump_file.seek((chunk_size*chunk_number)-prev_page, 0)
                    break

                id_start = data.find("<id>", page_start) + 4  # len("<id>")
                if id_start == 3:
                    dump_file.seek((chunk_size*chunk_number)-prev_page, 0)
                    break

                id_end = data.find("</id>", id_start)
                if id_end == -1:
                    dump_file.seek((chunk_size*chunk_number)-prev_page, 0)
                    break
                id = data[id_start:id_end]

                text_start = data.find("<text", id_end)
                if text_start == -1:
                    dump_file.seek((chunk_size*chunk_number)-prev_page, 0)
                    break

                text_end = data.find("</text>", text_start)
                if text_end == -1:
                    dump_file.seek((chunk_size*chunk_number)-prev_page, 0)
                    break 

                links = re.findall("\[\[[^\[\]]+\]\]", data[text_start:text_end])
                for link in links:
                    link = link.strip("[[").strip("]]")
                    if "|" in link:
                        try:
                            link_text, link_title = link.split("|")
                        except:
                            continue
                    else:
                        link_text, link_title = link, link
                    doc_to_links[id].append((link_text, link_title))

                start_idx = id_end
            break

    with open(os.path.join(ROOTDIR, "data/doc_to_links.json"), "w") as dump_file:
        for docid, links in doc_to_links.items():
            dump_file.write(json.dumps({docid: links})+"\n")

if __name__ == "__main__":
    main()
