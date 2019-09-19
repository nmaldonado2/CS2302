# Course: CS2302 Data Structures
# Date of Last Modification: September 18, 2019
# Assignment: Lab 2 - Runtime Complexity
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to identify if the number of comparisons
#          and performance time matched the theoretical runtime complexity for
#          each sorting algorithm.  This file includes classes for Record
#          and Stack that will be used for the QuickSort with 
#          stack algorithm.

# Class Record
# Attributes: integral values that represent the low and high index of the 
#             list to be evaluated.
# Assume the low and high are numbers greater than or equal to 0.
class Record:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        
# Class Node
# Attributes: the activation_record that the node holds and a pointer to the 
#             next node.
class Node:
    def __init__(self, activationRecord, next = None):
        self.activationRecord = activationRecord
        self.next = next

# Class Stack
# Attributes: the top and bottom of the stack and the stack's size.
class Stack:
    def __init__(self, head=None):
        self.top = self.bottom = head
        if self.top is None:
            self.size = 0
        else:
            self.size = 1
    
    # Function that returns true if the stack is empty or false otherwise.
    # Input: None
    # Output: True if the stack is empty or false otherwise.
    def isEmpty(self):
        return self.size == 0
    
    # Removes The element at the top of the stack and returns the element.
    # Input: None
    # Output: The element removed from the top of the stack.
    def pop(self):
        
        # Returns None if the stack is empty.
        if self.size == 0:
            print("Empty stack")
            return
        
        # Removes element at the top of the stack.
        element = self.top.activationRecord
        if self.size == 1:
            self.top = self.bottom = None
        else:
            self.top = self.top.next
        
        # Updates size.
        self.size -= 1
        return element
    
    # Pushes element to the stop of the stack.
    # Input: The element to be pushed to the top of the stack.
    # Output: None.
    def push(self, activationRecord):
        
        # Adds element to the top of the stack.
        node = Node(activationRecord)
        if self.size == 0:
            self.top = self.bottom = node
        else:
            node.next = self.top
            self.top = node
            
        # Updates size.
        self.size += 1
    
    # Returns the element at the top of the stack.
    # Input: None
    # Output: The element at the top of the stack.
    def peek(self):
        
        # Returns None if the stack is empty.
        if self.top is None:
            return None
        return self.top.activationRecord
