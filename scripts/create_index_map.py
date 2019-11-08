"""
	Input Format: 
		json.dumps
	Output Format:
"""

import argparse
import json

def get_args():
	parser = argparse.ArgumentParser(description='Build Index Map')
	parser.add_argument('--input-path', type=str, help='json dump file as input')
	parser.add_argument('--entity2text-path', type=str, help='path to store entity-text mapping')
	parser.add_argument('--entity2doc-path', type=str, help='path to store entity-docid mapping')

	return parser.parse_args()

def main():
	args = get_args()
	entity_text_map = {} # key:entity, value: a list of corresponding text(s)
	entity_doc_map = {} # key:entity, value: a list of document ids that the entity occurs in 


	with open(args.input_path, "r", encoding = "utf-8") as input_file:
		for line in input_file.readlines():
			json_object = json.loads(line)
			for doc_id in json_object:
				for entity, text in json_object[doc_id]:
					"""
						update entity_text_map
					"""
					if entity not in entity_text_map:
						entity_text_map[entity] = [text]
					elif text not in entity_text_map[entity]:
							entity_text_map[entity].append(text)
					"""
						update entity_doc_map
					"""
					if entity not in entity_doc_map:
						entity_doc_map[entity] = [doc_id]
					else:
						entity_doc_map[entity].append(doc_id)
	with open(args.entity2text_path, "w", encoding = "utf-8") as output_file:
		json.dump(entity_text_map, output_file)
	with open(args.entity2doc_path, "w", encoding = "utf-8") as output_file:
		json.dump(entity_doc_map, output_file)


if __name__ == '__main__':
	
	main()

