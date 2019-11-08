# OpenQA
# Map titles of squad articles to wikipedia dump.

import os
import json


def main():
    base_dir = "/projects/tir2/users/kfusion/"
    squad_file = "train-v2.0.json"
    num_docs = 0
    num_title_matches = 0

    with open(os.path.join(base_dir, "data/squad", squad_file)) as f:
        obj = json.load(f)
        for document in obj['data']:
            num_docs += 1
            doc_title = document['title'].replace(" ", "_space_").replace(".", "_dot_").replace("/", "_slash_") + ".xml"
            if os.path.exists(os.path.join(base_dir, "data/articles", doc_title)):
                num_title_matches += 1
    print("Num docs: {}, Num matches: {}, Titles not found: {}, percentage found: {:.2f}".format(num_docs, num_title_matches, num_docs-num_title_matches, num_title_matches/num_docs)) 
            

if __name__ == "__main__":
    main()
