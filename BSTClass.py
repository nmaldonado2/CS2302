# Course: CS2302 Data Structures
# Date of Last Modification: October 12, 2019
# Assignment: Lab 4 - Binary Search Trees and B-Trees
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was read a file containing word embeddings
#          and populate a Binary Search Tree (BST) or B-Tree with 
#          WordEmbedding objects.  The similarities of the word 
#          embedding pairs from a given file is then computed.  The following 
#          file contains class for the B-Tree.  The corresponding functions
#          inlcude the number of nodes, the height, insertion, and search.

# Provided by the instructor.
# Class BST
# Attributes: Data that the node will contain and the left and right BST node
#             that the current node points to.
class BST(object):
    def __init__(self, data, left = None, right = None):
        self.data = data
        self.left = left
        self.right = right

# Calculates the number of nodes rooted at the BST node T.
# Input: The root of BST whose number of rooted nodes will be calculated.
# Output: The number of nodes rooted at BST node T.
def NumberOfNodesBST(T):
    if T is None:
        return 0
    return 1 + NumberOfNodesBST(T.left) + NumberOfNodesBST(T.right)

# Caclulates the height of the BST.
# Input: The root of BST whose height will be calculated
# Output: The height of the BST rooted at BST node T. Negative one is returned
#         if the BST is empty.
def HeightBST(T):
    if T is None:
        return -1
    return 1 + max(HeightBST(T.left), HeightBST(T.right))

# Inserts a WordEmbedding object alphabetically into a BST based on the word  
# word attribute of the object.
# Input: The root of the BST and the object to be inserted into the tree.
# Output: The BST with the new object inserted in the tree.
def BSTInsert(T, word_embedding):
    if T is None:
        return BST(word_embedding)
    
    # If the word_embedding already exists in the tree no further traversals 
    # occur.
    if T.data.word == word_embedding.word:
        return T
    
    # Makes recursive calls to the left or right subtree based on the current
    # node's relation with the word_embedding.
    if word_embedding.word < T.data.word:
        T.left = BSTInsert(T.left, word_embedding)
    else:
        T.right = BSTInsert(T.right, word_embedding)
    return T

# Finds a WordEmbedding object in a BST whose word attribute matches the key.
# Input: A string of the word that will be searched for in the BST based
#        on the WordEmbedding's word attribute.
# Output: The emb attribute of the WordEmbedding object if it is found or None
#         otherwise.
def FindWordBST(T, key):
    
    # If the WordEmbedding object is not found in the BST, None is returned.
    if T is None:
        return None
   
    # The WordEmbedding emb attribute is returned if found.
    if T.data.word == key:
        return T.data.emb
    
    # Otherwise the right or left subtree is searched accordingly.
    if key < T.data.word:
        return FindWordBST(T.left, key)
    return FindWordBST(T.right, key)