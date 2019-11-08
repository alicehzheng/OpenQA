print("Begin")

from bs4 import BeautifulSoup
import os
from lxml import etree
import json


id_to_title = {}
title_to_id = {}
root_dir = "/projects/tir2/users/kfusion"
c = 0
uh_ohs = 0

print("Starting")
for file in os.scandir(os.path.join(root_dir, "data/articles")): 
    with open(os.path.join(root_dir, "data/articles", file), encoding='utf-8') as f:
        article_soup = BeautifulSoup(f.read(), 'lxml-xml')
    id = str(article_soup.find("id")).strip("<id>").strip("</id>")
    title = str(article_soup.find("title")).strip("<title>").strip("</title>")
    del article_soup
    if id is None:
        print("uh oh", uh_ohs)
        uh_ohs += 1
        continue
    id_to_title[id] = title
    title_to_id[title] = id
    c += 1
    if c % 10000 == 0:
        print(c)
        

with open(os.path.join(root_dir, "data", "id_to_title.json"), "w") as f:
    json.dump(id_to_title, f)

with open(os.path.join(root_dir, "data", "title_to_id.json"), "w") as f:
    json.dump(title_to_id, f)
