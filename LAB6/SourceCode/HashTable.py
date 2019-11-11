
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
    # Input: k, in the format of (source, destination, edge)
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