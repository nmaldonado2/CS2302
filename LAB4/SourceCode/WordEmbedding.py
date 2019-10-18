# Course: CS2302 Data Structures
# Date of Last Modification: October 12, 2019
# Assignment: Lab 4 - Binary Search Trees and B-Trees
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was read a file containing word embeddings
#          and populate a Binary Search Tree (BST) or B-Tree with 
#          WordEmbedding objects.  The similairts of the word 
#          embedding pairs from a given file is then computed.  The following 
#          file contains the class for WordEmbedding. The embedding attribute
#          must be a list or array of length 50 for this lab.

import numpy as np

# Provided by the instructor.
# Class WordEmbedding
# Attributes: A string representing a word and an embedding that can be a list
#             list or array of integers or floats.
class WordEmbedding(object):
    def __init__(self, word, embedding):
        
        # word must be a string, embedding can be a list or an array or
        # ints or floats
        self.word = word
        self.emb = np.array(embedding, dtype=np.float32)
