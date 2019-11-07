"""
	Input Format: 
		json.dumps: 

	Output Format:
"""

import argparse
import json

def get_args():
	parser = argparse.Argumentparser(description='Build Index Map')
	parser.add_argument('--input-file', type=str, help='json dump file as input')
	return parser.parse_args

def main():
	args = get_args()
	raw_dict = json.loads(open(args.input_file, "r")) # load data in the json dump into a dictionary
    


if __name__ == '__main__':
	
	main()

