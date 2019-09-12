# Course: CS2302 Data Structures
# Date of Last Modification: September 10, 2019
# Assignment: Extra Credit Activation Records
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this extra credit was to implement the recursive
#          Tower of Hanoi function by using a stack.

from activationStack import Stack
from activationStack import Node
from activationStack import ActivationRecord

# Recursive method provided that performs the Tower of Hanoi
# Input: the number of disks and the three poles: source, spare, and stack
# Output: None, except where the disks are moved.
def hanoiOriginal(disks, source, spare, dest):
    if disks> 1:
        hanoiOriginal(disks - 1, source, dest, spare)
        print("Move disk from", source,"to",dest)
        hanoiOriginal(disks - 1, spare, source, dest)
    else:
        print("Move disk from", source,"to", dest)
        
# Iterative method that uses a stack to perform the Tower of Hanoi algorithm
# Input: the stack that will hold the activationRecord objects.
# Output: None, except where the disks are moved.
def hanoi(stack):
    while not stack.isEmpty():
        currActivationRecord = stack.peek()
        
        # Creates a new activation record and pushes it to the stack if the
        # current one is has an index pointer of 3 and more than 1 disk.
        if currActivationRecord.indexPointer == 3 and currActivationRecord.disks > 1:
            newRecord = ActivationRecord(currActivationRecord.disks - 1, 
                                         currActivationRecord.source, 
                                         currActivationRecord.dest, 
                                         currActivationRecord.spare, 3)
            currActivationRecord.indexPointer = 6
            stack.push(newRecord)
            
        # For all other cases the movement of the disk is printed and the
        # current activation record is popped from the stack.
        else:
            print("Move disk from", currActivationRecord.source, "to",
                  currActivationRecord.dest)
            stack.pop()
            
            # If the index pointer is 6, then a new activation record is 
            # pushed to the stack.
            if currActivationRecord.indexPointer == 6:
                newRecord = ActivationRecord(currActivationRecord.disks - 1, 
                                         currActivationRecord.spare, 
                                         currActivationRecord.source, 
                                         currActivationRecord.dest, 3)
                stack.push(newRecord)

# Main method that prints the Tower of Hanoi steps based on the number of disks
# that the user provides.
# Input: None
# Output: None
numDisks = int(input("Enter the number of disks: "))

if numDisks >= 1:
    initialActivationRecord = Node(ActivationRecord(numDisks,"A", "B", "C", 3))
    stack = Stack(initialActivationRecord)
    
    print("Expecting:")
    hanoiOriginal(numDisks, "A", "B", "C")
    
    print("\nActual:")
    hanoi(stack)
else:
    print("Please enter a valid integer greater than 0")
    print("Program terminating")
