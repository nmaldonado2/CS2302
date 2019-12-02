# Course: CS2302 Data Structures
# Date of Last Modification: November 29, 2019
# Assignment: Lab 7 - Algorithm Design Techniques
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to verify if a Hamiltonian cycle exists
#          using randomization or identify if a Hamiltonian cycle exists using
#           randomization. The hash table was used to store edges to ensure
#           that duplicates were not used and to keep track of the edges.

# Class HashTableChain
# Attributes: 2D list of buckets.
# Behaviours: insert and the hash function h.
class HashTableChain(object):
    
    # Provided by the instructor.
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self,size):  
        self.bucket = [[] for i in range(size)]
     
    # Hash function that maps element to the based on the length of bucket.
    # Input: The value to be hashed.
    # Output: The index where element should be hashed to.
    def h(self, element):
        return element%len(self.bucket)    
            
    # Inserts edge into the hash table.
    # Input: edge, in the format of (source, destination, weight)
    # Output: 1 if the insertion was successful or -1 otherwise.
    def insert(self, edge):
        
        # Inserts edge in appropriate bucket (list) 
        # Does nothing if edge is already in the table.
        b1 = self.h(edge[0])
        b2 = self.h(edge[1])
        already_exists = False
        for item in self.bucket[b1]:
            if item[0] == edge[0] and item[1] == edge[1]:
                already_exists = True
        for item in self.bucket[b2]:
            if item[0] == edge[1] and item[1] == edge[0]:
                already_exists = True
        if not already_exists:
            self.bucket[b1].append(edge)
            return 1
        return -1
    
    # Inserts edge into the hash table.
    # Input: edge, in the format of (source, destination, weight) will be hashed
    #        as long as it does not already exist in the hash table. Edge will
    #        also be hashed as (destination, source, and weight).
    # Output: 1 is returned if the inerstion was successful. Otherwise -1 is
    #         returned.
    def insert_double(self, edge):
        
        # Inserts edge in appropriate bucket (list) 
        # Does nothing if edge is already in the table
        b1 = self.h(edge[0])
        b2 = self.h(edge[1])
        for item in self.bucket[b1]:
            if item[0] == edge[0] and item[1] == edge[1]:
                return -1
        for item in self.bucket[b2]:
            if item[0] == edge[1] and item[1] == edge[0]:
                return -1

        self.bucket[b1].append(edge)
        self.bucket[b2].append([edge[1], edge[0], edge[2]])
        return 1
            
    # Inserts a word based on the string length into the hash table.
    # Input: Word to be hashed based on the string length.
    # Output: None
    # Assume that the word has not already been inserted.  However, based
    # on the hash table's implementation, duplicates will not affect the 
    # random selection of words of the same length.
    def insert_word(self, word):
        
        # Inserts word in appropriate bucket (list) 
        b = self.h(len(word))
        self.bucket[b].append(word)

    # Counts the number of elements in each bucket which represent the number
    # of edges. If a bucket does not have two elements, False is returned.
    # Input: None
    # Output: Returns true if all buckets have two elements. False is otherwise
    #         returned.
    def correct_num_edges(self):
        for bucket in self.bucket:
            if len(bucket) != 2:
                return False
        return True
    
    # Formats the elements in each bucket to demonstrate a cycle of edges.
    # Input: None
    # Output: The cycle of edges.
    # Assume that the buckets contain a hamiltonian cycle in which all buckets
    # have exactly two elements and all the edges are double hashed and connected.
    def format_elements(self):
        prev_vertex = 0
        curr_vertex = self.bucket[0][1][1]
        
        # Assume each bucket has two elements
        cycle = [[self.bucket[0][0][1], 0],[0, curr_vertex]]
        
        # Builds the cycle until it contains as many edges as vertices.
        while len(cycle) < len(self.bucket):
            
            # If the adjacent edge of the current vertex is not the previously
            # added vertex, then the edge is appended to the cycle, previous
            # is updated to the current vertex, and the next current vertex
            # is evaluated.
            for element in self.bucket[curr_vertex]:
                if element[1] != prev_vertex:
                    cycle.append([curr_vertex, element[1]])
                    prev_vertex = curr_vertex
                    curr_vertex = element[1]
                    break
        return cycle