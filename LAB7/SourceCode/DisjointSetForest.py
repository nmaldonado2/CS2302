# Course: CS2302 Data Structures
# Date of Last Modification: November 29, 2019
# Assignment: Lab 7 - Algorithm Design Techniques
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to verify if a Hamiltonian cycle exists
#          using randomization or identify if a Hamiltonian cycle exists using
#           randomization. This file contains the class for the disjoint set
#           forest which was used to ensure that a cycle, other than the
#           Hamiltonian cycle, did not exist in the graph.

import numpy as np

# Class DSF
# Attributes: Parent array
# Behaviours: find using path compression and union.
class DSF:
    
    # Constructor provided by the instructor.
    # Creates a disjoint set forest with all sets initialized as root nodes.
    # Input: the number of sets which denotes the number of forests.
    # Output: None
    def __init__(self, sets):
        
        # Creates forest with 'sets' root nodes
        self.parent = np.zeros(sets,dtype=int)-1

    # Finds the root of i using path compression.
    # Input: i whose root will be found.
    # Output: the root of i.
    # Assume i is within the range of parent.
    def find(self, i):
        if self.parent[i] < 0:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    # Provided by the instructor.
    # Unites the set of j with the set of of i if the sets are not connected
    # components. the root of set j will be assigned to the root of set i.
    def union(self,i,j):
        
        # Makes root of j's tree point to root of i's tree if they are different
        # Return 1 if a parent reference was changed, 0 otherwise
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_j] = root_i
            return 1
        return 0         