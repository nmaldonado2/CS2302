# Course: CS2302 Data Structures
# Date of Last Modification: October 2, 2019
# Assignment: Lab 3 - Linked Lists
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to implement 10 functions for a 
#          SortedList and List class and calculate the run times.  
#          The 10 functions were Print, Insert, Delete, Merge, IndexOf,
#          Clear, Min, Max, HasDuplicates, and Select.  The following program 
#          allows the user to run automated tests for each of the functions
#          described above or create their own linked list and perform tests.

from SortedList import SortedList, List
import random
import time

# Creates a SortedList and List of random integers within the range [0, size]
# Input: The size of the lists to be created
# Output: A list containing a SortedList and List.
def random_linked_list(size):
    list_of_lists = [SortedList(), List()]
    
    # Populates lists.
    for x in range(size):
        random_int = random.randint(0, size)
        list_of_lists[0].Insert(random_int)
        list_of_lists[1].Insert(random_int)
    return list_of_lists

# Creates a SortedList and List of integers without duplicates
# Input: The size of the lists to be created
# Output: A list containing a SortedList and List.
def random_non_duplicate_list(size):
    list_of_lists = [SortedList(), List()]
    
    # Creates lists without duplicates and out or order.
    for x in range(0, size, 2):
        list_of_lists[0].Insert(x)
        list_of_lists[1].Insert(x)
    
    for x in range(1, size, 2):
        list_of_lists[0].Insert(x)
        list_of_lists[1].Insert(x)
    return list_of_lists

# Performance test for Print function that calculates the performance time.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.  
def print_performance_test(printSizes):
    for size in printSizes:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        
        # Runs tests for every linked list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList:")
            else:
                print("List:")
            start_time = time.perf_counter()
            list_of_lists[i].Print()
            elapsed_time = time.perf_counter() - start_time
            print("Linked List Print: %.6f ms\n" % elapsed_time)

# Performance test for Insert function that calculates the performance time for
# inserting integral values of -1, a value of size divided by 2, the value
# of the tail minus one, and the value of the size plus 2.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.  
def insertion_performance_test(insertion_sizes, will_print):
    for size in insertion_sizes:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        
        # Performs tests for each list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList:")
            else:
                print("List:")
                
            if will_print:
                print("\nBefore: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Insertion of -1
            start_time = time.perf_counter()
            list_of_lists[i].Insert(-1)
            elapsed_time = time.perf_counter() - start_time
            print("Insertion of -1: %.6f ms" % elapsed_time)
            
            # Insertion of size divided by 2
            start_time = time.perf_counter()
            list_of_lists[i].Insert(size // 2)
            elapsed_time = time.perf_counter() - start_time
            print("Insertion of central value %d: %.6f ms" % ((size //2), elapsed_time))
            
            # Insertion of the data at the tail minus 1.
            val = (list_of_lists[i].tail.data) - 1
            start_time = time.perf_counter()
            list_of_lists[i].Insert(val)
            elapsed_time = time.perf_counter() - start_time
            print("Insertion of integer before tail %d: %.6f ms" % (val, elapsed_time))
            
            # Insertion of the size plus 2.
            start_time = time.perf_counter()
            list_of_lists[i].Insert(size + 2)
            elapsed_time = time.perf_counter() - start_time
            print("Insertion of integer greater than the range %d: %.6f ms\n" % ((size + 2), elapsed_time))
            
            if will_print:
                print("\nAfter: ")
                list_of_lists[i].Print()
                print("\n")
                             
# Performance test for Delete function that calculates the performance time for
# deleting the integral value at the head, tail, and a random integer.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.      
def deletion_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        random_index = random.randint(1,size - 1)
        
        # Performs tests for each list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList:")
            else:
                print("List:")
                
            if will_print:
                print("\nBefore: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Deleting integer of head.
            start_time = time.perf_counter()
            val = list_of_lists[i].head.data
            list_of_lists[i].Delete(val)
            elapsed_time = time.perf_counter() - start_time
            print("Deletion of head integer %d: %.6f ms" % (val, elapsed_time))
            
            # Deleting integer of tail.
            start_time = time.perf_counter()
            val = list_of_lists[i].tail.data
            list_of_lists[i].Delete(val)
            elapsed_time = time.perf_counter() - start_time
            print("Deletion of tail integer %d: %.6f ms" % (val, elapsed_time))
            
            # Deleting a random integer.
            start_time = time.perf_counter()
            list_of_lists[i].Delete(random_index)
            elapsed_time = time.perf_counter() - start_time
            print("Deletion of random integer %d: %.6f ms\n" % (random_index, elapsed_time))
            
            if will_print:
                print("\nAfter: ")
                list_of_lists[i].Print()
                print("\n")
 
# Performance test for Merge function that calculates the performance time for
# merging two lists of the same class.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.        
def merge_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of", size, "elements")
        print("Merging list of", (size // 2), "elements")
        print("________________________________________________________\n")
        
        # Generates lists of the designated size and lists of half the size
        # that will be merged with the original lists.
        list_of_lists = random_linked_list(size)
        list_of_lists_to_merge = random_linked_list(size // 2)
        
        # Performs tests for each original list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
                
            if will_print:
                print("\nBefore: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Merges lists.
            start_time = time.perf_counter()
            list_of_lists[i].Merge(list_of_lists_to_merge[i])
            elapsed_time = time.perf_counter() - start_time
            print("Merge: %.6f ms\n" % elapsed_time)
            
            if will_print:
                print("\nAfter: ")
                list_of_lists[i].Print()
                print("\n")

# Performance test for IndexOf function that calculates the performance time
# for identifying the index of the value at the head, tail, a random integer,
# and an integer out of the list's range.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.        
def index_of_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        random_index = random.randint(1,100)
        
        # Performs tests for every list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
            
            if will_print:
                print("\nCurrent: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Retrieves index of the head's integer.
            start_time = time.perf_counter()
            val = list_of_lists[i].head.data
            index = list_of_lists[i].IndexOf(val)
            elapsed_time = time.perf_counter() - start_time
            print("Index of head, %d: %.6f ms" % (val, elapsed_time))
            print("Index:", index)
            
            # Retrieves index of the tail's integer.
            start_time = time.perf_counter()
            val = list_of_lists[i].tail.data
            index = list_of_lists[i].IndexOf(val)
            elapsed_time = time.perf_counter() - start_time
            print("Index of tail, %d: %.6f ms" % (val, elapsed_time))
            print("Index:", index)
            
            # Retrieves index of a random integer.
            start_time = time.perf_counter()
            index = list_of_lists[i].IndexOf(random_index)
            elapsed_time = time.perf_counter() - start_time
            print("Index of rangdom integer, %d: %.6f ms" % (random_index, elapsed_time))
            print("Index:", index)
            
            # Retrieves index of an integer out of the list's scope.
            start_time = time.perf_counter()
            index = list_of_lists[i].IndexOf(size + 2)
            elapsed_time = time.perf_counter() - start_time
            print("Index of i out of scope, %d: %.6f ms" % (size + 2, elapsed_time))  
            print("Index:", index)
            print()
       
# Performance test for Clear function that calculates the performance time
# for removing all the elements of a designated list.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.
def clear_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        
        # Performs tests for each list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
                
            if willPrint:
                print("\nBefore: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Intiates the list's Clear function.
            start_time = time.perf_counter()
            list_of_lists[i].Clear()
            elapsed_time = time.perf_counter() - start_time
            print("Clear: %.6f ms\n" % (elapsed_time))
            
            if will_print:
                print("\nAfter: ")
                list_of_lists[i].Print()
                print("\n")

# Performance test for Min function that calculates the performance time
# for retrieving the minimimum value of a list.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.
def min_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        
        # Performs tests for every list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
        
            if will_print:
                print("\nCurrent: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Retrieves and displays the minimum value of a list.
            start_time = time.perf_counter()
            min_val = list_of_lists[i].Min()
            elapsed_time = time.perf_counter() - start_time
            print("Minimum value: ", min_val)
            print("Minimum: %.6f ms\n" % (elapsed_time))

# Performance test for Max function that calculates the performance time
# for retrieving the maximum value of a list.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.       
def max_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        
        # Performs tests for every list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
            
            if will_print:
                print("\nCurrent: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Retrieves and displayes the maximum value of the list.
            start_time = time.perf_counter()
            max_val = list_of_lists[i].Max()
            elapsed_time = time.perf_counter() - start_time
            print("Maximum value: ", max_val)
            print("Maximum: %.6f ms\n" % (elapsed_time))

# Performance test for HasDuplicates function that calculates the performance 
# time for determining whether the list has duplicate values.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.         
def has_duplicates_performance_test(size_list, will_print):
    for size in size_list:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        
        # Two lists of SortedList and List are created, in which one list has
        # duplicates and the other does not.
        list_of_lists = random_linked_list(size)
        list_of_no_duplicates = random_non_duplicate_list(size)
        
        # Performs tests for every list generated.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
                
            if will_print:
                print("\nDuplicates:")
                list_of_lists[i].Print()
                print("\n")
                
                print("\nNo Duplicates:")
                list_of_no_duplicates[i].Print()
                print("\n")
            
            # Calculates performance time for a list with duplicates.
            start_time = time.perf_counter()
            hasDuplicates = list_of_lists[i].HasDuplicates()
            elapsed_time = time.perf_counter() - start_time
            print("Has duplicates: ", hasDuplicates)
            print("Has duplicates: %.6f ms" % elapsed_time)
            
            # Calculates performance time for a list without duplicates.
            start_time = time.perf_counter()
            hasDuplicates = list_of_no_duplicates[i].HasDuplicates()
            elapsed_time = time.perf_counter() - start_time
            print("Has duplicates: ", hasDuplicates)
            print("Has duplicates: %.6f ms\n" % elapsed_time)

# Performance test for Select function that calculates the performance 
# time for determining the kth smallest element in a list.
# Input: The size of the lists to be tested and a boolean representing if the
#        the lists will be printed.
# Output: None, only the performance times will be displayed.  
def select_performance_test(sizeList, willPrint):
    for size in sizeList:
        print("________________________________________________________")
        print("Linked list of ", size, "elements")
        print("________________________________________________________\n")
        list_of_lists = random_linked_list(size)
        random_index = random.randint(1, size)
        
        # Performs tests for each list.
        for i in range(len(list_of_lists)):
            if i == 0:
                print("SortedList")
            else:
                print("List")
                
            if willPrint:
                print("\nCurrent: ")
                list_of_lists[i].Print()
                print("\n")
            
            # Initiates the Select function to return the 0th smallest element.
            start_time = time.perf_counter()
            element = list_of_lists[i].Select(0)
            elapsed_time = time.perf_counter() - start_time
            print("kth smallest element, k = 0: ", element)
            print("kth element: %.6f ms" % elapsed_time)
            
            # Initiates the Select function to return the largest element.
            start_time = time.perf_counter()
            element = list_of_lists[i].Select(size - 1)
            elapsed_time = time.perf_counter() - start_time
            print("kth smallest element, k =", size - 1, ":", element)
            print("kth element: %.6f ms" % elapsed_time)
            
            # Initiates the Select function to return a random kth value.
            start_time = time.perf_counter()
            element = list_of_lists[i].Select(random_index)
            elapsed_time = time.perf_counter() - start_time
            print("kth smallest element, k =",  random_index, ":", element)
            print("kth element: %.6f ms\n" % elapsed_time)

# Function that converts a string of integers seperated by spaces to a 
# SortedList and List.
# Input: None
# Output: A list with the elements SortedList and List which were
#         populated by the user.
def str_list_to_linked_list():
    print("Enter a list of number seperated by spaces or press ", end = "")
    print(" enter for an empty linked list.")
    str_list = input("Linked list: ").split(" ")
    list_of_lists = [SortedList(), List()]
    print()
    
    # If the user only pressed enter, a list comprised of an empty
    # SortedList and List is returned.
    if str_list is None:
        return list_of_lists
    
    # Otherwise each list is populated with the data received from the user.
    for i in range(len(str_list)):
        list_of_lists[0].Insert(int(str_list[i]))
        list_of_lists[1].Insert(int(str_list[i]))
    return list_of_lists

# Custom performance test that calculates the performance time of the function
# Print for the SortedList and List passed in list_of_lists.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance time displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.
def custom_print_test(list_of_lists):
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
        
        # Caculates and displays the performance time for Print.
        start_time = time.perf_counter()
        list_of_lists[i].Print()
        elapsed_time = time.perf_counter() - start_time
        print("Linked List Print: %.6f ms\n" % elapsed_time)

# Custom performance test that calculates the performance time of inserting
# a value specified by the user into the SortedList and List.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance time displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.
def custom_insert_test(list_of_lists):
    
    # Receives the integral value that will be added to the lists.
    val = int(input("Enter the value you want to add to the list: "))
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for Insert.
        start_time = time.perf_counter()
        list_of_lists[i].Insert(val)
        elapsed_time = time.perf_counter() - start_time
        print("Linked List Insert: %.6f ms\n" % elapsed_time)

# Custom performance test that calculates the performance time of deleting
# a value specified by the user from the SortedList and List.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance time displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.    
def custom_delete_test(list_of_lists):

    # Receives the integral value that will be removed from the lists.  
    val = int(input("Enter the value you want to delete from the list: "))
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for Delete.
        start_time = time.perf_counter()
        list_of_lists[i].Delete(val)
        elapsed_time = time.perf_counter() - start_time
        print("Linked List Delete: %.6f ms\n" % elapsed_time)

# Custom performance test that calculates the performance time for merging
# a user provided list, with the SortedList and List from list_of_lists.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance time displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.       
def custom_merge_test(list_of_lists):
    
    # Creates the lists to be merged based on the user's input.
    print("Create the second list to merge")
    merge_list_of_lists = str_list_to_linked_list()
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for merging each list from 
        # list_of_lists with a list from mergeListOfLists.
        start_time = time.perf_counter()
        list_of_lists[i].Merge(merge_list_of_lists[i])
        elapsed_time = time.perf_counter() - start_time
        print("Linked List Merge: %.6f ms\n" % elapsed_time)

# Custom performance test that calculates the performance time of identifying
# the index of the user provided value in the SortedList and List.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance times and indeces displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.      
def custom_index_of_test(list_of_lists):
    
    # Receives the integer whose index will be searched for in the lists.
    val = int(input("Enter the value whose index will be returned from the list: "))
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Caculates the performance time for the IndexOf function
        # and displays the index returned.
        start_time = time.perf_counter()
        index = list_of_lists[i].IndexOf(val)
        elapsed_time = time.perf_counter() - start_time
        print("Index:", index)
        print("Index of %d: %.6f ms" % (val, elapsed_time))
    
# Custom performance test that calculates the performance time of removing
# all elements from the SortedList and List.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance times displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.   
def custom_clear_test(list_of_lists):
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for the function Clear.
        start_time = time.perf_counter()
        list_of_lists[i].Clear()
        elapsed_time = time.perf_counter() - start_time
        print("Clear: %.6f ms" % elapsed_time)

# Custom performance test that calculates the performance time of retrieving
# the minimum element in the SortedList and List.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance times and minimum values are 
#         displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.  
def custom_min_test(list_of_lists):
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for the Min function and displays
        # the minimum value returned.
        start_time = time.perf_counter()
        min = list_of_lists[i].Min()
        elapsed_time = time.perf_counter() - start_time
        print("Minimum value:", min)
        print("Minimum: %.6f ms\n" % elapsed_time)
 
# Custom performance test that calculates the performance time of retrieving
# the maximum element in the SortedList and List.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance times and maximum values are 
#         displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.      
def custom_max_test(list_of_lists):
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for the Min function and displays
        # the minimum value returned.
        start_time = time.perf_counter()
        max = list_of_lists[i].Min()
        elapsed_time = time.perf_counter() - start_time
        print("Maximum value:", max)
        print("Maxiumum: %.6f ms\n" %  elapsed_time)
 
# Custom performance test that calculates the performance time of determining
# if the SortedList or List has duplicates.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance times and whether the lists contains
#         duplicates are displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.         
def custom_duplicates_test(list_of_lists):
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
            
        # Calculates the performance time for the HasDuplicates function
        # and displays the boolean value returned.
        start_time = time.perf_counter()
        has_duplicates = list_of_lists[i].HasDuplicates()
        elapsed_time = time.perf_counter() - start_time
        print("Has Duplicates:", has_duplicates)
        print("Has Duplicates: %.6f ms\n" %  elapsed_time)

# Custom performance test that calculates the performance time of returning the
# kth smallest element in the SortedList and List. Assume that valid k values
# start at 0.
# Input: list_of_lists which contains a SortedList at index 0 and a List at
#        index 1.
# Output: None, other than the performance times and the kth smallest element
#         are displayed.
# Assume list_of_lists will always contain a SortedList at index 0 and a List
# at index 1.     
def custom_select_test(list_of_lists):
    
    # Receives the kth value from the user, which will be searched for in the
    # Select function.
    k = int(input("Enter the kth smallest value you want returned: "))
    for i in range(len(list_of_lists)):
        if i == 0:
            print("SortedList")
        else:
            print("List")
        
        # Calculates the performance time for the Select function and displays
        # the kth smallest integer returned.
        start_time = time.perf_counter()
        element = list_of_lists[i].Select(k)
        elapsed_time = time.perf_counter() - start_time
        print("kth smallest element, k = ",  k, ": ", element, sep="")
        print("kth element: %.6f ms\n" % elapsed_time)

# Function that allows users to create their own SortedList and List and
# perform custom tests on each of the possible SortedList and List functions.
# Input: None
# Output: None
def custom_list():
    
    # Initiates the creation of a SortedList and List based on the user's
    # input.
    list_of_lists = str_list_to_linked_list()
    
    # Continues to allow the user to perform the following functions on the
    # SortedList and List until the user enters 11.
    menu_num = 1
    while menu_num > 0 and menu_num < 11:
        
        # Main menu for the custom test framework.
        print("1. Print linked list")
        print("2. Insert value")
        print("3. Delete value")
        print("4. Merge lists")
        print("5. Return the index of a value")
        print("6. Clear the list")
        print("7. Return the minimum value")
        print("8. Return the maximum value")
        print("9. Check if the list has duplicates")
        print("10. Select the kth element")
        print("11. Return to main menu")
        menu_num = int(input("\nSelect 1 - 11: "))
        print()
        
        # Calls the custom test functions based on the user's selection.
        try:
            if menu_num == 1:
                custom_print_test(list_of_lists)
            elif menu_num == 2:
                custom_insert_test(list_of_lists)
            elif menu_num == 3:
                custom_delete_test(list_of_lists)
            elif menu_num == 4:
                custom_merge_test(list_of_lists)
            elif menu_num == 5:
                custom_index_of_test(list_of_lists)
            elif menu_num == 6:
                custom_clear_test(list_of_lists)
            elif menu_num == 7:
                custom_min_test(list_of_lists)
            elif menu_num == 8:
                custom_max_test(list_of_lists)
            elif menu_num == 9:
                custom_duplicates_test(list_of_lists)
            elif menu_num == 10:
                custom_select_test(list_of_lists)
            print()
        
        # Informs the user if an incorrect value was entered.
        except ValueError:
            print("Invalid input. Operation was not performed.")
    
    # Informs the user if an incorrect menu number was entered.
    if menu_num != 11:
        print("Invalid menu number.  Returning to main menu.\n")
    

# Main method for the program that allows users to run automated tests
# on a SortedList and List or perform their own tests on the list's functions.
# Input: None
# Output: None
print("Welcome to Silly Sorts\n")

menu = 0

# As long as the user does not type 3, the program continues.    
while menu != 3:     
    
    print("1. Run automated tests")
    print("2. Create your own linked list")
    print("3. Exit")
    
    try: 
        menu = int(input("\nSelect 1, 2, or 3: "))
        print()
        
        if menu == 1:
            sub_menu = 0
            
            # Allows users to determine which test they want to run.
            while sub_menu < 1 or sub_menu > 11:
                print("1. Print Test")
                print("2. Insert Test")
                print("3. Delete Test")
                print("4. Merge Test")
                print("5. IndexOf Test")
                print("6. Clear Test")
                print("7. Min Test")
                print("8. Max Test")
                print("9. Has Duplicates Test")
                print("10. Select Test")
                sub_menu = int(input("\nSelect 1 to 10: "))
                print()
                
                # Sizes of the SortedList and List that will be tested.
                listSizes = [100, 500, 1000, 2000]
                
                # Determines whether the user wants to have the SortedList
                # and List printed for a specific function in order to see the 
                # changes that occured.
                if sub_menu > 1 and sub_menu < 11:
                    print ("Would you like to:")
                    print("1. Print the lists for each test")
                    print("2. Show performance times only")
                    willPrint = int(input("Select 1 or 2: "))
                    
                    # Assigns willPrint to a corresponding boolean value.
                    if willPrint == 1:
                        willPrint = True
                    elif willPrint == 2:
                        willPrint = False
                    else:
                        
                        # If the user selected an incorrect number, then the 
                        # test ends.
                        print("Invalid selction. Test aborted\n")
                        break
                    
                #  Calls the correct performance test function based
                # on the user's selection..   
                if sub_menu == 1:
                    print_performance_test(listSizes)
                    
                elif sub_menu == 2:
                    insertion_performance_test(listSizes, willPrint)
                    
                elif sub_menu == 3:
                    deletion_performance_test(listSizes, willPrint)
                    
                elif sub_menu == 4:
                    merge_performance_test(listSizes, willPrint)
                
                elif sub_menu == 5:
                    index_of_performance_test(listSizes, willPrint)
                    
                elif sub_menu == 6:
                    clear_performance_test(listSizes, willPrint)
                
                elif sub_menu == 7:
                    min_performance_test(listSizes, willPrint)
                
                elif sub_menu == 8:
                    max_performance_test(listSizes, willPrint)
                
                elif sub_menu == 9:
                    has_duplicates_performance_test(listSizes, willPrint)
                
                elif sub_menu == 10:
                    select_performance_test(listSizes, willPrint)
                    
                # Notifies the user of an incorrect menu selection.
                else:
                    print("Incorrect menu number. Please try again. \n")
        
        # Initiates custom list creation and tests.
        elif menu == 2:
            try:
                custom_list()
            except:
                print("Invalid input. Operation aborted.\n")
        elif menu != 3:
            print("Incorrect menu number. Please try again. \n")
    except ValueError:
        print("Invalid input. Operation aborted \n")