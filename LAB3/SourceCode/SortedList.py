# Course: CS2302 Data Structures
# Date of Last Modification: October 2, 2019
# Assignment: Lab 3 - Linked Lists
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to implement 10 functions for a 
#          SortedList and List class and calculate the run times.  
#          The 10 functions were Print, Insert, Delete, Merge, IndexOf,
#          Clear, Min, Max, HasDuplicates, and Select.  The following file
#          contains the classes Node, SortedList, and List. For SortedList
#          all of the elements are ordered at all times.  For List, the order
#          of elements is negligible

import math

# Class Node
# Attributes: integral value that represent the data of the Node a pointer
#             to the next Node.
class Node:
    def __init__(self, data, next = None):
        self.data = data
        self.next = next

# Class SortedList
# Attributes: a pointer to the head and tail of the SortedList.
# Behaviors: Print, Insert, Delete, Merge, FindEndOfNodesToAdd, Clear, Min,
#            Max, IndexOf, HasDuplicates, and Select.
class SortedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    # Function that prints every Node's data in a SortedList starting from the
    # head to the tail.
    # Input: None
    # Output: None other than the data from the SortedList is displayed.
    def Print(self):
        
        # Tells the user if the SortedList is empty.
        if self.head is None:
            print("List is empty")
            return
    
        # Otherwise, the SortedList is traversed through and the data from
        # each node is printed.
        curr = self.head
        
        while not curr.next is None:
            print(curr.data, end=" -> ")
            curr = curr.next
        print(curr.data)
    
    # Function that inserts i in its correct place in the SortedList.
    # Input: the integer, i, to be added to the SortedList.
    # Output: None.
    def Insert(self, i):
        if self.head is None:
            self.head = self.tail = Node(i)
            return
        
        node_to_add = Node(i)
        
        # If the i is less than or equal to the integer at the head, then it is 
        # prepended to the SortedList.
        if i <= self.head.data:
            node_to_add.next = self.head
            self.head = node_to_add
            return
        
        # If i is greater than or equal to the integer at the tail, then it is
        # appended to the SortedList.
        if i >= self.tail.data:
            self.tail.next = node_to_add
            self.tail = node_to_add
            return
        
        # Otherwise, the list is iterated through until the next node contains
        # data greater than i.  The Node with i is then added to the list.
        curr = self.head
        while curr.next.data < i:
            curr = curr.next
        node_to_add.next = curr.next
        curr.next = node_to_add

    # Function that deletes all instances of i from the SortedList.
    # Input: the integer, i, to be deleted from the SortedList.
    # Output: None.
    def Delete(self, i):
        if self.head is None or i > self.tail.data:
            return
        
        # dummy_node used in the instance that all integers are removed from
        # the list.
        dummy_node = Node(5)
        dummy_node.next = self.head
        curr = dummy_node
        
        # Iterates until the next node contains data greater than or equal
        # to i.
        while not curr.next is None and curr.next.data < i:
            curr = curr.next
        
        # Removes all instances of i from the SortedList
        while not curr.next is None and curr.next.data == i:
            curr.next = curr.next.next
        
        # Reassigns the tail.
        if curr.next is None:
            self.tail = curr
        
        # Reassigns the head.
        self.head = dummy_node.next
    
    # Function that Merges the SortedList M with the current SortedList.
    # Input: the SortedList M to be merged with the current SortedList.
    # Output: None.
    # Assume that M will always be a SortedList.
    def Merge(self, M):
        if M is None or M.head is None:
            return
        
        # If the current list is empty, its head and tail are assigned to M's
        # head and tail.
        if self.head is None:
            self.head = M.head
            self.tail = M.tail
            return
        
        # If all of M's data is less than the current SortedList's data, it
        # is prepended.
        if M.tail.data <= self.head.data:
            M.tail.next = self.head
            self.head = M.head
            return
        
        # If all of M's data is greater than the current SortedList's data, it
        # is appended.
        if M.head.data >= self.tail.data:
            self.tail.next = M.head
            self.tail = M.tail
            return
        
        dummy_node = Node(5)
        dummy_node.next = self.head
        list1_curr = dummy_node
        list2_curr = M.head
        
        while not list1_curr.next is None and not list2_curr is None:
            
            # If the current node in M contains data less than or equal to 
            # the current list's data, it is inserted into the list.
            if list2_curr.data <= list1_curr.next.data:
                
                # If all of M's data is less than the current data, the entire
                # list is inserted.
                if M.tail.data <= list1_curr.next.data:
                    M.tail.next = list1_curr.next
                    list1_curr.next = list2_curr
                    list2_curr = None
                    
                # Otherwise, the segment of M with data less than or equal
                # to the current data is inserted in the list.
                else:
                    end_node = self.FindEndOfNodesToAdd(list1_curr.next.data, list2_curr)
                    temp_curr = list2_curr
                    list2_curr = end_node.next
                    end_node.next = list1_curr.next
                    list1_curr.next = temp_curr
                    list1_curr = end_node
            
            # Otherwise, list1curr points to the next Node in the current list.
            else:
                list1_curr = list1_curr.next
        
        # If the entire current list has been iterated through and list2_curr
        # still points to more Nodes, the segment is appended to the list.
        if not list2_curr is None:
            list1_curr.next = list2_curr
            self.tail = M.tail
        self.head = dummy_node.next
    
    # Function that finds the end of a segment of Nodes with data less than
    # or equal to the key.
    # Input: a segment of Nodes with values less than or equal to the key.
    # Output: The Node with data greater than the key.
    # Assume that M will always be a SortedList.
    # Assume Node is not null and starts with a value less than or equal to
    # the key.
    def FindEndOfNodesToAdd(self, key, node):
        curr = node
        while curr.next.data <= key:
            curr = curr.next
        return curr
    
    # Function that returns the index of integer i if it exists in the
    # SortedList.
    # Input: the integer i whose index will be returned if it exists in the
    #        SortedList.
    # Output: The index of integer i in the list, where the index of the
    #         first Node is 0. -1 is returned if i does not exist in the 
    #         SortedList.
    def IndexOf(self, i):
        if self.head is None or i < self.head.data or i > self.tail.data:
            return -1
        
        index = 0
        curr = self.head
        
        # index is incremented for every Node iterated through. If i is
        # found, then the index is returned. Otherwise -1 is returned.
        while not curr is None and curr.data <= i:
            if curr.data == i:
                return index
            curr = curr.next
            index += 1
        return -1
    
    # Function that removes all Nodes from the SortedList.
    # Input: None.
    # Output: None.
    def Clear(self):
        self.head = self.tail = None
    
    # Function that returns the minimum value in the SortedList.
    # Input: None.
    # Output: the minimum value or math.inf if the SortedList is empty.
    def Min(self):
        if self.head is None:
            return math.inf
        return self.head.data
    
    # Function that returns the maximum value in the SortedList.
    # Input: None.
    # Output: the maximum value or math.inf if the SortedList is empty.
    def Max(self):
        if self.head is None:
            return math.inf
        return self.tail.data
    
    # Function that returns True if the SortedList has duplicates or False
    # if no duplicates exist.
    # Input: None.
    # Output: True if the SortedList contains duplicates and False otherwise.
    def HasDuplicates(self):
        if self.head is None:
            return False
        
        curr = self.head
        
        # The SortedList is iterated through until duplicates are found or
        # until the end of the list is reached.
        while not curr.next is None:
            
            # If duplicates are found, True is immediately returned.
            if curr.data == curr.next.data:
                return True
            curr = curr.next
        return False
     
    # Function that returns the kth smallest value in the list, where the first
    # smallest value is the 0th smallest value in the list.  If the kth
    # smallest value does not exist in the list, then math.inf is returned.
    # Input: k, which represents the kth smallest value that needs to be
    #        returned.
    # Output: the kth smallest value in the SortedList or math.inf otherwise.
    def Select(self, k):
        if k < 0:
            return math.inf
        
        index = 0
        curr = self.head
        
        # The list is iterated through until the index equals the kth value
        # or the end of the SortedList is reached.
        while index != k and not curr is None:
            curr = curr.next
            index += 1
        
        # If the end of the SortedList is reached, then math.inf is returned.
        if curr is None:
            return math.inf
        return curr.data
    
# Class List
# Attributes: a pointer to the head and tail of the List.
# Behaviors: Print, Insert, Delete, Merge, Clear, Min, Max, IndexOf,
#            HasDuplicates, Select, MergeList, MergeSort, Split, FindMiddle,
#            Partition, and ModifiedQuickSort.    
class List:
    def __init__(self):
        self.head = None
        self.tail = None
    
    # Function that prints every Node's data in a List starting from the
    # head to the tail.
    # Input: None
    # Output: None other than the data from the List is displayed.
    def Print(self):
        
        # Tells the user if the List is empty.
        if self.head is None:
            print("List is empty")
            return
        
        curr = self.head
        
        # Otherwise, the List is traversed through and the data from
        # each node is printed.
        while not curr.next is None:
            print(curr.data, end=" -> ")
            curr = curr.next
        print(curr.data)
    
    # Function appends integer i to the List.
    # Input: the integer, i, to be appended to the List.
    # Output: None.
    def Insert(self, i):
        if self.head is None:
            self.head = self.tail = Node(i)
            return
        
        # Node with integer i is appended to the end of the List.
        self.tail.next = Node(i)
        self.tail = self.tail.next
    
    # Function that deletes all instances of integer i from the List.
    # Input: the integer, i, to be deleted from the List.
    # Output: None.
    def Delete(self, i):
        if self.head is None:
            return
                
        dummy_node = Node(4)
        dummy_node.next = self.head
        curr = dummy_node
        
        # Iterates through the list and removes all instances of i.
        while not curr.next is None:
            if curr.next.data == i:
                curr.next = curr.next.next
            else:
                curr = curr.next
                
        # Reassigns the head and tail of the List if they were altered during
        # deletion.
        self.head = dummy_node.next
        if self.head is None:
            self.tail = self.head
        else:
            self.tail = curr
    
    # Function that Merges the List M with the current List by appending M.
    # Input: the List M that will be appended to the end of the current List.
    # Output: None.
    # Assume that M will always be a List.
    def Merge(self, M):
        if M is None:
            return
        
        # If the current list is empty, its head and tail point to M's head
        # and tail.
        if self.head is None:
            self.head = M.head
            self.tail = M.tail
            return
        
        # Otherwise, M is appended to the current List.
        self.tail.next = M.head
        self.tail = M.tail
    
    # Function that returns the index of integer i if it exists in the
    # List.
    # Input: the integer i whose index will be returned if it exists in the
    #        SortedList.
    # Output: The index of integer i in the list, where the index of the
    #         first Node is 0. -1 is returned if i does not exist in the 
    #         List.
    def IndexOf(self, i):        
        curr = self.head
        index = -1
        
        # index is incremented for every Node iterated through. If i is
        # found, then the index is returned. Otherwise -1 is returned.
        while not curr is None:
            index += 1
            if curr.data == i:
                return index
            
            curr = curr.next
        return -1
    
    # Function that removes all Nodes from the SortedList.
    # Input: None.
    # Output: None.
    def Clear(self):
        self.head = self.tail = None
    
    # Function that returns the minimum value in the List.
    # Input: None.
    # Output: the minimum value or math.inf if the List is empty.
    def Min(self):
        if self.head is None:
            return math.inf
        
        min = self.head.data
        curr = self.head
        
        # Iterates through the List and assigns min with the smallest value.
        while not curr is None:
            if curr.data < min:
                min = curr.data
            curr = curr.next
        return min
    
    # Function that returns the maximum value in the List.
    # Input: None.
    # Output: the maximum value or math.inf if the List is empty.
    def Max(self):
        if self.head is None:
            return math.inf
        
        max = self.head.data
        curr = self.head
        
        # Iterates through the List and assigns max with the largest value.
        while not curr is None:
            if curr.data > max:
                max = curr.data
            curr = curr.next
        return max  
    
    # Function that returns a merged list in order.
    # Input: the two lists to be merged.
    # Output: a merged list of Nodes that is sorted in ascending order.
    def MergeList(self, left_list, right_list):
        if left_list is None:
            return right_list
        if right_list is None:
            return left_list
        
        dummy_node = Node(5, left_list)
        left_curr = dummy_node
        right_curr = right_list
        
        # Appends Nodes to the dummy_node, based on the value of the current
        # Nodes referenced by left_curr and right_curr.
        while not left_curr.next is None and not right_curr is None:
            
            # If the right_curr has data less than or equal to the left_curr
            # data, then the right_curr Node is inserted before the left_curr
            if right_curr.data <= left_curr.next.data:
                temp_curr = right_curr.next
                right_curr.next = left_curr.next
                left_curr.next = right_curr
                right_curr = temp_curr
            left_curr = left_curr.next
        
        # If more Nodes exist in the right_list, then it is appended to the 
        # end of left_list.
        if not right_curr is None:
           left_curr.next = right_curr 
            
        return dummy_node.next
    
    # Function that sorts the List by constantly halving the list and then
    # merging those halves.
    # Input: the list to be sorted.
    # Output: a merged list that is sorted in ascending order.
    def MergeSort(self, n):
        if n is None or n.next is None:
            return n
        
        # Retrieves the left and right sublist.
        left_list, right_list = self.Split(n)
        
        # Performs mergeSort on the left and righ sublists.
        left_list = self.MergeSort(left_list)
        right_list = self.MergeSort(right_list)
        
        # Returns the merged, ordered left and right sublist.
        return self.MergeList(left_list, right_list)        
    
    # Function that returns True if the List has duplicates or False
    # if no duplicates exist.
    # Input: None.
    # Output: True if the List contains duplicates and False otherwise.
    def HasDuplicates(self):
        if self.head is None:
            return False
        
        # Sorts a copy of the current List
        sorted_list = self.MergeSort(self.head)
        
        curr = sorted_list
        
        # The List is iterated through until duplicates are found or
        # until the end of the list is reached.
        while not curr.next is None:
            
            # If duplicates are found, True is immediately returned.
            if curr.data == curr.next.data:
                return True
            curr = curr.next
        
        return False
    
    # Function that returns the left and right sublist of n halved.
    # Input: a list of Nodes, n, that will be divided evenly into two
    #        sub-lists.
    # Output: The two sublists divided from n.
    def Split(self, n):
        if n is None: 
            return None
        
        left_list = List()
        lag = n
        fast = n
        left_list.head = left_list.tail = Node(lag.data)
        
        # Finds the middle of the list.  Every time lag is updated, a Node is
        # added to the left_list.
        while not fast.next is None and not fast.next.next is None:
            lag = lag.next
            left_list.tail.next = Node(lag.data)
            left_list.tail = left_list.tail.next
            fast = fast.next.next
        
        # The right sublist consists of all Nodes after lag.
        return left_list.head, lag.next        
    
    # Function that returns the middle of a list.
    # Input: a list of Nodes, n, whose middle Node will be found.
    # Output: The middle Node of the list n.
    def FindMiddle(self, n):
        if n is None:
            return None
        
        lag = n
        fast = n
        
        # The lag pointer is updated once for every two reassignments of fast.
        # This results in lag reaching the middle of the list when fast
        # reaches the end of the list.
        while not fast.next is None and not fast.next.next is None:
            lag = lag.next
            fast = fast.next.next
            
        return lag
    
    # Function that partitions the list into a left and right sublist by using
    # a pivot.  All elements less than the pivot will be in the left sublist
    # and all of the elements greater than or equal to the pivot will be in the
    # right sublist.
    # Input: a list of nodes, n, to be partitioned.
    # Output: The left and right sublist where the left consists of Nodes with 
    #         integers less than the pivot and the right pivot with integers
    #         greater than or equal to the pivot.
    def Partition(self, n):
        if n is None:
            return (None, None, -1)
        
        if n.next is None:
            return (None, Node(n.data), 0)
        
        # The middle value of the list is assigned as the pivot.
        pivot = self.FindMiddle(n).data
        index = 0
        dummy_right = Node(5)
        dummy_left = Node(5)
        right_curr = dummy_right
        left_curr = dummy_left
        curr = n
        
        # Nodes are added to the sublists depending on their values.
        while not curr is None:
            
            # If the current Node has data less than the pivot, it is added to
            # the left sublist. Index is also incremented to represent the
            # location of the pivot.
            if curr.data < pivot:
                left_curr.next = Node(curr.data)
                left_curr = left_curr.next
                index += 1
                
            # If the current Node has data equal to the pivot, it is prepended
            # to the right sublist.
            elif curr.data == pivot:
                n = Node(curr.data)
                n.next= dummy_right.next
                dummy_right.next = n
                if not right_curr.next is None:
                    right_curr = right_curr.next
                    
            # If the current Node has data greater than the pivot, it is
            # appended to the right sublist.
            else:
                right_curr.next = Node(curr.data)
                right_curr = right_curr.next
            curr = curr.next

        return dummy_left.next, dummy_right.next, index
    
    # Function that finds the kth smallest element by constantly partitioning
    # a List into left and right sublists and then identifying if the index
    # of the pivot returned is equal to k.
    # Input: a list of nodes, n,  and the kth value to be found.
    # Output: The kth smallest element found.
    def ModifiedQuickSort(self, n, k):
        if n is None:
            return math.inf
        
        # n is partitioned.
        left_list, right_list, index = self.Partition(n)
        
        # returns the pivot value from Partition if k equals the index.
        if index == k:
            return right_list.data
        
        # If the index is less than k, then the right_list is evaluated. k is
        # decremented by the index plus one since we are now
        # looking for the kth element of that sublist.
        if index < k:
            return self.ModifiedQuickSort(right_list.next, k - (index + 1))
        
        # Otherwise, the left_list is evaluated.
        return self.ModifiedQuickSort(left_list, k)
    
    # Function that finds the kth smallest element by using the
    # ModifiedQuickSort function to find the kth smallest element in the list.
    # Input: k representing the kth smallest element to be found.
    # Output: The kth smallest element or math.inf if the list is empty
    #         or k is outside of the range of the List.
    def Select(self, k):
        if (k < 0) or (self.head is None):
            return math.inf
        
        return self.ModifiedQuickSort(self.head, k)        
