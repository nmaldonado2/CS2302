# Course: CS2302 Data Structures
# Date of Last Modification: September 10, 2019
# Assignment: Extra Credit Activation Records
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this extra credit was to implement the recursive
#          Tower of Hanoi function by using a stack. This file includes a 
#          stack that will store activationRecord objects.

# ActivationRecord objects have the attributes of the number of disks,
# the pole locations, and the indexPointer which points to the "next line
# of execution".
class ActivationRecord:
    def __init__(self,disks, source, spare, dest, indexPointer):
        self.disks = disks
        self.source = source
        self.spare = spare
        self.dest = dest
        self.indexPointer = indexPointer

# Node class that will contain the activationRecord objects.
class Node:
    def __init__(self, activationRecord, next=None):
        self.activationRecord = activationRecord
        self.next = next

# Stack class that will be used to store and pop the activationRecords.
class Stack:
    def __init__(self, head=None):
        self.top = self.bottom = head
        if self.top is None:
            self.size = 0
        else:
            self.size = 1
    
    def getSize(self):
        return self.size
    
    def isEmpty(self):
        return self.size == 0
    
    def pop(self):
        if self.size == 0:
            print("Empty stack")
            return
        element = self.top.activationRecord
        if self.size == 1:
            self.top = self.bottom = None
        else:
            self.top = self.top.next
            
        self.size -= 1
        return element
    
    def push(self, activationRecord):
        n = Node(activationRecord)
        if self.size == 0:
            self.top = self.bottom = n
        else:
            n.next = self.top
            self.top = n
        self.size += 1
    
    def peek(self):
        return self.top.activationRecord
    
    def print(self):
        curr = self.top
        while not curr is None:
            print(curr.val, end = " ")
            curr = curr.next
        print()