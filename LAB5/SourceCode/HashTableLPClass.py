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
#          the cosine distance between them. The following 
#          file contains the HashTableLP class and corresponding functions such
#          as insertion, search, finding the number of elements, and the max 
#          index referenced. Lastly, the hash tables are populated 
#          based on the user's selection of a hash function which are the 
#          following: (1) string length (2) ascii value of the first character
#          (3) ascii value of the first and last character (4) ascii sum
#          (5) recursive Horner's method (6) custom.

import numpy as np

# Provided by the instructor.
# Class HashTableLP
# Attributes: The size of the hash table with linear probing
# Behaviours: find, insert, number of elements, hashing functions, and the 
#             maximum index referenced.
class HashTableLP(object):
    
    # Provided by the instructor.
    # Builds a hash table of size 'size', initilizes items to -1 (which means empty)
    # Constructor
    def __init__(self,size):  
        self.item = np.zeros(size,dtype=np.object)-1
    
    # Inserts a WordEmbedding object by using the specified hashing function.
    # Input: The WordEmbedding object to be inserted and the hashing
    #        function number which will denote which hashing function to use.
    # Output: If the WordEmbedding was successfully inserted, then its position
    #         is returned.  Otherwise, -1 is returned.
    def insert(self,word_embedding, function_num):
        
        # Finds the bucket where the WordEmbedding object should be loacated.
        initial_bucket = self.h(word_embedding.word, function_num)
        pos = initial_bucket
        
        # Iterates through the hash table staring at the initial bucket until
        # an empty bucket is found or the entire table is searched.
        for i in range(len(self.item)):
            
            # Updates the bucket to the next bucket.
            if i != 0:
                pos = (i + initial_bucket) % len(self.item)
            
            # If the WordEmbedding already exists in the hash table, it is
            # not inserted.
            try:
                if self.item[pos].word == word_embedding.word:
                    return -1
            
            # If an exception is thrown, it indicates that the bucket contains
            # an integral value, so the WordEmbedding is inserted.
            except:
                self.item[pos] = word_embedding
                return pos
        return -1
    
    # Returns WordEmbedding object's emb attribute if the word_embedding is
    # found in the hash table.
    # Input: The word to be searched for, the hashing function number, and 
    #        an index_usage_hash table which will update the index where the
    #        word should reside by 1.
    # Output: If the WordEmbedding was found, then the emb attribute is
    #         returned.  Otherwise, None is returned.
    def find(self,word, function_num, index_usage_hash_table):
        
        # Finds the bucket where the word should reside.
        initial_bucket = self.h(word, function_num)
        
        # Increments the index's reference in the hash table by 1.
        if index_usage_hash_table.item[initial_bucket] < 0:
            index_usage_hash_table.item[initial_bucket] = 1
        else:
            index_usage_hash_table.item[initial_bucket] += 1
        
        pos = initial_bucket
        
        # Iterates through the buckets starting at the initial bucket until the
        # WordEmbedding is found or a -1 is reached.
        for i in range(len(self.item)):
            if i != 0:
                pos = (i + initial_bucket) % len(self.item)
            
            # Returns the emb attribute if the word is found.
            try:
                if self.item[pos].word == word:
                    return self.item[pos].emb
            
            # Stops the search if a -1 is found.
            except:
                if self.item[pos] == -1:
                    return None
        return None
         
    # 1st hash function implementation based on the word's length.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    def hash_function_str_length(self, word):
        return len(word) % len(self.item)    
    
    # 2nd hash function implementation based on the ascii value of the first
    # letter.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    # Assume word will at least have one letter.
    def hash_function_ascii_first_char(self, word):
        return ord(word[0]) % len(self.item)
    
    # 3rd hash function implementation based on the ascii value of the first
    # and last letter.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    # Assume word will at least have one letter.
    def hash_function_ascii_first_last_char(self, word):
        return (ord(word[0]) * ord(word[-1])) % len(self.item)
    
    # 4th hash function implementation based on the ascii value of the ascii
    # sum of the word.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    # Assume word will at least have one letter.
    def hash_function_ascii_sum(self, word):
        ascii_sum = 0
        for i in word:
            ascii_sum += ord(i)
        return ascii_sum % len(self.item)
    
    # 5th hash function implementation based on the recursive computation of
    # Horner's method.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    def hash_function_recursive(self, word):
        if len(word) == 0:
            return 1
        return (ord(word[0]) + 255 * self.hash_function_recursive(word[1:])) % len(self.item)
    
    # 6th hash function implementation custom made based on Horner's method
    # and the murmur hashing function.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    def hash_function_custom(self, word):
        if len(word) == 0:
            return 0
        
        summation = ord(word[0])
        for i in range(1, len(word)):
            binary_val = bin(((133 ** i) * ord(word[i])) ^ (37**i))
            binary_val = int(binary_val, 2)
            summation += binary_val
        return summation % len(self.item)
    
    # Hashing function that determines which hashing function to use based on
    # the function_num.
    # Input: The word to be hashed and the function_num which determines which
    #        hashing function to use.
    # Output: The hashing value computed by the selected hashing function.
    def h(self, word, function_num):
        if function_num == 1:
            return self.hash_function_str_length(word)
        if function_num == 2:
            return self.hash_function_ascii_first_char(word)
        if function_num == 3:
            return self.hash_function_ascii_first_last_char(word)
        if function_num == 4:
            return self.hash_function_ascii_sum(word)
        if function_num == 5:
            return self.hash_function_recursive(word)
        return self.hash_function_custom(word)

    # Caluclates the number of WordEmbedding objects in the hash table.
    # Input: None
    # Output: The number of WordEmbedding objects in the hash table.
    def num_elements(self):
        num_elements = 0
        
        # Calculates the number of WordEmbedding objects in the hash table.
        for i in self.item:
            try:
                # If the current element is an integer less than 0, then the
                # number of elements is not updataed.
                if i < 0:
                    num_elements += 0
            
            # If an exception is thrown, then the element must be a
            # WordEmbedding object.
            except:
                num_elements += 1
        return num_elements
    
    # Resturns most used index and the number of times the index was referenced.
    # Input: None
    # Ouput: The most used index and the number of times the index was
    #        referenced.
    # Note, the following function only applies to hash tables populated with
    # integral values only.
    def most_used_index(self):
        if len(self.item) == 0:
            return -1, -1
        
        index = 0
        max_used = self.item[0]
        
        # Finds the maximum number of times that an index was referenced.
        for i in range(len(self.item)):
            if self.item[i] > max_used:
                index = i
                max_used = self.item[i]
        return index, max_used      