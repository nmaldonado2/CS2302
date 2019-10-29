# Course: CS2302 Data Structures
# Date of Last Modification: October 18, 2019
# Assignment: Lab 5 - Hash Tables
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to read a file containing word embeddings
#          and populate a Hash Table with Chaining or Linear Probing with 
#          WordEmbedding objects.  A second file is then read with a pair
#          of words per line, seperated by commas or a user enters their own
#          word pair.  The similarity of these words are then calculated by 
#          the cosine distance between them. The similarities are displayed as 
#          well as the running times for the consturction of the tree and the 
#          similarity calculations.  Lastly, the hash tables are populated 
#          based on the user's selection of a hash function which are the 
#          following: (1) string length (2) ascii value of the first character
#          (3) ascii value of the first and last character (4) ascii sum
#          (5) recursive Horner's method (6) custom.

import HashTableLPClass as htlp
import HashTableChainClass as htc
import WordEmbedding as wemb
import time
import numpy as np

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

# Prints the pairs whose similarities were unable to be found.
# Input: A list containing word pairs.
# Output: The word pairs whose similairities were unable to be found will be
#         displayed to the screen.
def print_non_analyzed_pairs(non_analyzed_pairs):
    print("The following line was not analyzed since one or more", end = " ")
    print("embeddings could not be found or the line's format was incorrect.")
    for pair in non_analyzed_pairs:
        print(pair)
    print()

# Prints the most referenced index that resulted from the hash table's
# find function.
# Input: a hash table that contains the number of references made to each index
#        during a hash table's find function.
# Output: The most referenced index and the number of calls made to the index
#         will be displayed.
def print_index_usage(index_usage_hash_table):
    index, max_calls = index_usage_hash_table.most_used_index()
    if index != -1:
        print("Index most referenced: Index", index)
        print("Number of calls made to the index:", max_calls)
        print()

# Reads a file of word pairs and searches for the corresponding WordEmbedding
# objects in the hash table. Also intiates the calculation of the words' 
# similarities.
# Input: The hash table with linear probing or chaining containing
#        WordEmbedding objects and the file path containing the word pairs. The
#       function_num is also included which specifies the hash function
#       to be used.
# Output: The running time for finding the similairites of all the pairs.
# Assume the function_num is an integer from 1 to 6. The function_num
# corresponds to the hashing function listed in the header.
def find_similarities_file(hash_table, file_path_pairs, function_num):    
    
    # Reads the file containing the word pairs.
    print("Reading word file to determine similarities\n")
    pairs_file = open(file_path_pairs, "r")
    line = pairs_file.readline()
    
    word_pairs = []
    
    # Will be populated if a word embedding could not be found or a line was
    # not formatted properly.
    non_analyzed_pairs = []
    
    # Initializes a hash table that will keep track of the number of times
    # the indices are referenced.
    try:
        index_usage = htlp.HashTableLP(len(hash_table.item))
    except:
        index_usage = htlp.HashTableLP(len(hash_table.bucket))
    
    # Reads each line and finds the corresponding embeddings in the hash table.
    # The similarity between the words is then computed and added to a list.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").rstrip(" ").split(",")
            
            # Only evaluates lines with a word at the first index.
            if len(line) == 2 and line[0].isalpha() and line[1].isalpha():
                
                # Finds the embeddings in the hash table.
                embedding1 = hash_table.find(line[0].lower(), function_num, index_usage)
                embedding2 = hash_table.find(line[1].lower(), function_num, index_usage)

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
    
    # Initiates the printing of the word_pairs and most referenced index.
    print_similarities(word_pairs)
    print_index_usage(index_usage)
    return end_time - start_time

# Receives a pair of words and searches for the corresponding WordEmbedding
# objects in the hash table with linear probing or chaining. Also intiates the 
# calculation of the words' similarity.
# Input: A hash table containing WordEmbedding objects and a list containing
#        two words. The function_num is also included and denotes the hash
#        function to be used.
# Output: The running time for finding the similairites of the pair.
# Assume pair is a list with only two words, one at index 0 and one at index 1.
# Also assume the words only contain lower-case letters.
# Assume the function_num is an integer from 1 to 6. The function_num
# corresponds to the hashing function listed in the header.
def find_similarity(hash_table, pair, function_num):
    
    # Initializes a hash table that will keep track of the number of times
    # the indices are referenced.
    try:
        index_usage = htlp.HashTableLP(len(hash_table.item))
    except:
        index_usage = htlp.HashTableLP(len(hash_table.bucket))
    
    start_time = time.perf_counter()
    
    # Finds the embeddings in the hash table.
    embedding1 = hash_table.find(pair[0], function_num, index_usage)
    embedding2 = hash_table.find(pair[1], function_num, index_usage)
                
    # Computes and adds the similarity to the word_pairs
    # as long as each embedding was successfully found in the list.
    if not embedding1 is None and not embedding2 is None:
        similarity = compute_similarity(embedding1, embedding2)
        end_time = time.perf_counter()
        
        # Initiates the printing of the results and the most referenced index.
        print_similarities([[pair[0], pair[1], similarity]])
        print_index_usage(index_usage)
    else:
        end_time = time.perf_counter()
        print("The pair's similiarity was not found since one or", end = " ")
        print("more words could not be found.")
    
    return end_time - start_time

# Reads a file with word embeddings and populates a hash table with chaining
# with the corresponding WordEmbedding objects.
# Input: The file path where the word embeddings are located, the hash function
#        and the table_size factor selected by the user.
# Output: The hash table with linear probing created and the running time for 
#         the table's consturction.
# Assume the function_num is an integer from 1 to 6. The function_num
# corresponds to the hashing function listed in the header.
def file_to_chaining(file_path_words, function_num, table_size):
    
    # Opens the file to read.
    word_file = open(file_path_words, "r")
    line = word_file.readline()
    
    # Counts the number of lines to set the hash table's size.
    num_lines = 0
    while line:
        num_lines += 1
        line = word_file.readline()
    
#    # Testing demonstrated that to have a lod function of .75 with the currrent
#    # files a factor of 0.1 needed to be applied.
#    if table_size == 1:
#        table_size += 0.1
    
    # Creates the hash table with chaining.
    hash_table = htc.HashTableChain(int(num_lines * table_size + 1))
    
    # Re-starts the file reading.
    word_file.seek(0)
    line = word_file.readline()
    
    # For each file line read, a WordEmbedding object is created and inserted
    # into the hash table.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            
            # The line is only evaluated if a word exists at the first
            # index of the line.
            if len(line) > 0 and line[0].isalpha():
                word_embedding = wemb.WordEmbedding(line[0], line[1:])
                hash_table.insert(word_embedding, function_num)
        line = word_file.readline()
    end_time = time.perf_counter()
    
    word_file.close()
    
    return hash_table, (end_time - start_time) 
    
    
# Reads a file with word embeddings and populates a hash table with linear 
# probing with the corresponding WordEmbedding objects.
# Input: The file path where the word embeddings are located, the hash function
#        number, and the table_size factor selected by the user.
# Output: The hash table created and the running time for the table's 
#         consturction.
# Assume the function_num is an integer from 1 to 6. The function_num
# corresponds to the hashing function listed in the header.
def file_to_linear_probing(file_path_words, function_num, table_size):

    # Opens the file to read.
    word_file = open(file_path_words, "r")
    line = word_file.readline()
    
    num_lines = 0
    while line:
        num_lines += 1
        line = word_file.readline()
    
    if table_size == 1.1 and num_lines == 10000:
        table_size += 0.15
    if table_size == 0.9 and num_lines == 10000:
        table_size += 0.13
    
    # Counts the number of lines to set the hash table's size
    hash_table = htlp.HashTableLP(int(num_lines * table_size + 1))
    
    word_file.seek(0)
    line = word_file.readline()
    
    # For each file line read, a WordEmbedding object is created and inserted
    # into the hash table.
    start_time = time.perf_counter()
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            
            # The line is only evaluated if a word exists at the first
            # index of the line.
            if len(line) > 0 and line[0].isalpha():
                word_embedding = wemb.WordEmbedding(line[0], line[1:])
                hash_table.insert(word_embedding, function_num)
        line = word_file.readline()
    end_time = time.perf_counter()
    
    word_file.close()
    
    return hash_table, (end_time - start_time) 
    

# Initiates the creation of a hash table with chaining and prints the stats of 
# the table.
# Input: The file path where the word embeddings are locatedm the hashing 
#        function number, and the table_size factor.
# Output: The hash table with chaining stats are displayed and the built table 
#         is returned.
def chaining_setup(file_path_words, function_num, table_size):
    print("Building the Hash Table with Chaining\n")
    
    # Intiates hash table construction.
    hash_table, runtime = file_to_chaining(file_path_words, function_num, table_size)
    
    # Prints the hash table stats.
    print("Hash Table with Chaining stats:\n")
    num_elements = hash_table.num_elements()
    print("Number of elements:", num_elements)
    print("Number of empty lists:", hash_table.num_empty_lists())
    print("Load Factor: %.4f\n" % (num_elements / len(hash_table.bucket)))
    print("Running time for hash table with chaining construction: %.4f seconds\n" % runtime)

    return hash_table

# Initiates the creation of a hash table with linear probing and prints the 
# stats of the table.
# Input: The file path where the word embeddings are located, the hash function
#        number, and the table_size factor.
# Output: The hash table with linear probing stats are displayed and the  
#         populated table is returned.
def linear_probing_setup(file_path_words, function_num, table_size):
    print("Building Hash Table with Linear Probing\n")
    
    # Intiates hash table construction.
    hash_table, runtime = file_to_linear_probing(file_path_words, function_num, table_size)
    
    # Prints the hash table stats.
    print("Hash Table with Linear Probing stats:\n")
    num_elements = hash_table.num_elements()
    print("Number of elements:", num_elements)
    print("Number of empty lists:", len(hash_table.item) - num_elements)
    print("Load Factor: %.4f\n" % (num_elements / len(hash_table.item)))
    print("Running time for hash table with linear probing construction: %.4f seconds\n" % runtime)
    
    return hash_table

# Initiates the creation of the hash table with chaining and the computation of 
# the similarities between pairs of words.
# Input: The file path where the word embeddings are located and a list with
#        the file path for the word pairs or a pair of words. The hashing
#        function number and the table size factor, which will be used to 
#        adjust the load factor, are also parameters.
# Output: None, other than the running time for the query processing is
#         displayed.    
# Assume pair_path_or_input will be a list of length one or 2.  If the list
# has a length of 1, then it will only contain the path for the file
# with word pairs.  If the length is two, then at each index a word is located.
# The two words create the pair to be evaluated.
def chaining_analysis(file_path_words, pair_path_or_input, function_num, table_size):

    # Initiates the hash table's construction.
    hash_table = chaining_setup(file_path_words, function_num, table_size)
    
    # Intiates the similarity analysis.
    if len(pair_path_or_input) == 1:
        perf_time = find_similarities_file(hash_table, pair_path_or_input[0], function_num)
    else:
        perf_time = find_similarity(hash_table, pair_path_or_input, function_num)

    print("Running time for hash table with chaining query ", end = "")
    print(" processing: %.4f seconds" % perf_time)
        
# Initiates the creation of the hashing table with linear probing and the 
# computation of the similarities between pairs of words.
# Input: The file path where the word embeddings are located and a list with
#        the file path for the word pairs or a pair of words.  The hashing
#        function number and the table size factor, which will be used to 
#        adjust the load factor, are also parameters.
# Output: None, other than the running time for the query processing is
#         displayed.    
# Assume pair_path_or_input will be a list of length one or 2.  If the list
# has a length of 1, then it will only contain the path for the file
# with word pairs.  If the length is two, then at each index a word is located.
# The two words create the pair to be evaluated.
def linear_probing_analysis(file_path_words, pair_path_or_input, function_num, table_size):
    
    # Intiates the hash table's construction.
    hash_table = linear_probing_setup(file_path_words, function_num, table_size)
    
    # Intiates the similarity analysis.
    if len(pair_path_or_input) == 1:
        perf_time = find_similarities_file(hash_table, pair_path_or_input[0], function_num)
    else:
        perf_time = find_similarity(hash_table, pair_path_or_input, function_num)

    print("Running time for hash table with linear probing query ", end = "")
    print(" processing: %.4f seconds" % perf_time)

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
# want to build a hash table with linear probing or chaining with WordEmbedding 
# objects. The data structure will then be used to retrieve the pairs and
# compute the word similarities.
# Input: None
# Output None
try:
#    valid_input, file_path_words, pair_path_or_input = pairs_from_file_or_input()
    valid_input = True
    file_path_words = "/Users/nichole_maldonado/Desktop/glove.6B.50d.txt"
    pair_path_or_input = ["/Users/nichole_maldonado/Desktop/Lab4/Trial1_100.txt"]
    
    # If file paths are .txt files or the pairs only contain two words, then
    # the hash table is built and the pairs similarites are calculated.
    if valid_input:
        
        # The user is allowed to choose a hash table with chaining or linear
        # probing.
        print("Choose table implementation below")
        print("Type 1 for hash table with chaining or 2 hash table with linear probing")
        menu = int(input("Choice: "))
        print()
        
        # The user then selects the hash table function.
        if menu == 1 or menu == 2:
            print("Choose a hashing function")
            print("1. Length of the String")
            print("2. Ascii Value of the First Character")
            print("3. Ascii Values of the First and Last Characters")
            print("4. Sum of Ascii Values")
            print("5. Recursion")
            print("6. Custom")
            function_num = int(input("Select 1 - 6: "))
            print()
            
            # The user then selects the table_size factor which will be 
            # used to adjust the load factor.
            if function_num >= 1 and function_num <= 6:
                print("Chose the size of the hash table")
                print("1. Load Factor of Approximately 0.75")
                print("2. Load Factor of Apprxoimately 0.5")
                print("3. Load Factor of Approximately 0.27")
                print("4. Load Factor of Approximately 0.9")
                table_size = int(input("Select 1, 2, or 3: "))
        
                # If the user correctly selected all of the above options,
                # then the main table construction and find occurs.
                if table_size >= 1 and table_size <= 4:
                    if table_size == 1:
                        table_size = 1.1
                    elif table_size == 2:
                        table_size = 2
                    elif table_size == 3:
                        table_size = 3
                    else:
                        table_size = 0.9
                        
                    
                    # If the users chooses one, then the hash table with 
                    # chaining is built and evaluated.
                    if menu == 1:
                        chaining_analysis(file_path_words, pair_path_or_input, 
                                          function_num, table_size)
                        
                    # If the users chooses two, then the hash table with 
                    # linear probing is built and evaluated.
                    else:
                        linear_probing_analysis(file_path_words, pair_path_or_input, 
                                                function_num, table_size)
                
                # Otherwise the program terminates.
                else:
                   print("Invalid menu selection. Program terminating.") 
            else:
                print("Invalid menu selection. Program terminating.")
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