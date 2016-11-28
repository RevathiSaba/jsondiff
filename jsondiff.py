#!/usr/bin/python


'''
Script to compare two json files

Args: 
    file1 (string): path to file1
    file2 (string): path to file2 

'''

# Imports

import argparse
import pprint
import sys
import time
import pwd
import grp
import os
import re
import json
import pprint
import site
site.addsitedir('/usr/bin/python')



g_output_dict1_missing_keys = []
g_output_dict2_missing_keys = []
g_output_non_matching_keys =[]


def get_matching_keys(a_dict1, a_dict2):
	l_keys1 = a_dict1.keys()
	l_keys2 = a_dict2.keys()
	l_matching_keys = list(set(l_keys1).intersection(set(l_keys2)))

	l_dict2_missing_keys = (list(set(l_keys1)-set(l_matching_keys)))
	l_dict1_missing_keys = (list(set(l_keys2)-set(l_matching_keys)))

	if l_dict1_missing_keys is not None:
		g_output_dict1_missing_keys.append(l_dict1_missing_keys)

	if l_dict2_missing_keys is not None:
    g_output_dict2_missing_keys.append(l_dict2_missing_keys)

	return l_matching_keys



def compare_dicts(l_dict1, l_dict2):
	if l_dict1 == l_dict2:
		return
	else:
		if l_dict1.keys() == l_dict2.keys():
			l_keys = l_dict1.keys()
		else:
			l_keys = get_matching_keys(l_dict1, l_dict2)
		for l_key in l_keys:
			if type(l_dict1[l_key]) == type(dict()) and type(l_dict2[l_key]) == type(dict()):
				compare_dicts(l_dict1[l_key],l_dict2[l_key])
			else:
				if l_dict1[l_key] != l_dict2[l_key]:
				    g_output_non_matching_keys.append({'key': l_key,
				    	                           'dict1_value':l_dict1[l_key],
				    	                           'dict2_value':l_dict2[l_key]
				    	                             })


def print_output():
	if g_output_dict1_missing_keys:
		print "Keys missing in dict1 %s:" %g_output_dict1_missing_keys
	if g_output_dict2_missing_keys:
		print "Keys missing in dict2 %s:" %g_output_dict2_missing_keys
	if g_output_non_matching_keys:
		pp = pprint.PrettyPrinter(indent=4)
		print "Non matching keys:" 
		pp.pprint(g_output_non_matching_keys)


def load_data(l_path1, l_path2):

	if not os.path.exists(l_path1):
		print "not a valid path for file1: %s" %(l_path1)
		return

	if not os.path.exists(l_path2):
		print "not a valid path for file2: %s" %(l_path2)
		return

	with open(l_path1, 'r') as output_file:
		l_dict1 = json.load(output_file)

	with open(l_path2, 'r') as output_file:
		l_dict2 = json.load(output_file)

	compare_dicts(l_dict1, l_dict2)
	print_output()




def main(argv):

    arg_parser = argparse.ArgumentParser(
                description='Compare two json files',
                usage= '%(prog)s',
                epilog= '')


    # Template file
    arg_parser.add_argument('-f1',
                            '--file1',
                            dest='file1',
                            help='absolute path to file1',
                            required=True)

    # base64 encoded json
    arg_parser.add_argument('-f2',
                            '--file2',
                            dest='file2',
                            help='absolute path to file2',
                            required=True)


    args = arg_parser.parse_args()

    load_data(args.file1, args.file2)
    #compare_dicts(g_dict1, g_dict2)
    #print_output()

if __name__ == "__main__":
    main(sys.argv[1:])