# Course: CS2302 Data Structures
# Date of Last Modification: September 18, 2019
# Assignment: Lab 2 - RuntimeComplexity
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to identify if the number of comparisons
#          and performance time matched the theoretical runtime complexity for
#          each sorting algorithm.  The five sorting methods tested were
#          Bubble Sort, QuickSort, a modified QuickSort, QuickSort with a stack
#          and an iterative, modified QuickSort.  The following program allows
#          the user to run automated tests or their own tests on a given list.

from NicholeMaldonado_activationStack import Stack, Node, Record
import random
import time
import sys

# Part 1

# Outer function for the recurisve Bubble Sort function.
# Input: the list to be sorted and the k, marking the index of the element to
#        be returned.
# Output: The kth element in the list.
# Assume k is a valid index of L and L has a length greater than 0.
def select_bubble(L, k):
    return bubble(L, k, len(L) - 1)
   
# Recurisve Bubble Sort function that continues to swap values that are out
# of order. The recursive call stops once the entire list has been iterated
# through without swapping values or until the list has been iterated
# n^2 times, where n is the length of the list.
# Input: the list to be sorted, k which marks the index of the element to
#        be returned, and the endIndex which divides the list between the
#        unsorted and sorted values.
# Output: The kth element in the list.
def bubble(L, k , endIndex):
    global counter
    
    counter += 1
    
    # Base case that signifies that all elements to the right of the endIndex
    # are in their known sorted location.
    if endIndex == 0:
        return L[k]
    
    # has_swapped is used to dertermine if another recursive call needs to be
    # made.
    has_swapped = False
    
    counter += 1
    
    # Iterates through the range and swaps variables if the element to the left
    # is greater than the element to the right. If a swap occurs, has_swapped
    # is assigned to true.
    for i in range(0, endIndex):
        
        # counter incremented due to iteration and comparisons
        counter += 2
        
        if(L[i + 1] < L[i]):
            L[i + 1], L[i] = L[i], L[i + 1]
            has_swapped = True
            
    # If a swap has occured, the list needs to be reiterated through. The
    # endIndex is decremented because the largest element is now at the end.
    counter += 1
    if has_swapped:
        return bubble(L, k, endIndex - 1)   
     
    return L[k]

# Outer function for the recurisve QuickSort function.
# Input: the list to be sorted and the k, marking the index of the element to
#        be returned.
# Output: The kth element in the list.
# Assume k is a valid index of L and L has a length greater than 0.
def select_quick(L, k):
    quick_sort(L, k, 0, len(L) - 1)
    return L[k]

# Recursive QuickSort function that continues to divide the list based on the 
# value returned from the partition and evalute the resulting sublists.
# Input: the list to be sorted and k which marks the index of the element
#       to be returned.  The low and high index mark the current segment of the
#       list that will be evaluated.
# Output: None.
def quick_sort(L, k, low, high):
    global counter 
    counter += 1
    
    # Base case that stops all recursive calls once the low index is greater
    # than or equal to the high index.
    if low >= high:
        return
    
    middle = partition(L, low, high)

    quick_sort(L, k, low, middle - 1)
    quick_sort(L, k, middle + 1, high)

# Function that selects a pivot from the middle of the list and moves all
# values less than the pivot to the left and all values greater than or equal
# to the pivot to the right.
# Input: the list and low and high index marking the bounds for the section of 
#        the list to be partitioned.
# Output: the index of the pivot now in its correct, ordered place.
def partition(L, low, high):
    global counter

    right = high - 1
    
    # pivot is selected as the middle element and then moved to the right most
    # position.
    middle = low + ((high - low) // 2)
    L[middle], L[high] = L[high], L[middle]
    pivot = L[high]
    
    # Continues to partition the list based on the pivot value until the 
    # low value is greater than the right value.
    counter += 1
    while low <= right: 
        counter += 3
        
        while L[low] < pivot:
            counter += 1
            low += 1
            
        while L[right] > pivot:
            counter += 1
            right -= 1
        
        # Swaps values to the correct side of the partition.
        if low <= right:
            L[low], L[right] = L[right], L[low]
            low += 1
            right -= 1
            
        counter += 1
        
    # Places the pivot in its correct, sorted poisition in the list.
    L[low], L[high] = L[high], L[low]
    return low

# Outer function for the recurisve modified QuickSort function.
# Input: the list to be sorted and k which marks the index of the element to
#        be returned.
# Output: The kth element in the list.  
# Assume k is a valid index of L and L has a length greater than 0.
def select_modified_quick(L, k):
    return modified_quick(L, k, 0, len(L) - 1)

# Recursive function for the modified QuickSort.  This version of QuickSort
# only makes recursive calls to segments of the list where the kth element
# is located.  Thus, it is not guaranteed that the entire list will be sorted.
# Input: the list to be sorted and k which marks the index of the element
#        to be returned.  The low and high index mark the segment of the list
#        that will be evaluated.
# Output: The kth element in the list.
def modified_quick(L, k, low, high):
    middle = partition(L, low, high)
 
    global counter
    counter += 1
    
    # Base case in which the value returned from partition is the kth element.
    if k == middle:
        return L[middle]
    
    # If k is less than the value returned, then a recursive call is made on 
    # the left sublist.
    counter += 1
    if k < middle:
       return modified_quick(L, k, low, middle - 1)
   
    # Otherwise a recursive call is made on the right sublist.
    return modified_quick(L, k, middle + 1, high)

# Part 2

# Function that implements QuickSort using a stack rather than recursion. 
# Record objects are pushed to the stack to represent recursive calls
# to be made and their low or high attribute is based on the index returned
# from partition.
# Input: the list to be sorted and the k which marks the index of the element
#        to be returned.
# Output: The kth element in the list. 
# Assume k is a valid index of L and L has a length greater than 0.           
def quick_sort_with_stack(L, k):
    global counter
    
    # First QuickSort call is pushed to the stack.
    quicksort_record = Record(0, len(L) - 1)
    stack = Stack(Node(quicksort_record))
    
    # Continues to iterate until all activation records are removed from the
    # stack.
    counter += 1
    while not stack.isEmpty():
        
        # counter is incremeted for the loop iteration and peek.
        counter += 2
        curr_record = stack.peek()

        # Removes the activation record if low is greater than or equal to high.
        if curr_record.low >= curr_record.high:
            
            # Popping has 2 comparisons.
            counter += 2
            stack.pop()
        else:
            middle = partition(L, curr_record.low, curr_record.high)
            
            # curr_record is finished since the two recursive calls will be
            # pushed to the stack.
            counter += 2
            stack.pop()
            
            # Pushes the QuickSort recursive call, that analyzes the right 
            # sub-list, to the stack.
            counter += 1
            quicksort_record = Record(middle + 1, curr_record.high)
            stack.push(quicksort_record)
            
            # Pushes the QuickSort recursive call, that analyzes the left 
            # sub-list, to the stack.
            counter += 1
            quicksort_record = Record(curr_record.low, middle - 1)
            stack.push(quicksort_record)
            
        counter += 1
            
    return L[k] 

# Iterative implementation for the the modified QuickSort function.  
# This version of QuickSort repeatedly evaluates the new segment of the list
# where the kth element can be found, based on the partition. Thus, it is not 
# guaranteed that the entire list will be sorted.
# Input: the list to be sorted and the k which marks the index of the element
#        to be returned.
# Output: The kth element in the list.
# Assume k is a valid index of L and L has a length greater than 0.
def iterative_select_modified_quick(L, k):
    global counter
    low = 0
    high = len(L) - 1
    middle = partition(L, low, high)
    
    counter += 1
    
    # The left or right sublist will continue to be partitioned and evaluated
    # until the value returned from the partition is the kth element.
    while k != middle:
        counter += 1
        
        # Left sublist is evaluated if k is less than middle.
        if k < middle:
            high = middle - 1
            middle = partition(L, low, high)
            
        # Right sublist is evaluated if k is greater than the middle.
        else:
            low = middle + 1
            middle = partition(L, low, high)
            
        counter += 1
        
    return L[middle]  

# Function that generates copies of the list passed in.
# Input: the list that will be copied.
# Output: a list of 5 copies of the list passed in.
# Assume that only 5 copies of the list will be made.
def generate_list_copies(list):
    list_of_lists = []
    for x in range(5):
        list_of_lists.append(list[:])
        
    return list_of_lists

# Function that generates a random list of a given size.
# Input: the size of the random list to be generated.
# Output: a random list of integers of length size.
def random_list_generation(size):
    list = []
    for x in range(size):
        list.append(random.randint(0, 101))
        
    return generate_list_copies(list)

# Function that generates a sorted list of a given size.
# Input: the size of the sorted list to be generated.
# Output: a sorted list of integers of length size.
def sorted_list_generation(size):
    list = []
    for x in range(size):
        list.append(x)
                
    return generate_list_copies(list)

# Function that generates a nearly sorted list of a give size.
# Input: the size of the nearly sorted list to be generated.
# Output: a nearly sorted list of integers of length size.  A fourth of the
#         list will contain elements out of order.
def nearly_sorted_list_generation(size):
    list = []
    for x in range(size):
        list.append(x)
    
    # A fourth of the list will have random integers out of order.
    for x in range(size // 4):
        list[random.randint(0, size - 1)] = random.randint(0, 101)
        
    return generate_list_copies(list)

# Function that calculates the perfomance time for QuickSort, Bubble Sort, 
# modified QuickSort, QuickSort with a stack, and the iterative modified 
# QuickSort. The function also displays the kth element returned and the 
# the number of comparisons made by each function.
# Input: the list_of_lists which contains 5 copies of the same list and k
#        which marks the kth element to be returned.
# Output: None other than the performance time, number of comparisons, and
#         element returned from each function described above.
# Assume that the list_of_lists contains 5 valid lists that will be passed
# to the sorting functions. Also assume k is in the valid range of the lists.
def performance_tests(list_of_lists, k):
    global counter
    
    # Bubble Sort test.
    counter = 0
    start_time = time.perf_counter()
    element = select_bubble(list_of_lists[0], k)
    elapsed_time = time.perf_counter() - start_time
    
    
    print("Bubble Sort: %.6f ms" % elapsed_time)
    print("  Element returned:", element)
    print("  Number of Comparisons:", counter)
    counter = 0
    
    # QuickSort test.
    start_time = time.perf_counter()
    element = select_quick(list_of_lists[1], k)
    elapsed_time = time.perf_counter() - start_time
    
    print("QuickSort: %.6f ms" % elapsed_time)
    print("  Element returned:", element)
    print("  Number of Comparisons:", counter)
    counter = 0
    
    # Modified QuickSort test.
    start_time = time.perf_counter()
    element = select_modified_quick(list_of_lists[2], k)
    elapsed_time = time.perf_counter() - start_time
    
    print("Modified QuickSort: %.6f ms" % elapsed_time)
    print("  Element returned:", element)
    print("  Number of Comparisons:", counter)
    counter = 0
    
    # QuickSort with a stack test.
    start_time = time.perf_counter()
    element = quick_sort_with_stack(list_of_lists[3], k)
    elapsed_time = time.perf_counter() - start_time
    
    print("QuickSort with Stack: %.6f ms" % elapsed_time)
    print("  Element returned:", element)
    print("  Number of Comparisons:", counter)
    counter = 0
    
    # Iterative modified QuickSort test.
    start_time = time.perf_counter()
    element = iterative_select_modified_quick(list_of_lists[4], k)
    elapsed_time = time.perf_counter() - start_time
    
    print("Iterative Modified QuickSort: %.6f ms" % elapsed_time)
    print("  Element returned:", element)
    print("  Number of Comparisons:", counter, "\n")
    counter = 0
    
# Function that prints the lists from list_of_lists.
# Input: the list_of_lists which contains 5 copies of the same list that have 
#        been sorted by BubbleSort, QuickSort, the modified QuickSort, the 
#        QuickSort with a stack, and the iterative modified QuickSort.
# Output: None, other than the lists printed.   
def print_sorted_lists(list_of_lists):
    print("Bubble Sort:")
    print(list_of_lists[0])
    
    print("QuickSort:")
    print(list_of_lists[1])
    
    print("Modified QuickSort:")
    print(list_of_lists[2])
    
    print("QuickSort with Stack:")
    print(list_of_lists[3])
    
    print("Iterative Modified QuickSort:")
    print(list_of_lists[4])
    print()

# Function that initiates tests to be run on lists of length size that will 
# be sorted by QuickSort, Bubble Sort, Modified QuickSort, iterative modified
# QuickSort, and QuickSort with a stack.
# Input: the size of the lists that will be made and tested.
# Output: None
# Assume that the size is a valid integer greater than or equal to 0.  
def test_framework(size):
    menu = 0
    
    # Allows users to determine whether they want to print each list after
    # the lists have been sorted by the functions.
    while menu != 1 and menu != 2:
        print("1. Display the lists and performance time for every function.")
        print("2. Only display performance time and number of comparisons.")
        menu = int(input("Select 1 or 2: "))
        print()
        
        if menu == 1:
            print_list = True
        elif menu == 2:
            print_list = False
        else:
            print("Invalid menu number. Please try again\n")
    
    # Initiates a total of 9 performance tests. Three for sorted, unsorted, and
    # nearly sorted lists, with k ranging from 0, the index of the middle
    # element, and the index of the last element.
    for k in [0, (size // 2) - 1, size - 1]:
        # Generates random lists.
        list_of_lists = random_list_generation(size)
        print("___________________________________________________________")
        print("Unsorted lists  with k = ", k, ":")
        print("___________________________________________________________\n")
        if print_list:
            print("List to be sorted:", list_of_lists[0], "\n")
        
        # Runs performance tests.
        performance_tests(list_of_lists, k)
        
        # Prints lists based on user's request.
        if print_list:
            print_sorted_lists(list_of_lists)
        
        # Generates nearly sorted lists.
        list_of_lists = nearly_sorted_list_generation(size)
        print("___________________________________________________________")
        print("Nearly sorted lists with k =", k, ":")
        print("___________________________________________________________\n")
        if print_list:
            print("List to be sorted:", list_of_lists[0], "\n")
            
        # Runs performance tests.
        performance_tests(list_of_lists, k)
        
        # Prints lists based on user's request.
        if print_list:
            print_sorted_lists(list_of_lists)
        
        # Generates sorted lists.
        list_of_lists = sorted_list_generation(size)
        print("___________________________________________________________")
        print("Sorted lists with k = ", k, ":")
        print("___________________________________________________________\n")
        if print_list:
            print("List to be sorted:", list_of_lists[0], "\n")
        
        # Runs performance tests.
        performance_tests(list_of_lists, k)
        
        # Prints lists based on user's request.
        if print_list:
            print_sorted_lists(list_of_lists)

# Function that allows users to enter their own list to be sorted by Bubble
# Sort, QuickSort, modified QuickSort, iterative modified QuickSort, and 
# QuickSort with a stack.  User also signifies which kth element they want
# returned.
# Input: None
# Output: None
def custom_test():
    
    # Allows user to enter the list and k value.
    str_list = input("Enter a list of numbers seperated by spaces: ").split()
    
    if len(str_list) <= 0:
        print("Invalid list. Test aborted\n")
        return 
    
    list = [int(x) for x in str_list]
    k = int(input("What kth value would you like to return: "))
    
    if k < 0 or k > len(list) - 1:
        print("Invalid k. Test aborted\n")
        return    
    
    menu = 0
    
    # Allows user to select their perferences for the list.
    while menu != 1 and menu != 2:
        print("1. Display the lists and performance time for every method.")
        print("2. Only display performance time and number of comparisons.")
        menu = int(input("Select 1 or 2: "))
        print()
        
        if menu == 1:
            print_list = True
        elif menu == 2:
            print_list = False
        else:
            print("Invalid menu number.\n")
    
    # Makes copies of the user provided lists and initiates the performance
    # test.
    list_of_lists = generate_list_copies(list)
    performance_tests(list_of_lists, k)
    
    # Prints lists based on the user's request.
    if print_list:
        print_sorted_lists(list_of_lists)
        
# Main function that allows user to determine whether they want to run 
# automated tests for the Bubble Sort, QuickSort, modified QuickSort,
# iterative modified QuickSort, and QuickSort with a stack, or run their
# own test.
# Input: None
# Output: None
counter = 0   
menu = 1 
sys.setrecursionlimit(4000)

# As long as the user does not type 3, the program continues.    
while menu != 3:     
    
    print("1. Run automated tests")
    print("2. Create your own test")
    print("3. Exit")
    
    try: 
        menu = int(input("\nSelect 1, 2, or 3: "))
        print()
        
        if menu == 1:
            sub_menu = 0
            
            # Allows users to determine which test they want to run.
            while sub_menu < 1 or sub_menu > 5:
                print("1. Run small tests (100 elements)")
                print("2. Run average tests (500 elements)")
                print("3. Run medium tests (1000 elements)")
                print("4. Run large tests (2000 elements)")
                print("5. Run extra large tests (3000 elements)")
                sub_menu = int(input("\nSelect 1, 2, 3, 4, or 5: "))
                print()
                
                # Run tests on 100 element list
                if sub_menu == 1:
                    test_framework(100)
                
                # Run tests on 500 element list
                elif sub_menu == 2:
                    test_framework(500)
                
                # Run tests on 500 element list
                elif sub_menu == 3:
                    test_framework(1000)
                    
                # Run tests on 2000 element list
                elif sub_menu == 4:
                    test_framework(2000)
                 # Run tests on 3000 element list
                elif sub_menu == 5:
                    test_framework(3000)
                    
                # Notify user of incorrect menu selection.
                else:
                    print("Incorrect menu number. Please try again. \n")
        
        # Initiates custom tests.
        elif menu == 2:
            try:
                custom_test()
            except:
                print("Invalid input. Test aborted.\n")
        elif menu != 3:
            print("Incorrect menu number. Please try again. \n")
    except ValueError:
        print("Incorrect menu number. Please try again. \n")
