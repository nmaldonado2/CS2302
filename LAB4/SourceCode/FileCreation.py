# Course: CS2302 Data Structures
# Date of Last Modification: October 12, 2019
# Assignment: Lab 4 - Binary Search Trees and B-Trees
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to read a file containing word embeddings
#          and populate a Binary Search Tree (BST) or B-Tree with 
#          WordEmbedding objects.  The similairty of the word embedding pairs
#          from a given file is then computed. The following file adds the word
#          embeddings to a list and creates files with randomly selected word
#          pairs that will be evaluated by the main program.

import random

# Populates a list with all the words found in the word embedding file.
# Input: The path for the file contaiining the word embeddings.
# Output: A list with all the word embeddings' words.
def populate_word_list(file_path_words):
    
    # Opens the file to read it.
    word_file = open(file_path_words, "r")
    line = word_file.readline()
    
    word_list = []
    
    # Adds each word to word_list as long as the word only contains letters.
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            if len(line) > 0 and line[0].isalpha():
                word_list.append(line[0])
        line = word_file.readline()
    word_file.close()
    
    return word_list

# Populates different file sizes with randomly chosen word pairs.
# Input: The list of words that will be randomly selected to be added to the
#        file.
# Output: A file of a designated size populated by pairs of random words.  Each
#         pair is sepearted by a newline and the individual words are seperated
#         by commas.
def create_txt_files(word_list):
    
    # Number of pairs added to the file.
    amount_words = [100, 500, 1000, 2000, 5000, 50000, 100000, 150000, 200000,300000]
    
    # Creates three versions for each pair size.
    for trial_num in range(0,3):
        
        # Populates file with randomly chosen pairs.
        for amount in amount_words:
            
            # Files are named by the trial number and the number of pairs.
            file_name = "Trial" + str(trial_num + 1) + "_" + str(amount) + ".txt"
            file = open(file_name, "w+")
            for i in range(0, amount):
                randIndex1 = random.randint(0, len(word_list) - 1)
                randIndex2 = random.randint(0, len(word_list) - 1)
                file_text = word_list[randIndex1] + "," + word_list[randIndex2] + "\n"
                file.write(file_text)
            file.close()

# Main function that allows users to enter the file path with the word
# embeddings to create files with randomly selected pairs.
# Input: None
# Output: None
print("Enter the file path for the word embeddings:")
file_path_words = input("File Path: ")
print()

# Initiates the population of a list with the word embeddings and the file
# creation of the word pairs.
try:
    word_list = populate_word_list(file_path_words)
    create_txt_files(word_list)
except FileNotFoundError:
    print("The file could not be found.  Program terminating.")
except IOError:
    print("The file could not be accessed. Program terminating.")