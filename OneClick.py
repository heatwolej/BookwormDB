import MySQLdb
import re
import sys
import json
import os
txtdir = "../"

#First off: what are we using? Pull a dbname from command line input.                                                                 
#As well as the username and password. 

execfile("CreateDatabase.py")
write_metadata()

#execfile("ImportNewLibrary.py")

#Most of these commands are inside CreateNewDatabase.py
#load_word_list()
#create_unigram_book_counts()
#create_bigram_book_counts()
load_book_list()
create_memory_table_script(allVariables)
jsonify_data(allVariables)
create_API_settings(allVariables)
