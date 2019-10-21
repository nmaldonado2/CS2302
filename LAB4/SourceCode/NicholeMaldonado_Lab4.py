# Course: CS2302 Data Structures
# Date of Last Modification: October 18, 2019
# Assignment: Lab 4 - Binary Search Trees and B-Trees
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to read a file containing word embeddings
#          and populate a Binary Search Tree (BST) or B-Tree with 
#          WordEmbedding objects.  A second file is then read with a pair
#          of words per line, seperated by commas.  The similarity of these
#          words are then calculated by the cosine distance between them. The
#          similarities are displayed as well as the running times for the
#           consturction of the tree and the similarity calculations.

import BTreeClass as bt
import WordEmbedding as wemb
import BSTClass as bst
import time
import numpy as np

# Reads a file with word embeddings and populates a BST with the corresponding
# WordEmbedding objects.
# Input: The file path where the word embeddings are located.
# Output: The BST created and the running time for the tree's consturction.
def file_to_bst(file_path_words):
    
    # Opens file to read from it.
    word_file = open(file_path_words, "r")
    line = word_file.readline()
    
    # The BST initially starts as None.
    T = None
    
    # For each file line read, a WordEmbedding object is created and inserted
    # into the BST T.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            
            # The line is only evaluated if a word exists at the first
            # index of the line.
            if len(line) > 0 and line[0].isalpha():
                word_embedding = wemb.WordEmbedding(line[0], line[1:])
                T = bst.BSTInsert(T, word_embedding)
        line = word_file.readline()
    end_time = time.perf_counter()
    
    word_file.close()
    
    return T, (end_time - start_time) 

# Reads a file with word embeddings and populates a B-Tree with the 
# corresponding WordEmbedding objects.
# Input: The file path where the word embeddings are located.
# Output: The B-Tree created and the running time for the tree's consturction.
def file_to_btree(file_path_words, max_items):
    
    # Opens the file to read.
    word_file = open(file_path_words, "r")
    line = word_file.readline()
    
    T = bt.BTree([], max_data = max_items)
    
    # For each file line read, a WordEmbedding object is created and inserted
    # into B-Tree T.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            if len(line) > 0 and line[0].isalpha():
                word_embedding = wemb.WordEmbedding(line[0], line[1:])
                bt.BTreeInsert(T, word_embedding)
        line = word_file.readline()
    end_time = time.perf_counter()
    
    word_file.close()
    
    return T, (end_time - start_time) 

# Calculates the similarity between two words based on their vectors. In order
# to find the similarity the dot product of the vectors is divided by the 
# magnitude of the vectors.
# Input: The vectors of the two words that will be compared.
# Output: The similarity of the two words ranging for -1 (different) to 1 
#         (the same).
def compute_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    magnitude = np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
    return dot_product / magnitude

# Prints the similarites calculated for a list of word pairs.
# Input: A list containing word pairs and their corresponding similarity.
# Output: The similarity of the two words will be displayed.
def print_similarities(list_similarities):
    for pair in list_similarities:
        print("Similarity [%s,%s] = %.4f" % (pair[0], pair[1], pair[2]))
    print()
    
def print_non_analyzed_pairs(non_analyzed_pairs):
    print("The following line was not analyzed since one or more", end = " ")
    print("embeddings could not be found or the line's format was incorrect.")
    for pair in non_analyzed_pairs:
        print(pair)
    print()
    
# Receives a pair of words and searches for the corresponding WordEmbedding
# objects in the BST. Also intiates the calculation of the words' similarity.
# Input: The BST containing WordEmbedding objects and a list containing two
#        words.
# Output: The running time for finding the similairites of the pair.
# Assume pair is a list with only two words, one at index 0 and one at index 1.
# Also assume the words only contain lower-case letters.
def find_similarity_bst(T, pair):
    
    # Similarities are not found if the tree is empty.
    if T is None:
        print("Empty tree.  The similarities were not calculated.")
        return
    
    start_time = time.perf_counter()
    
    # Finds the embeddings in the BST.
    embedding1 = bst.FindWordBST(T, pair[0])
    embedding2 = bst.FindWordBST(T, pair[1])
                
    # Computes and adds the similarity to the word_pairs
    # as long as each embedding was successfully found in the list.
    if not embedding1 is None and not embedding2 is None:
        similarity = compute_similarity(embedding1, embedding2)
        end_time = time.perf_counter()
        
        # Initiates the printing of the results.
        print_similarities([[pair[0], pair[1], similarity]])
    else:
        end_time = time.perf_counter()
        print("The pair's similiarity was not found since one or", end = " ")
        print("more words could not be found.")
    
    return end_time - start_time

# Reads a file of word pairs and searches for the corresponding WordEmbedding
# objects in the BST. Also intiates the calculation of the words' similarities.
# Input: The BST containing WordEmbedding objects and the file path containing
#        the word pairs.
# Output: The running time for finding the similairites of all the pairs.
def find_similarities_file_bst(T, file_path_pairs):
    
    # Does not find the similarities if the tree is empty.
    if T is None:
        print("Empty tree.  The similarities were not calculated.")
        return
    
    # Reads the file containing the word pairs.
    print("Reading word file to determine similarities\n")
    pairs_file = open(file_path_pairs, "r")
    line = pairs_file.readline()
    
    word_pairs = []
    
    # Will be populated if a word embedding could not be found or a line was
    # not formatted properly.
    non_analyzed_pairs = []
    
    # Reads each line and finds the corresponding embeddings in the BST.
    # The similarity between the words is then computed and added to a list.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").rstrip(" ").split(",")
            
            # Only evaluates lines with a word at the first index.
            if len(line) == 2 and line[0].isalpha() and line[1].isalpha():
                
                # Finds the embeddings in the BST.
                embedding1 = bst.FindWordBST(T, line[0].lower())
                embedding2 = bst.FindWordBST(T, line[1].lower())
                
                # Computes and adds the similarity to the word_pairs
                # as long as each embedding was successfully found in the list.
                if not embedding1 is None and not embedding2 is None:
                    word_pairs.append([line[0].lower(), line[1].lower(), 
                                       compute_similarity(embedding1, embedding2)])
                
                # If the embedding was not found, it is added to
                # non_analyzed_pairs.
                else:
                    non_analyzed_pairs.append(line)
                    
            # If the line does not have the proper format, it is added to
            # non_analyzed_pairs.
            else:
                non_analyzed_pairs.append(line)
        line = pairs_file.readline()
    end_time = time.perf_counter()
    
    pairs_file.close()
    
    # Prints the pairs that were not analyzed.
    if len(non_analyzed_pairs) > 0:
        print_non_analyzed_pairs(non_analyzed_pairs)
    
    # Initiates the printing of the word_pairs.
    print_similarities(word_pairs)
    return end_time - start_time

# Receives a pair of words and searches for the corresponding WordEmbedding
# objects in the B-Tree. Also intiates the calculation of the words' similarity.
# Input: The B-Tree containing WordEmbedding objects and a list containing two
#        words.
# Output: The running time for finding the similairites of all the pairs.
# Assume pair is a list with only two words, one at index 0 and one at index 1.
# Also assume the words only contain lower-case letters.
def find_similarity_btree(T, pair):
    
    # Similarities are not found if the tree is empty.
    if len(T.data) == 0:
        print("Empty tree.  The similarities were not calculated.")
        return
    
    start_time = time.perf_counter()
    
    # Finds the embeddings in the BST.
    embedding1 = bt.FindWordBTree(T, pair[0])
    embedding2 = bt.FindWordBTree(T, pair[1])
                
    # Computes and adds the similarity to the word_pairs
    # as long as each embedding was successfully found in the list.
    if not embedding1 is None and not embedding2 is None:
        similarity = compute_similarity(embedding1, embedding2)
        end_time = time.perf_counter()
        
        # Initiates the printing of the results.
        print_similarities([[pair[0], pair[1], similarity]])
    else:
        end_time = time.perf_counter()
        print("The pair's similiarity was not found since one or", end = " ")
        print("more words could not be found.")
    
    return end_time - start_time

# Reads a file of word pairs and searches for the corresponding WordEmbedding
# objects in the B-Tree. Also intiates the calculation of the words' 
# similarities.
# Input: The B-Tree containing WordEmbedding objects and the path for the file
#        containing the word pairs.
# Output: The running time for finding the similairites of all the pairs.
def find_similarities_file_btree(T, file_path_pairs):
    
    # Similarities are not found if the tree is empty.
    if len(T.data) == 0:
        print("Empty tree.  The similarities were not compared.")
        return
    
    # Reads the file containing the word pairs.
    print("Reading word file to determine similarities\n")
    pairs_file = open(file_path_pairs, "r")
    line = pairs_file.readline()
    
    word_pairs = []
    
    # Will be populated if a word embedding could not be found or a line was
    # not formatted properly.
    non_analyzed_pairs = []
    
    # Reads each line and finds the corresponding embeddings in the B-Tree.
    # The similarity between the words is then computed and added to a list.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(",")
            
            # Only evaluates lines with a word at the first index.
            if len(line) == 2 and line[0].isalpha() and line[1].isalpha():
                
                # Finds the embeddings in the B-Tree.
                embedding1 = bt.FindWordBTree(T, line[0].lower())
                embedding2 = bt.FindWordBTree(T, line[1].lower())
                
                # Computes and adds the similarity to the word_pairs
                # as long as each embedding was successfully found in the list.
                if not embedding1 is None and not embedding2 is None:
                    word_pairs.append([line[0].lower(), line[1].lower(), 
                                       compute_similarity(embedding1, embedding2)])
    
                # If the embedding could not be found, it is added to
                # non_analyzed pairs.
                else:
                    non_analyzed_pairs.append(line)
                    
            # If the line does not have the proper format, it is added to
            # non_analyzed pairs.
            else:
                non_analyzed_pairs.append(line)
        line = pairs_file.readline()
    end_time = time.perf_counter()
    
    pairs_file.close()
    
    # Prints the pairs that were not analyzed.
    if len(non_analyzed_pairs) > 0:
        print_non_analyzed_pairs(non_analyzed_pairs)
    
    # Initiates the printing of the word_pairs.
    print_similarities(word_pairs)
    return end_time - start_time

# Initiates the creation of a BST and prints the stats of the tree.
# Input: The file path where the word embeddings are located.
# Output: The BST stats are displayed and the built tree is returned.
def bst_setup(file_path_words):
    print("Building binary search tree\n")
    T, runtime = file_to_bst(file_path_words)
    print("Binary Search Tree stats:")
    print("Number of nodes:", bst.NumberOfNodesBST(T))
    print("Height:", bst.HeightBST(T))
    print("Running time for binary search tree construction: %.4f seconds\n" % runtime)
    return T

# Initiates the creation of the BST and the computation of the similarities
# between pairs of words.
# Input: The file path where the word embeddings are located and a list with
#        the file path for the word pairs or a pair of words.
# Output: None, other than the running time for the query processing is
#         displayed.  
# Assume pair_path_or_input will be a list of length one or 2.  If the list
# has a length of 1, then it will only contain the path for the file
# with word pairs.  If the length is two, then at each index a word is located.
# The two words create the pair to be evaluated.
def bst_analysis(file_path_words, pair_path_or_input):
    
    # Intiates the BST's construction.
    T = bst_setup(file_path_words)
    
    # Intiates the similarity analysis.
    if len(pair_path_or_input) == 1:
        perf_time = find_similarities_file_bst(T, pair_path_or_input[0])
    else:
        perf_time = find_similarity_bst(T, pair_path_or_input)
    if not perf_time is None:
        print("Running time for binary search tree query processing:", end = "")
        print(" %.4f seconds"%(perf_time))

# Initiates the creation of a B-Tree and prints the stats of the tree.
# Input: The file path where the word embeddings are located.
# Output: The B-Tree stats are displayed and the built tree is returned.
def btree_setup(file_path_words):
    max_data = int(input("Maximum number of items in node: "))
    print()
    print("Building B-tree")
    T, runtime = file_to_btree(file_path_words, max_data)
    print("B-Tree stats:")
    print("Number of nodes:", bt.NumberOfNodesBTree(T))
    print("Height:", bt.HeightBTree(T))
    print("Running time for B-Tree construction: %.4f seconds\n" % runtime)
    return T

# Initiates the creation of the B-Tree and the computation of the similarities
# between pairs of words.
# Input: The file path where the word embeddings are located and a list with
#        the file path for the word pairs or a pair of words.
# Output: None, other than the running time for the query processing is
#         displayed.    
# Assume pair_path_or_input will be a list of length one or 2.  If the list
# has a length of 1, then it will only contain the path for the file
# with word pairs.  If the length is two, then at each index a word is located.
# The two words create the pair to be evaluated.
def btree_analysis(file_path_words, pair_path_or_input):
    
    # Intiates the B-Tree's construction.
    T = btree_setup(file_path_words)
    
    # Intiates the similarity analysis.
    if len(pair_path_or_input) == 1:
        perf_time = find_similarities_file_btree(T, pair_path_or_input[0])
    else:
        perf_time = find_similarity_btree(T, pair_path_or_input)
    if not perf_time is None:
        print("Running time for B-tree query processing", end = "")
        print(" (with max_items = %d): %.4f seconds"%(T.max_data, perf_time))

# Ensures that file_path includes a .txt file at the end.
# Input: a string of the file path that will be evaluated.
# Output: Returns false if file_path does not end in .txt and returns
#         true otherwise.
def is_txt_file(file_path):
    
    # Returns false if the file_path does not have at least 5 letters since a
    # valid .txt file name can have a minimum of 5 letters.
    if len(file_path) < 5:
        print("Invalid file.")
        return False
    
    # If the length of file_path is greater than or equal to 5, then true is
    # returned only if file_path ends in ".txt".
    else:
        if file_path[-4:] == ".txt":
            return True
        else:
            print("Invalid file.")
            return False

# Retrieves the file path for the word embeddings. Then, based on the user's
# preference a file path for the pairs or an indivudal pair of words will
# be collected.
# Input: None
# Output: The first output consists of a boolean value that denotes whether
#         all file paths entered contain a .txt file and, if applicable,
#         a correct pair of words were selected by the user. The second output
#         is a string of the path for the file containing the word embeddings.
#         Lastly, the third output is a list that will contain only the path
#         for the file containing the word pairs or a list containing
#         a pair of words. The path or pair of words is selected by the user.
def pairs_from_file_or_input():
    
    # Retrieves path for the file containing the word embeddings.
    print("Enter the file path for the word embeddings.")
    file_path_words = input("File Path: ")
    print()
    
    # If the file_path_words contains a .txt file, then the user can select
    # whether they want to evaluate the pairs from a file or enter a pair to
    # evaluate.
    if is_txt_file(file_path_words):
        print("1. Read pairs from file to find similairites")
        print("2. Enter pair to find similairty")
        menu = int(input("Select 1 or 2: "))
        print()
    
        # Retrieving path for file with the pairs.
        if menu == 1:
            print("Enter the file path for the word pairs")
            pair_path_or_input = input("File Path: ")
            print()
            
            # The file path will be deemed valid if it contains a .txt file.
            if is_txt_file(pair_path_or_input):
                return True, file_path_words, [pair_path_or_input]  
            
        # Retrieving word pair to later be evaluated.
        elif menu == 2:
            word1 = input("Enter the first word: ")
            word2 = input("Enter the second word: ")
            print()
            
            # Only words with letters will be evaluated.
            if word1.isalpha() and word2.isalpha():
                return True, file_path_words, [word1.lower(), word2.lower()]
            print("One or more of your words did not solely consist of letters.")
        else:
            print("Invalid menu number")         
    print()
    return False, "", []

# Main method that allows the user to enter the file paths for the word
# embeddings and word pairs.  The user is then able to select whether they
# want to build a BST or B-BTree with WordEmbedding objects and use the
# data structure to retrieve the pairs.
# Input: None
# Output None
try:
    valid_input, file_path_words, pair_path_or_input = pairs_from_file_or_input()
    
    # If file paths are .txt files or the pairs only contain two words, then
    # the trees are built and the pairs similarites are calculated.
    if valid_input:
        
        # The user is allowed to choose a BST or B-Tree.
        print("Choose table implementation below")
        print("Type 1 for binary search tree or 2 B-tree")
        menu = int(input("Choice: "))
        print()
        
        # If the users chooses one, then the BST is built and evaluated.
        if menu == 1:
            bst_analysis(file_path_words, pair_path_or_input)
            
        # If the user chooses two, then the B-Tree is built and evaluated.
        elif menu == 2:
            btree_analysis(file_path_words, pair_path_or_input)
            
        # Otherwise the program terminates.
        else:
            print("Invalid menu selection. Program terminating.")
    else:
        print("Program terminating")
        
# Prints errors that occur during file opening or invalid user selection.
except FileNotFoundError:
    print("One or more of the files provided for the word embeddings or")
    print("the pair of words could not be found. Program terminating.")
except IOError:
    print("One of more of the files provided for the word embeddings or")
    print("the pair of words could not be accessed. Program terminating.")
except ValueError:
    print("Invalid input. Program terminating.")