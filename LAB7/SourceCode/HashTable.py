# Course: CS2302 Data Structures
# Date of Last Modification: November 14, 2019
# Assignment: Lab 6 - Graphs
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to represent graphs through adjacency
#          lists, adjacency matrices, and edge lists. These grahical
#          representations were then used to solve the riddle concerning a fox,
#          chicken, sack of grain, and person by using breadth first search and
#          depth first search.  This file provides the class for a hash table
#          with chaining. This hash table with chaining was used to store valid
#          edges that would later be used to populate a graph.

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
     
    # Hash function that maps k to the based on the length of bucket.
    # Input: The value to be hashed.
    # Output: The index where k should be hashed to.
    def h(self,k):
        return k%len(self.bucket)    
            
    # Inserts k into the hash table.
    # Input: k, in the format of (source, destination, weight)
    # Output: 1 if the insertion was successful or -1 otherwise.
    def insert(self,k):
        
        # Inserts k in appropriate bucket (list) 
        # Does nothing if k is already in the table
        b1 = self.h(k[0])
        b2 = self.h(k[1])
        already_exists = False
        for item in self.bucket[b1]:
            if item[0] == k[0] and item[1] == k[1]:
                already_exists = True
        for item in self.bucket[b2]:
            if item[0] == k[1] and item[1] == k[0]:
                already_exists = True
        if not already_exists:
            self.bucket[b1].append(k)
            return 1
        return -1
    
    def insert_double(self, k):
        
        # Inserts k in appropriate bucket (list) 
        # Does nothing if k is already in the table
        b1 = self.h(k[0])
        b2 = self.h(k[1])
        for item in self.bucket[b1]:
            if item[0] == k[0] and item[1] == k[1]:
                return -1
        for item in self.bucket[b2]:
            if item[0] == k[1] and item[1] == k[0]:
                return -1

        self.bucket[b1].append(k)
        self.bucket[b2].append([k[1], k[0], k[2]])
        return 1
    
    def find(self, source, dest):
        b1 = self.h(source)
        b2 = self.h(dest)

        for item in self.bucket[b1]:
            if item[0] == source and item[1] == dest:
                return True
        for item in self.bucket[b2]:
            if item[0] == dest and item[1] == source:
                return True
        return False
    
    def display(self):
        for i in self.bucket:
            for element in i:
                print(element)