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
#          file contains the HashTableChain class and corresponding functions such
#          as insertion, search, finding the number of elements, and the max 
#          index referenced. Lastly, the hash tables are populated 
#          based on the user's selection of a hash function which are the 
#          following: (1) string length (2) ascii value of the first character
#          (3) ascii value of the first and last character (4) ascii sum
#          (5) recursive Horner's method (6) custom.

# Provided by the instructor.
# Class HashTableChain
# Attributes: The size of the hash table with linear probing
# Behaviours: find, insert, number of elements, and hashing functions.
class HashTableChain(object):
    
    # Provided by the constructor.
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.bucket = [[] for i in range(size)]
    
    # 1st hash function implementation based on the word's length.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    def hash_function_str_length(self, word):
        return len(word) % len(self.bucket)    
    
    # 2nd hash function implementation based on the ascii value of the first
    # letter.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    # Assume word will at least have one letter.
    def hash_function_ascii_first_char(self, word):
        return ord(word[0]) % len(self.bucket)
    
    # 3rd hash function implementation based on the ascii value of the first
    # and last letter.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    # Assume word will at least have one letter.
    def hash_function_ascii_first_last_char(self, word):
        return (ord(word[0]) * ord(word[-1])) % len(self.bucket)
    
    # 4th hash function implementation based on the ascii value of the ascii
    # sum of the word.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    # Assume word will at least have one letter.
    def hash_function_ascii_sum(self, word):
        ascii_sum = 0
        for i in word:
            ascii_sum += ord(i)
        return ascii_sum % len(self.bucket)
    
    # 5th hash function implementation based on the recursive computation of
    # Horner's method.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    def hash_function_recursive(self, word):
        if len(word) == 0:
            return 1
        return (ord(word[0]) + 255 * self.hash_function_recursive(word[1:])) % len(self.bucket)
    
    # 6th hash function implementation custom made based on Horner's method
    # and the murmur hashing function.
    # Input: The word to be hashed.
    # Output: The index computed by the hashing function.
    def hash_function_custom(self, word):
        if len(word) == 0:
            return 0
        summation = ord(word[0])
        for i in range(1, len(word)):
#            temp = bin(((133 ** i) * ord(word[i]) + i) ^ (((119 ** i) ^ i) * (summation//3)))
            temp = bin(((133 ** i) * ord(word[i])) ^ (37**i))
            temp = int(temp, 2)
            summation += temp
#            summation += ((133 ** i) * ord(word[i]) + i**i)
            
#            coefficient = (67 * coefficient) + ord(word[i])
#            coefficient += ord(word[i]) * 67
        return summation % len(self.bucket)
    
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
    
    # Inserts a WordEmbedding object into a sorted list by using Binary Search to 
    # find the appropriate location and then inserting the WordEmbedding at that
    # index.
    # Input: A sorted list of WordEmbedding objects and the WordEmbedding object
    #       to be inserted. start and end denote the current portion of the list
    #       being evaluated.
    # Output: None
    # Asume that the list is not None.
    def binary_insertion(self, list,word_embedding, start, end):
        
        # If the list is empty, then the word_embedding is appended.
        if len(list) == 0:
            list.append(word_embedding)
            return
        
        # If start is greater than or equal to the end, then the word_embedding
        # is inserted in its correct position with relation to start.
        if start >= end:
            if word_embedding.word < list[start].word:
                list.insert(start, word_embedding)
            elif word_embedding.word > list[start].word:
                if start == len(list) - 1:
                    list.append(word_embedding)
                else:
                    list.insert(start + 1, word_embedding)
            return
        
        # If the word_embedding already exists, it is not inserted.
        mid = (start + end) // 2
        if list[mid].word == word_embedding.word:
            return
        
        # Otherwise the left or right subtree is traversed accordingly.
        if word_embedding.word < list[mid].word:
            self.binary_insertion(list, word_embedding, start, mid - 1)
        else:
            self.binary_insertion(list, word_embedding, mid + 1, end)
    
    # Inserts a WordEmbedding object by using the specified hashing function.
    # Input: The WordEmbedding object to be inserted and the hashing
    #        function number which will denote which hashing function to use.
    # Output: None
    def insert(self, word_embedding, hash_func_num):
        b = self.h(word_embedding.word, hash_func_num)
        
        # Inserts the WordEmbedding object.
        self.binary_insertion(self.bucket[b], word_embedding, 0, len(self.bucket[b]) - 1)
    
    # Finds the index of the word location in the designated hash table's chain.
    # Input: The chain of the bucket where the word should reside and the
    #        word key whose embedding is being searched for. start and end mark
    #        the current range of the chain's list being analyzed.
    # Output: The index of the where the word resides in the chain's list.
    #         If the word does not reside in the list, then -1 is returned.
    def find_binary_search(self, chain, key, start, end):
        
        # If start is greater than end, then the word is not in the list.
        if start > end:
            return -1

        mid = (start + end) // 2
        
        # If the word is found, the index is returned.
        if key == chain[mid].word:
            return mid
        
        # The range of the list searched is based on the key's relation with the
        # middle value.
        if key < chain[mid].word:
            return self.find_binary_search(chain, key, start, mid - 1)
        return self.find_binary_search(chain, key, mid + 1, end)
    
    # Returns WordEmbedding object's emb attribute if the word_embedding is
    # found in the hash table.
    # Input: The word to be searched for, the hashing function number, and 
    #        an index_usage_hash table which will update the index where the
    #        word should reside by 1.
    # Output: If the WordEmbedding was found, then the emb attribute is
    #         returned.  Otherwise, None is returned.
    def find(self,k, function_num, index_usage_hash_table):
        
        # Finds the bucket where the word should reside.
        b = self.h(k, function_num)
        
        # Increments the index's reference in the hash table by 1.
        if index_usage_hash_table.item[b] < 0:
            index_usage_hash_table.item[b]  = 1
        else:
            index_usage_hash_table.item[b] += 1
        
        # Performs binary search to find the word.
        i = self.find_binary_search(self.bucket[b], k, 0, len(self.bucket[b]) - 1)
        
        # If the word found, then the emb attribute of the WordEmbedding object
        # is returned.
        if i != -1:
            return self.bucket[b][i].emb
        return None
    
    # Caluclates the number of WordEmbedding objects in the hash table.
    # Input: None
    # Output: The number of WordEmbedding objects in the hash table.
    def num_elements(self):
        num_elements = 0
        
        # Calculates the number of WordEmbedding objects in the hash table.
        for i in self.bucket:
            num_elements += len(i)
        return num_elements
    
    # Caluclates the number of empty buckets in the hash table.
    # Input: None
    # Output: The number of empty buckets in the hash table.
    def num_empty_lists(self):
        empty_lists = 0
        for i in self.bucket:
            if len(i) == 0:
                empty_lists += 1
        return empty_lists