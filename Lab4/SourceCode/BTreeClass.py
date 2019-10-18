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
#          file contains class for the BST and corresponding functions
#          to find the number of nodes in a tree, for the height, for insertion,
#          and for search.

# Provided by the instructor.
# Class BTree
# Attributes: Data that the B-Tree node will conatin, the children of the 
#             B-Tree node, whether the node is a leaf, and the maximum amount
#             of data that the node can contain.
class BTree(object):
    def __init__(self, data, child=[], is_leaf = True, max_data = 5):
        self.data = data
        self.child = child
        self.is_leaf = is_leaf
        
        if max_data < 3:
            max_data = 3
        if max_data % 2 == 0:
            max_data += 1
        self.max_data = max_data

# Calculates the number of nodes in the B-Tree
# Input: The root of B-Tree whose number of nodes will be calculated.
# Output: The number of nodes in the B-Tree.
def NumberOfNodesBTree(T):
    
    # Counts the number of nodes in a tree.
    num_nodes = 1
    if T.is_leaf:
        return num_nodes
    for i in T.child:
        num_nodes += NumberOfNodesBTree(i)
    return num_nodes

# Caclulates the height of the B-Tree.
# Input: The root of B-Tree whose height will be calculated
# Output: The height of the B-Tree rooted at node T. Negative one is returned
#         if the B-Tree is empty.
def HeightBTree(T):
    if T.is_leaf:
        return 0
    return 1 + HeightBTree(T.child[-1])

# Finds the index of T's child where the key could be located by using Binary
# Search.
# Input: The parent B-Tree node and key used to identify which child should
#        be evaluated next. The start and end index denote the current portion
#        of the list being searched.
# Output: The index of T's child where the key could potentially be located. If
#         the key already exists in the tree, -1 is returned.
def FindChildBinarySearch(T, key, start, end):
    
    # If start is greater than end, then the child is located at index start.
    if start > end:
        return start
    
    # If start is equal to end, then the child is located at index start 
    # or start plus 1.
    if start == end:
        if key > T.data[start].word:
            return start + 1
        return start
    
    mid = (start + end) // 2
    
    # If the key already exists, -1 is returned.
    if key == T.data[mid].word:
        return -1
    
    # The range of the list searched is based on the key's relation with the
    # middle value.
    if key < T.data[mid].word:
        return FindChildBinarySearch(T, key, start, mid - 1)
    return FindChildBinarySearch(T, key, mid + 1, end)

# Outer method for the inner recursive method that finds the appropriate child
# of T based on val.
# Input: The parent T B-Tree node and the value.  The index of T's child
#        where val could potentially be located will be returned.
# Output:The index of T's child where val could potentially be located will be 
#        returned.
def FindChild(T, val):
    return FindChildBinarySearch(T, val.word, 0, len(T.data) - 1)

# Provided by the instructor.
# Initiates the insertion of a WordEmbedding in T if it is a leaf or continues
# to traverse the B-Tree until the correct node is found to insert the object.
# Input: The current B-Tree node where the WordEmbedding object may be 
#        inserted.
# Output: None
def InsertInternal(T, i):
    
    # Inserts value at the leaf.
    if T.is_leaf:
        InsertLeaf(T, i)
        
    # Otherwise finds the next child to be accessed and splits the child
    # if it is full.
    else:
        k = FindChild(T, i)
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.data.insert(k, m)
            T.child[k] = l
            T.child.insert(k + 1, r)
            k = FindChild(T, i)
        InsertInternal(T.child[k], i)

# Provided by the instructor.
# Splits the current B-Tree node T by creating a left and right child from the
# full node.
# Input: A full B-Tree node T.
# Output: The middle value of the data at T and a left and right child.  These
#         children contain data, and the children, if applicable, to 
#         left or right of middle.
def Split(T):
    middle = T.max_data // 2
    
    # Creates a left and right subchild for T based on whether T is a leaf.
    if T.is_leaf:
        left_child = BTree(T.data[:middle], max_data = T.max_data)
        right_child = BTree(T.data[middle + 1:], max_data = T.max_data)
        
    else:
        left_child = BTree(T.data[:middle], T.child[:middle +1], T.is_leaf, T.max_data)
        right_child = BTree(T.data[middle + 1:], T.child[middle + 1:], T.is_leaf, T.max_data)
    return T.data[middle], left_child, right_child

# Inserts a WordEmbedding object into a sorted list by traversing the list one
# element at a time until the appropriate position is found.
# Input: A sorted list of WordEmbedding objects and the WordEmbedding object
#       to be inserted.
# Output: None
def LinearInsertion(list, word_embedding):
    
    # If the word_embedding's word is greater than the last word in the list,
    # it is appended at the end.
    if word_embedding.word > list[-1].word:
        list.append(word_embedding)
        
    # Otherwise, the word_embedding is inserted in it's correct position.
    else:
        i = 0
        while word_embedding.word > list[i].word:
            i += 1
        list.insert(i, word_embedding)

# Inserts a WordEmbedding object into a sorted list by using Binary Search to 
# find the appropriate location and then inserting the WordEmbedding at that
# index.
# Input: A sorted list of WordEmbedding objects and the WordEmbedding object
#       to be inserted. start and end denote the current portion of the list
#       being evaluated.
# Output: None
# Asume that the list is not None.
def BinaryInsertion(list,word_embedding, start, end):
    
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
        BinaryInsertion(list, word_embedding, start, mid - 1)
    else:
        BinaryInsertion(list, word_embedding, mid + 1, end)
       
# Inserts a WordEmbedding object into a leaf B-Tree by initiating an insertion
# method.
# Input: The leaf B-Tree node and the WordEmbedding object to be inserted.
# Output: None
def InsertLeaf(T, word_embedding):
    
    # Inserts the word_embedding into a leaf node by using LinearInsertion
    # or binary insertion.
    if len(T.data) == 0:
        T.data.append(word_embedding)
    
    # Testing demonstrated that for lists with 115 elements or less, the Linear
    # Insertion function had faster running times than BinaryInsertion.
    elif len(T.data) <= 115:
        LinearInsertion(T.data, word_embedding)
    else:
        BinaryInsertion(T.data, word_embedding, 0, len(T.data) - 1)

# Provided by the instructor.
# Identifies if the current B-Tree node's data is full.
# Input: The B-Tree node to be evaulated
# Output: True is returend if the B-Tree node contains the maximum amount of
#         data.  False is otherwise returned.
def IsFull(T):
    return len(T.data) >= T.max_data

# Provided by the instructor.
# Initiates the insertion of a WordEmbedding object in a B-Tree.
# Input: The B-Tree node and WordEmbedding object to be inserted in the tree.
# Output: None.
def BTreeInsert(T, i):
    
    # If T is not full, then i is prepared to be inserted.
    if not IsFull(T):
        InsertInternal(T, i)
        
    # Otherwise, T needs to split before inserting i.
    else:
        m, l, r = Split(T)
        T.data = [m]
        T.child = [l, r]
        T.is_leaf = False
        k = FindChild(T, i)
        InsertInternal(T.child[k], i)


# Finds the index of the WordEmbedding object in the list or the index of the
# of the child where the key could reside.
# Input: A string of a word that will be searched for in the list. start 
#        and end denote the segment of the list being evaluated.
# Output: The index of the key in the list or the index of the child where the
#         WordEmbedding object could reside.
def BinarySearch(list, key, start, end):
    
    # Returns the index of where the key could lie in a specific child.
    if start >= end:
        if key <= list[start].word:
            return start
        return start + 1
    
    mid = (start + end) // 2
    
    # Returns the index of where the key is located in the list.
    if list[mid].word == key:
        return mid
    
    # Otherwise continues to look at the left or right sublist.
    if key < list[mid].word:
        return BinarySearch(list, key, start, mid - 1)
    else:
        return BinarySearch(list, key, mid + 1, end)
  
# Finds a WordEmbedding object in a B-Tree whose word attribute matches 
# the key.
# Input: A string of a word that will be searched for in the B-Tree based
#        on the WordEmbedding's word attribute.
# Output: The emb attribute of the WordEmbedding object if it is found or None
#         otherwise.      
def FindWordBTree(T, key):
    if key > T.data[-1].word:
       
        # If the key does not exist in the leaf T, then None is returned.
        if T.is_leaf:
            return None
       
        # If the key is greater then the last WordEmbedding in T then the 
        # right most child is evaluated.
        return FindWordBTree(T.child[-1], key)
    
    # Otherwise T's data is evaluated to see if the key resides in the list.
    i = BinarySearch(T.data, key, 0, len(T.data) - 1)
    
    # If the key does reside in the list, then the emb attribute is returned.
    if key == T.data[i].word:
        return T.data[i].emb
    
    # Otherwise, the child at index i is evaluated.
    return FindWordBTree(T.child[i], key)
