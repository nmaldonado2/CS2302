# Course: CS2302 Data Structures
# Date of Last Modification: October 31, 2019
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
#          well as the running times for the construction of the table and the 
#          similarity calculations. This file contains the WordEmbedding class
#          whose objects will be used to populate the hash tables.

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