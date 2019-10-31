# Course: CS2302 Data Structures
# Date of Last Modification: October 31, 2019
# Assignment: Lab 5 - Hash Tables
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# This program is a helper method for Lab5.  In order to test the different
# hash functions, smaller glove.6B.50d.txt files were needed.  This program
# makes subsets of the file based on the number of words.

# Populates a list with all the words found in the word embedding file.
# Input: The path for the file contaiining the word embeddings.
# Output: A list with all the word embeddings' words.
def populate_word_list(file_path_words):
    
    # Opens the file to read it.
    word_file = open(file_path_words, "r")
    line = word_file.readline()
    
    file_name = "medium_glove.txt"
    file = open(file_name, "w+")
    
    # Adds each word to word_list as long as the word only contains letters.
    for i in range(50000):
        if not line.isspace():
            file.write(line)
        line = word_file.readline()
    word_file.close()
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
    populate_word_list(file_path_words)
except FileNotFoundError:
    print("The file could not be found.  Program terminating.")
except IOError:
    print("The file could not be accessed. Program terminating.")