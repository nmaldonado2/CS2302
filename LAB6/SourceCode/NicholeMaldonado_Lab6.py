# Course: CS2302 Data Structures
# Date of Last Modification: November 14, 2019
# Assignment: Lab 6 - Graphs
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to represent graphs through adjacency
#          lists, adjacency matrices, and edge lists. These grahical
#          representations were then used to solve the riddle concerning a fox,
#          chicken, sack of grain, and person by using breadth first search and
#          depth first search.  This program allows the users to create their
#          own custom graph, solve the riddle, run the tests provided by the
#          instructor, and run automated tests.  These tests compare the runtime
#          between the different graphs' operations.

import graph_AL as al
import graph_AM as am
import graph_EL as el
import test_graphs as tg
import HashTable as ht
import random
import time
import sys

# Function that creates the graph for the fox, chicken, grain, person riddle.
# Input: The menu selection that determines the graph type.  If menu equals 1,
#        then an adjacency list is created.  If menu equals 2, an adjacency 
#        matrix is created.  If the menu equals three, an edge list is created.
# Output: The created graph.
# Assume menu is an integer that is either 1, 2, or 3.
def create_graph(menu):
    if menu == 1:
        graph = al.Graph(16)
    elif menu == 2:
        graph = am.Graph(16)
    else:
        graph = el.Graph(16)
    graph.insert_edge(0,5)
    graph.insert_edge(2,7)
    graph.insert_edge(2,11)
    graph.insert_edge(4,5)
    graph.insert_edge(4,7)
    graph.insert_edge(4,13)
    graph.insert_edge(8,11)
    graph.insert_edge(8,13)
    graph.insert_edge(10,11)
    graph.insert_edge(10,15)
    
    return graph

# Converts a path of integers into a set by adding pairs, that represent
# edges to the set.
# Input: A list of integers that represents a path between vertices.
# Output: A set with the edges of the path.
def path_to_set(path):
    set_of_edges = set()
    for i in range(len(path) - 1):
        set_of_edges.add((path[i], path[i + 1]))
    if len(path) == 1:
        set_of_edges.add((path[0], path[0]))
    return set_of_edges

# Function that returns the graph type based on the graph representation.
# Input: A string of characters that is either "AL", "AM", or "EL".
# Output: A string of the graph type based on the graph's representation.
def representation_to_text(representation):
    if representation == "AL":
        return "Adjacency List"
    if representation == "EL":
        return "Edge List"
    return "Adjacency Matrix"

# Function that displays the graphs and prints the graph if designated by the
# boolean draw_graph.
# Input: The graph to be displayed and a boolean that signifies if the graph
#        fwill be drawn
# Output: None, other than the graph will be displayed and potentially drawn.
def display_graph(graph, draw_graph):
    graph_type = representation_to_text(graph.representation)
    print(graph_type, ":")
    graph.display()
    print()
    if draw_graph:
        print("Graph based on the", graph_type, end = " ")
        print("will be stored in the current directory.\n")
        graph.draw()
        print()

# Function that prints the beginning or ending of the riddle.
# Input: A string, move, that is either "0000" or "1111". If the move is "0000",
#        the start is printed.  Otherwise, the end of the riddle is printed.
# Output: None
def print_start_end(move):
    if move == "0000":
        print("The person, fox, chicken, and grain start on the left side of the river.\n")
    else:
        print("The person, fox, chicken, and grain end on the right side of the river.")
 
# Function that prints all the characters in a list.
# Input: A list that contains a string of characters from the riddle that will
#        be printed to the screen.
# Output: None
def print_characters(characters):
    print("The", end = " ")
    for i in range(len(characters)):
        print(characters[i], end = "")
        
        # Prints the appropriate punctuation based on the current word's position
        # in the sentence.
        if i == len(characters) - 1:
            print(end = " ")
        else:
            if len(characters) > 2:
                print(end = ", ")
                if i == len(characters) - 2:
                    print("and ", end = "")
            else:
                print(end = " and ")

# Function that prints the side of the river.
# Input: The direction that signifies which side of the river needs to be printed.
#        If the direction is one, then right side is printed.  Otherwise left
#        side is printed.
# Output: None
# Assume that direction is an integer that is either 1 or 2.
def print_direction(direction):
    if direction == 1:
        print("right side of the river.")
    else:
        print("left side of the river.")

# Function that will print the current characters and where they move with
# reference to the river.
# Input: A list of characters and a interger representing which side of the 
#        the river the characters will move to.
# Output: None
# Assume that direction is an integer that is either 1 or 2.
def print_move(characters, direction):
    print_characters(characters)
    if len(characters) == 1:
        print("moves to the", end = " ")
    else:
        print("move to the", end = " ")
    print_direction(direction)

# Function that will print the current characters and where they will stay with
# reference to the river.
# Input: A list of characters and a interger representing which side of the 
#        the river the characters will stay on.
# Output: None
# Assume that direction is an integer that is either 1 or 2.
def print_stayed(characters, direction):
    print_characters(characters)
    if len(characters) == 1:
        print("stays on the", end = " ")
    else:
        print("stay on the", end = " ")
    
    print_direction(direction)

# Function that will add characters to the corresponding list to be processed 
# based on the current and past move.
# Input: Two string with 4 binary bits that represent the moves for the riddle.
# Output: None.
def different_moves(individual_move, move_before):
    char_who_moved_left = []
    char_who_moved_right = []
    char_who_stayed_left = []
    char_who_stayed_right = []

    for i in range(len(individual_move)):
        
        # If a character did moved, then they are added to the corresponding list.
        if individual_move[i] != move_before[i]:
            if individual_move[i] == "0":
                if i == 0:
                    char_who_moved_left.append("fox")
                elif i == 1:
                    char_who_moved_left.append("chicken")
                elif i == 2:
                    char_who_moved_left.append("grain")
                else:
                    char_who_moved_left.append("person")                
            else:
                if i == 0:
                    char_who_moved_right.append("fox")
                elif i == 1:
                    char_who_moved_right.append("chicken")
                elif i == 2:
                    char_who_moved_right.append("grain")
                else:
                    char_who_moved_right.append("person")
        
        # Otherwise, the characters are added to the corresponding 
        # char_who_stayed list.
        else:
            if individual_move[i] == "0":
                if i == 0:
                    char_who_stayed_left.append("fox")
                elif i == 1:
                    char_who_stayed_left.append("chicken")
                elif i == 2:
                    char_who_stayed_left.append("grain")
                else:
                    char_who_stayed_left.append("person")  
            else:
                if i == 0:
                    char_who_stayed_right.append("fox")
                elif i == 1:
                    char_who_stayed_right.append("chicken")
                elif i == 2:
                    char_who_stayed_right.append("grain")
                else:
                    char_who_stayed_right.append("person")
                    
    # Each list of characters will then be printed as long as one character
    # is in the list.
    if len(char_who_moved_left) > 0:              
        print_move(char_who_moved_left, 0)

    if len(char_who_moved_right) > 0:  
        print_move(char_who_moved_right, 1)
    
    if len(char_who_stayed_left) > 0:
        print_stayed(char_who_stayed_left, 0)
        
    if len(char_who_stayed_right) > 0:
        print_stayed(char_who_stayed_right, 1)
    print()

# Function that compares the current and past move and determines which
# functions to call to print the results.
# Input: Two strings of binary inputs with 4 bits each that specify the current
#        individual move and the past move.
# Output: None
def interpret_move(individual_move, move_before, start):
    if start and move_before == "0000":
        print_start_end(move_before)
        different_moves(individual_move, move_before)
    elif individual_move == "1111":
        print_start_end(individual_move)
    else:
        different_moves(individual_move, move_before)

# Function that will traverse the entire path and call the correseponding
# functions to interpret each line.
# Input: A path of integers to be interpreted.
# Output: None   
def interpret_solutions(valid_path):
    print("Path: ", valid_path)
    print("\nSolution:")
    for i in range(1, len(valid_path)):
        is_start = False
        if i == 1:
            is_start = True
        interpret_move("{0:04b}".format(valid_path[i]), "{0:04b}".format(valid_path[i - 1]), is_start)
    print()

# Function that will initiate the breadth first search or depth first search
# algorithm to solve the riddle. The function then causes the resulting graph
# to be drawn.
# Input: The graph type for the graph to be created and a integer that determines
#        which searching algorithm will be used.  If the search_alg_type is one
#        then breadth first search is called.  Otherwise DFS is called.
# Output: None 
# Assume that the graph_type is the integer 1, 2, or 3, which represent the
# adjacency list, matrix, and edge list.  Also assume the search_alg_type will
# either be equal to one or two.
def graph_configuration(graph_type, searching_alg_type):
    graph = create_graph(graph_type)
    display_graph(graph, True)
    
    # Solves riddle by breadth first search.
    if searching_alg_type == 1:
        start_time = time.perf_counter()
        path = graph.breadth_first_search(0, 15)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds\n"%(end_time - start_time))
        interpret_solutions(path)
        
    # Solves riddle by depth first search.
    else:
        start_time = time.perf_counter()
        path = graph.depth_first_search(0, 15)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds\n"%(end_time - start_time))
        interpret_solutions(path)
    if not path is None:
        print("The discovered path will be saved to the current directory.")
        set_of_edges = path_to_set(path)
        graph.draw_path(set_of_edges)

# Function that allows users to select the graph implementation.
# Input: None
# Output: The menu number based on the user's selection.  If the menu is one,
#          adjacency list is selected.  If two is selected, the matrix is selected.
#          If three is chosen,  the edge list is selected.
def select_graph_types():
    print("Choose your graph implementation")
    print("1. Adjacency List")
    print("2. Adjacency Matrix")
    print("3. Edge List")
    menu = int(input("Select 1, 2, or 3: "))
    print()
    return menu

# Main sub-menu for the riddle selection that allows users to select the algorithm
# type.  More functions are then called to create the graphs and perform the
# searches.
# Input: None
# Output: None
def riddle_menu_selection():
    menu = select_graph_types()
    if menu >= 1 and menu <= 3:
        print("Choose the search algorithm")
        print("1. Breadth First Search")
        print("2. Depth First Search")
        searching_alg_type = int(input("Select 1 or 2: "))
        
        if searching_alg_type >= 1 and searching_alg_type <= 2:
            graph_configuration(menu, searching_alg_type)
        else:
            print("Invalid menu number. Program terminating.")
    else:
        print("Invalid menu number. Program terminating.")
 
# Runs the tests from test_graphs.py and allows the user to select which graph
# type to use.
# Input: None
# Output: None.
def run_test_graphs():
    menu = select_graph_types()
    if menu >= 1 and menu <= 3:
        
        # If menu == 1, then an adjacency list is used.
        if menu == 1:
            graph_of_graphs = [
                al.Graph(6),
                al.Graph(6, directed = True),
                al.Graph(6, weighted = True),
                al.Graph(6, weighted = True, directed = True)
                ]
        
        # If menu == 2, then an adjacency matrix is used.
        elif menu == 2:
            graph_of_graphs = [
                am.Graph(6),
                am.Graph(6, directed = True),
                am.Graph(6, weighted = True),
                am.Graph(6, weighted = True, directed = True)
                ]
            
        # If menu == 3, then an edge list is used.
        else:
            graph_of_graphs = [
                el.Graph(6),
                el.Graph(6, directed = True),
                el.Graph(6, weighted = True),
                el.Graph(6, weighted = True, directed = True)
                ]
            
        # Runs tests
        tg.run_tests(graph_of_graphs)
    else:
        print("Invalid menu number. Program terminating.")

# Creates a hash table with edge combinations based on the number of edges
# needed. Each edge's source vertex will be hashed based on the vertex number.
# Only non-duplicate edges are hashed to the table.
# Input: The number of vertices the graph will have and the number of edges
#        that need to be hashed to the table.
# Output: A list of the hash table with linear chaining's buckets.
def compute_edge_combos(num_vertices, num_edges):
    edges = ht.HashTableChain(num_vertices)
    i = 0
    while i != num_edges:
        
        # Creates random vertices and weights.
        vertex_one = random.randint(0,num_vertices - 1)
        vertex_two = random.randint(0, num_vertices - 1)
        weight = random.randint(1,99)
        
        # Hashes the edge to the table. If the insertion is successful, then
        # i is incremented.
        if vertex_one != vertex_two:
            if edges.insert([vertex_one, vertex_two, weight]) != -1:
                i += 1
    return edges.bucket

# Function that allows for a list containing graphs to be displayed.
# Input: A 1D list that contains the graphs that will be displayed.
# Output: None.
def display_all_graphs(list_of_graphs):
    for graph in list_of_graphs:
        display_graph(graph, False)

# Function that tests the insert_edge for the adjacency list, adjacency matrix,
# and edge list graphs.
# Input: A list of graphs that will be populated with the edges from edge_combos.
#        edge_combos is a 2D list, that contains (source, destination, weight)
#        edges in the buckets.
# Output: None, other than the runtime is displayed.
def insert_test(list_of_graphs, edge_combos):
    
    # Populates each graph in list_of_graphs with the edges in edge_combos.
    for i in range(len(list_of_graphs)):
        print("Insertion for ", representation_to_text(list_of_graphs[i].representation))
        
        # Iterates through each bucket and inserts the edges into the graph.
        start_time = time.perf_counter()
        for bucket in edge_combos:
            for edge_pair in bucket:
                
                # If the graph is weighted, then the corresponding weight is 
                # included.
                if list_of_graphs[i].weighted:
                        list_of_graphs[i].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                        
                # Otherwise the defualt weight will be 1.
                else:
                    list_of_graphs[i].insert_edge(edge_pair[0], edge_pair[1])
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds\n"%(end_time - start_time))

# Function that tests the graph conversions to an adjacency list, adjacency 
# matrix, and edge list.
# Input: A list_of_graphs that contains the graphs that will be converted to the
#       other graph types and a boolean value, print_graphs, which will
#       determine whether the graphs will be printed.
# Output: None, other than the runtimes and graphs are displayed.
def different_representations_test(list_of_graphs, print_graphs):     
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        
        # Runs test for conversion to an adjacency list.
        print(graph_type, "to Adjacency List:")
        start_time = time.perf_counter()
        g = graph.as_AL()
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        if print_graphs:
            print("New ",end = "")
            display_graph(g, False)
        else:
            print()
        
        # Runs test for conversion to an adjacency matrix.
        print(graph_type, "to Adjacency Matrix:")
        start_time = time.perf_counter()
        g = graph.as_AM()
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        if print_graphs:
            print("New ",end = "")
            display_graph(g, False)
        else:
            print()
        
        # Runs test for conversion to an edge list.
        print(graph_type, "to Edge List:")
        start_time = time.perf_counter()
        g = graph.as_EL()
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_graphs:
            print("New ",end = "")
            display_graph(g, False)
        else:
            print()
        print("----------")

# Function that tests the depth first search method that finds a valid path
# from the start_vertex to end_vertex.
# Input: A list_of_graphs that contains the graphs that will conduct depth first
#        search.  The start_vertex and end_vertex determine where the search
#        will start and terminate. The boolean print_paths determine whether 
#        the paths will be printed. The boolean small_graph determines if the
#        path will be drawn (For lab demos only and graphs with 10 vertices).
# Output: None, other than the runtimes and graphs are displayed.
# Assume that start_vertex and end_vertex are integers.
def dfs_test(list_of_graphs, start_vertex, end_vertex, print_paths, small_graph):
    
    # Runs the tests for depth first search for each graph.
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        print(graph_type, ":")
        start_time = time.perf_counter()
        path = graph.depth_first_search(start_vertex, end_vertex)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_paths:
            print("Path: ", path, "\n")
            if small_graph and not path is None:
                graph.draw_path(path_to_set(path))
        else:
            print()

# Function that tests the breadth first search method that finds a valid path
# from the start_vertex to end_vertex.
# Input: A list_of_graphs that contains the graphs that will conduct breadth first
#        search.  The start_vertex and end_vertex determine where the search
#        will start and terminate. The boolean print_paths determine whether 
#        the paths will be printed. The boolean small_graph determines if the
#        path will be drawn (For lab demos only and graphs with 10 vertices).
# Output: None, other than the runtimes and graphs are displayed.
# Assume that start_vertex and end_vertex are integers.      
def bfs_test(list_of_graphs, start_vertex, end_vertex, print_paths, small_graph):
    
    # Runs the tests for breadth first search for each graph.
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        print(graph_type, ":")
        start_time = time.perf_counter()
        path = graph.breadth_first_search(start_vertex, end_vertex)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_paths:
            print("Path: ", path, "\n")
            if small_graph and not path is None:
                graph.draw_path(path_to_set(path))
        else:
            print()

# Function that tests the delete_edge for the adjacency list, adjacency matrix,
# and edge list graphs.
# Input: A list of graphs that whose edges will be deleted.
#        edge_combos is a 2D list, that contains (source, destination, weight)
#        edges in the buckets. edge_combos contains all the edges in the graphs.
# Output: None, other than the runtime is displayed.            
def delete_test(list_of_graphs, edge_combos, print_graphs):
    
    # Deletes all the edges from the graphs found in edge_combos.
    for i in range(len(list_of_graphs)):  
        print("Deletion for ", representation_to_text(list_of_graphs[i].representation))
        start_time = time.perf_counter()
        for bucket in edge_combos:
            for edge_pair in bucket:
                    list_of_graphs[i].delete_edge(edge_pair[0], edge_pair[1])
        end_time = time.perf_counter()
        
        if print_graphs:
            print("After deletion,", end = " ")
            display_graph(list_of_graphs[i], False)
        print("Runtime: %0.6f seconds\n"%(end_time - start_time))

# Function that tests the display furnction for the adjacency list, adjacency 
# matrix, and edge list graphs.
# Input: A list of graphs that will be displayed.
# Output: None, other than the runtime is displayed.        
def display_test(list_of_graphs):
    
    # Displays graphs.
    for graph in list_of_graphs:  
        print("Display for ", representation_to_text(graph.representation))
        start_time = time.perf_counter()
        graph.display()
        end_time = time.perf_counter()

        print("Runtime: %0.6f seconds\n"%(end_time - start_time))
        
# Function that tests the display furnction for the adjacency list, adjacency 
# matrix, and edge list graphs.
# Input: A list of graphs that will be displayed.
# Output: None, other than the runtime is displayed.        
def draw_test(list_of_graphs):
    print("All graph drawings will be stored in the current directory.")
    
    # Draws graphs.
    for graph in list_of_graphs:  
        print("Drawing for ", representation_to_text(graph.representation))
        start_time = time.perf_counter()
        graph.draw()
        end_time = time.perf_counter()

        print("Runtime: %0.6f seconds\n"%(end_time - start_time))

# Function that initiates the tests for the graphs' edge insertions.
# Input: The size of graphs to be created and a boolean that determines whether
#        the graphs will be printed.
# Output: None
def run_automated_insertion(graph_size, print_graphs):
    
    # Creates graphs that will be populated with edges from edge_combos.
    list_of_graphs, edge_combos = generate_test_graphs(graph_size, 1)
    
    # Runs tests for undirected graphs.
    print("\nUndirected Insertion")
    print("________________________________________________")
    insert_test(list_of_graphs[0], edge_combos)
    if print_graphs:
        display_all_graphs(list_of_graphs[0])
    
    # Runs tests for directed graphs.
    print("\nDirected Insertion")
    print("________________________________________________")
    insert_test(list_of_graphs[1], edge_combos)
    if print_graphs:
        display_all_graphs(list_of_graphs[1])
    
    # Runs tests for weighted graphs.
    print("\nWeighted Insertion")
    print("________________________________________________")
    insert_test(list_of_graphs[2], edge_combos)
    if print_graphs:
        display_all_graphs(list_of_graphs[2])
    
    # Runs tests for weighted, directed graphs.
    print("\nWeighted and Directed Insertion")
    print("________________________________________________")
    insert_test(list_of_graphs[3], edge_combos)
    if print_graphs:
        display_all_graphs(list_of_graphs[3])

# Function that initiates the tests for the graphs' conversions to different
# graphical representations.
# Input: The size of graphs to be created and a boolean that determines whether
#        the graphs will be printed.
# Output: None    
def run_automated_diff_rep(graph_size, print_graphs):
    
    # Creates the list of graphs to be converted.
    list_of_graphs = generate_test_graphs(graph_size, 3)
    
    # Runs tests for undirected graphs.
    if print_graphs:
        print("Graphs to be modeled after:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    print("\nUndirected Different Graph Representations")
    print("________________________________________________")
    different_representations_test(list_of_graphs[0], print_graphs)
    
    # Runs tests for directed graphs.
    if print_graphs:
        print("Graphs to be modeled after:",end = "\n")
        display_all_graphs(list_of_graphs[1])
    print("\nDirected Different Graphical Representations")
    print("________________________________________________")
    different_representations_test(list_of_graphs[1], print_graphs)
    
    # Runs tests for weighted graphs.
    if print_graphs:
        print("Graphs to be modeled after:",end = "\n")
        display_all_graphs(list_of_graphs[2])
    print("\nWeighted Different Graph Representations")
    print("________________________________________________")
    different_representations_test(list_of_graphs[2], print_graphs)
     
    # Runs tests for weighted, directed graphs.
    if print_graphs:
        print("Graphs to be modeled after:",end = "\n")
        display_all_graphs(list_of_graphs[3])
    print("\nWeighted and Directed Different Graphical Representations")
    print("________________________________________________")
    different_representations_test(list_of_graphs[3], print_graphs)

# Function that initiates the tests for depth first search.
# Input: The size of graphs to be created and a boolean that determines whether
#        the graphs will be printed. The boolean small_graph_selection is only
#        for lab demos to draw the graphs with 10 vertices.
# Output: None        
def run_automated_dfs(graph_size, print_graphs, small_graph_selection):
    
    # Creates random start and end vertices that will be used for the depth
    # first search.
    start_vertex = random.randint(0, graph_size - 1)
    end_vertex = random.randint(0, graph_size - 1)
    
    # Creates the graphs to be tested.
    list_of_graphs = generate_test_graphs(graph_size, 5)
    
    print("For all DFS, start vertex = %d, end vertex = %d" % (start_vertex, end_vertex))
    if small_graph_selection and print_graphs:
        print("Reference images of the graphs' paths will be saved to the current directory")

    # Runs tests for undirected graphs.
    print("\nUndirected Graphs DFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    dfs_test(list_of_graphs[0], start_vertex, end_vertex, print_graphs, small_graph_selection)
    
    # Runs tests for directed graphs.
    print("\nDirected Graphs DFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1])
    dfs_test(list_of_graphs[1], start_vertex, end_vertex, print_graphs, small_graph_selection)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs DFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[2])
    dfs_test(list_of_graphs[2], start_vertex, end_vertex, print_graphs, small_graph_selection)
     
    # Runs tests for directed, weighted graphs.
    print("\nWeighted and Directed Graphs DFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[3])
    dfs_test(list_of_graphs[3], start_vertex, end_vertex, print_graphs, small_graph_selection)

# Function that initiates the tests for breadth first search.
# Input: The size of graphs to be created and a boolean that determines whether
#        the graphs will be printed. The boolean small_graph_selection is only
#        for lab demos to draw the graphs with 10 vertices.
# Output: None   
def run_automated_bfs(graph_size, print_graphs, small_graph_selection):
    
    # Creates random start and end vertices that will be used for the breadth
    # first search.
    start_vertex = random.randint(0, graph_size - 1)
    end_vertex = random.randint(0, graph_size - 1)
    
    # Creates the graphs to be tested.
    list_of_graphs = generate_test_graphs(graph_size, 4)

    print("For all BFS, start vertex = %d, end vertex = %d" % (start_vertex, end_vertex))

    if small_graph_selection and print_graphs:
        print("Reference images of the graphs' paths will be saved to the current directory")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs BFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    bfs_test(list_of_graphs[0], start_vertex, end_vertex, print_graphs, small_graph_selection)
    
    # Runs tests for directed graphs.
    print("\nDirected Graphs BFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1])
    bfs_test(list_of_graphs[1], start_vertex, end_vertex, print_graphs, small_graph_selection)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs BFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[2])
    bfs_test(list_of_graphs[2], start_vertex, end_vertex, print_graphs, small_graph_selection)
     
    # Runs tests for weighted, directed graphs.
    print("\nWeighted and Directed Graphs BFS")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[3])
    bfs_test(list_of_graphs[3], start_vertex, end_vertex, print_graphs, small_graph_selection)

# Function that initiates the tests for the graphs' edge deletions.
# Input: The size of graphs to be created and a boolean that determines whether
#        the graphs will be printed.
# Output: None    
def run_automated_delete(graph_size, print_graphs):
    
    # Recieves the graphs populated with the edge_combos. The edge_combos will
    # used to delete the edges.
    list_of_graphs, edge_combos = generate_test_graphs(graph_size, 2)

    # Runs tests for undirected graphs.
    print("\nUndirected Graphs Deletion")
    print("________________________________________________")
    if print_graphs:
        print("Graph Before:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    delete_test(list_of_graphs[0], edge_combos, print_graphs)
    
    # Runs tests for directed graphs.
    print("\nDirected Graphs Deletion")
    print("________________________________________________")
    if print_graphs:
        print("Graph Before:",end = "\n")
        display_all_graphs(list_of_graphs[1])
    delete_test(list_of_graphs[1], edge_combos, print_graphs)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs Deletion")
    print("________________________________________________")
    if print_graphs:
        print("Graph Before:",end = "\n")
        display_all_graphs(list_of_graphs[2])
    delete_test(list_of_graphs[2], edge_combos, print_graphs)
     
    # Runs tests for weighted, directed graphs.
    print("\nWeighted and Directed Graphs Deletion")
    print("________________________________________________")
    if print_graphs:
        print("Graph Before:",end = "\n")
        display_all_graphs(list_of_graphs[3])
    delete_test(list_of_graphs[3], edge_combos, print_graphs)

# Function that initiates the tests for the graphs' display.
# Input: The size of graphs to be created.
# Output: None     
def run_automated_display(graph_size):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs(graph_size, 6)
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs Display")
    print("________________________________________________")
    display_test(list_of_graphs[0])
    
    # Runs tests for directed graphs.
    print("\nDirected Graphs Display")
    print("________________________________________________")
    display_test(list_of_graphs[1])
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs Display")
    print("________________________________________________")
    display_test(list_of_graphs[2])
     
    # Runs tests for weighted, directed graphs.
    print("\nWeighted and Directed Graphs Display")
    print("________________________________________________")
    display_test(list_of_graphs[3])

# Function that initiates the tests for the graphs' drawings.
# Input: The size of graphs to be created.
# Output: None   
def run_automated_draw(graph_size, display_graphs):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs(graph_size, 7)
    
    # Runs tests for undirected graphs.
    if display_graphs:
        print("Graphs to be drawn:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    print("\nUndirected Graphs Draw")
    print("________________________________________________")
    draw_test(list_of_graphs[0])
    
    # Runs tests for directed graphs.
    if display_graphs:
        print("Graphs to be drawn:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    print("\nDirected Graphs Draw")
    print("________________________________________________")
    draw_test(list_of_graphs[1])
    
    # Runs tests for weighted graphs.
    if display_graphs:
        print("Graphs to be drawn:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    print("\nWeighted Graphs Draw")
    print("________________________________________________")
    draw_test(list_of_graphs[2])
     
    # Runs tests for weighted, directed graphs.
    if display_graphs:
        print("Graphs to be drawn:",end = "\n")
        display_all_graphs(list_of_graphs[0])
    print("\nWeighted and Directed Graphs Draw")
    print("________________________________________________")
    draw_test(list_of_graphs[3])

# Function that creates a list_of_graphs that contains four sublists of directed,
# undirected, weigthed, and weighted, directed graphs. Based on the function
# number the graphs and edge combinations will be returned.
# Input: the graph size to be created and the function number.
# Output: The following specifies what the function_num repsents and what will
#         be returned accordingly:
# function_num == 1: insert method calls it. Returns a list of unpopulated 
#                    and a list of valid edge combinations.
# function_num == 2: delete method calls it. Returns a list of populated 
#                    graphs and a hash table with linear chaining's list 
#                    containing all the edges.
# function_num == 3: used for different graph representations. Returns the
#                    populated graphs.
# function_num == 4: used for breadth first search. Returns the populated graphs.
# function_num == 5: used for depth first search. Returns the populated graphs.
# function_num == 6: used for display. Returns the populated graphs.
# function_num == 7: used for draw. Returns the populated graphs.
def generate_test_graphs(graph_size, function_num):
    
    # Recieves combinations of valid edges.
    edge_combos = compute_edge_combos(graph_size, int(graph_size * 1.5))
    
    list_of_graphs_undirected = [al.Graph(graph_size), am.Graph(graph_size), 
                                 el.Graph(graph_size)]
    list_of_graphs_directed = [al.Graph(graph_size, directed = True), 
                               am.Graph(graph_size, directed = True),
                               el.Graph(graph_size, directed = True)]
    list_of_graphs_weighted = [al.Graph(graph_size, True), 
                               am.Graph(graph_size, True),
                               el.Graph(graph_size, True)]
    list_of_graphs_weight_dir = [al.Graph(graph_size, True, True), 
                               am.Graph(graph_size, True, True),
                               el.Graph(graph_size, True, True)]
    
    # Creates lists of unpopulated graphs.
    list_of_graphs = [list_of_graphs_undirected, list_of_graphs_directed, 
                      list_of_graphs_weighted, list_of_graphs_weight_dir]
    
    if function_num == 1:
        return list_of_graphs, edge_combos

    # Populates all the graphs with the edges from edge_combos.
    for i in range(len(list_of_graphs)):
        for j in range(len(list_of_graphs[i])):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i][j].weighted:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1])
    if function_num == 2:
        return list_of_graphs, edge_combos
    return list_of_graphs
    
# Function that allows users to select which graph function they would like
# to test on selected graph sizes.
# Input: None
# Output: None
def automated_test_setup():
    print("Select a function to test")
    print("1. Insert")
    print("2. Delete")
    print("3. Different Graphical Representations")
    print("4. Breadth First Search")
    print("5. Depth First Search")
    print("6. Display")
    print("7. Draw")
    
    menu = int(input("Select 1 - 7: "))
    print()
    if menu >= 1 and menu <= 7:
        
        # Prompts users to select the graph size to be tested.
        if menu >= 1 and menu <= 5:
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 500 vertices and 150 edges")
            print("3. 1000 vertices and 750 edges")
            print("4. 10000 vertices and 1500 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 500, 1000, 10000]
        else:
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 15 vertices and 22 edges")
            print("3. 20 vertices and 30 edges")
            print("4. 30 vertices and 45 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 15, 20, 30]
        
        if size_selection >= 1 and size_selection <= 4:
            graph_size = graph_size[size_selection - 1]
            
            if graph_size == 10:
                small_graph_selection = True
            else:
                small_graph_selection = False
            
            # Determines if the user wants the graphs displayed.
            if menu != 6:
                print("Would you like to display the graph?")
                print("1. Yes")
                print("2. No")
                print_graphs = int(input("Select 1 or 2: "))
                print()
                
                if print_graphs >= 1 and print_graphs <= 2:
                    if print_graphs == 1:
                        print_graphs = True
                    else:
                        print_graphs = False
                else:
                    print("Invalid menu number. Program terminating.")
                    return

            # Calls the corresponding run_automated function based on the
            # menu number selected.
            if menu == 1:
                run_automated_insertion(graph_size, print_graphs)
            elif menu == 2:
                run_automated_delete(graph_size, print_graphs)
            elif menu == 3:
                run_automated_diff_rep(graph_size, print_graphs)
            elif menu == 4:
                run_automated_bfs(graph_size, print_graphs, small_graph_selection)
            elif menu == 5:
                run_automated_dfs(graph_size, print_graphs, small_graph_selection)
            elif menu == 6:
                run_automated_display(graph_size)
            else:
                run_automated_draw(graph_size, print_graphs)
            
        else:
            print("Invalid menu number. Program terminating.")
    else:
        print("Invalid menu number. Program terminating.")

# Function that allows users to insert their own edge.
# Input: The current customized graph.
# Output: None, other than the runtime for the insertion method.
def custom_insert(graph):
    
    # Retrieves the source and destination vertex from the user.
    print("Enter the following attributes")
    source = int(input("Source Vertex: "))
    dest = int(input("Destination Vertex: "))
    if graph.weighted:
        weight = int(input("Weight: "))
    else:
        weight = 1
    
    # Inserts the edge.
    start_time = time.perf_counter()
    graph.insert_edge(source, dest, weight)
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))
 
# Function that allows users to delete an edge from the graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the deletion method.
def custom_delete(graph):
    
    # Retrieves the source and destination vertex from the user.
    print("Enter the following attributes")
    source = int(input("Source Vertex: "))
    dest = int(input("Destination Vertex: "))
    
    # Deletes the edge.
    start_time = time.perf_counter()
    graph.delete_edge(source, dest)
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))

# Function that allows users to create a different graphical repsentation based
# on the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the graph representation method.
def custom_graph_rep(graph):
    print("Select a graph to create based on the current graph")
    print("1. Adjacency List")
    print("2. Adjacency Matrix")
    print("3. Edge List")
    menu = int(input("Select 1, 2, or 3: "))
    
    # Converts the current graph to an adjacency list.
    if menu == 1:
        start_time = time.perf_counter()
        created_graph = graph.as_AL()
        end_time = time.perf_counter()
        
    # Converts the current graph to an adjacency matrix.
    elif menu == 2:
        start_time = time.perf_counter()
        created_graph = graph.as_AM()
        end_time = time.perf_counter()
        
    # Converts the current graph to an edge list.
    elif menu == 3:
        start_time = time.perf_counter()
        created_graph = graph.as_EL()
        end_time = time.perf_counter()
    else:
        print("Invalid menu selection. Returning to menu.")
        return
    
    print("Runtime: %0.6f seconds\n" % (end_time - start_time))
    print(representation_to_text(graph.representation), "as", end = " ")
    display_graph(created_graph, True)

# Function that allows users to perform breadth first search on the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the breadth first search method.
def custom_bfs(graph):
    
    # Retrieves the start and end vertex from the user.
    print("Enter the following staring and ending vertex for the path to find")
    start = int(input("Staring Vertex: "))
    end = int(input("Ending Vertex: "))
    
    # Performs breadth first search.
    start_time = time.perf_counter()
    path = graph.breadth_first_search(start, end)
    end_time = time.perf_counter()
    
    print("Path: ", path)
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))  
    
    if not path is None and len(path) > 0:
        print("The graph with the path will be stored in the current directory.\n")
        graph.draw_path(path_to_set(path))

# Function that allows users to perform depth first search on the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the depth first search function.    
def custom_dfs(graph):
    
    # Retrieves the start and end vertex from the user.
    print("Enter the following staring and ending vertex for the path to find")
    start = int(input("Staring Vertex: "))
    end = int(input("Ending Vertex: "))
    
    # Performs depth first search
    start_time = time.perf_counter()
    path = graph.depth_first_search(start, end)
    end_time = time.perf_counter()
    
    print("Path:", path)
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))  
    if not path is None and len(path) > 0:
        print("The graph with the path will be stored in the current directory.\n")
        graph.draw_path(path_to_set(path))

# Function that displays the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the display function.       
def custom_display(graph):
    print(representation_to_text(graph.representation), ":")
    
    # Displays graph.
    start_time = time.perf_counter()
    graph.display()
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))
    
# Function that draws the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the display function.       
def custom_draw(graph):
    print("The graph will be stored in the current directory.")
    
    # Draws graph.
    start_time = time.perf_counter()
    graph.draw()
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))

# Function that allows the user to select an operation to perform on the graph.
# Input: None
# Output: An integer 1 through 8 that represents the menu selection or negative
#         one if an incorrect menu number was selected.
def custom_graph_function_selection_menu():
    print("Select an operation")
    print("1. Insert an edge")
    print("2. Delete an edge")
    print("3. Express as a different graphical representation")
    print("4. Perform Breadth First Search to Find a Path")
    print("5. Perform Depth First Search to Find a Path")
    print("6. Display Graph")
    print("7. Draw Graph")
    print("8. Exit")
    menu = int(input("Select 1 - 8: "))
    if menu < 1 or menu > 8:
        print("Invalid menu selection. Exiting program")
        menu = -1
    return menu

# Function that determines which custom function to call based on the user's
# menu selection.
# Input: The current graph created by the user.
# Output: None.
def custom_graph_interface(graph):
    menu = custom_graph_function_selection_menu()
    print()
    
    # Continues to allow the user to perform the operations on the custom graph
    # as long as a valid menu number is selected.
    while  menu >= 1 and menu <= 7:
        
        try:
            # Insert edge.
            if menu == 1:
                custom_insert(graph)
            
            # Delete edge.
            elif menu == 2:
                custom_delete(graph)
            
            # Convert to a different graph representation.
            elif menu == 3:
                custom_graph_rep(graph)
                
            # Perform breadth first search.
            elif menu == 4:
                custom_bfs(graph)
                
            # Perform depth first search.
            elif menu == 5:
                custom_dfs(graph)
                
            # Display the graph.
            elif menu == 6:
                custom_display(graph)
                
            # Draw the graph.
            else:
                custom_draw(graph)
        except ValueError:
            print("Invalid input. Please try again.\n")
        menu = custom_graph_function_selection_menu()
        print()

# Allows the user to create a custom graph. Retrieves the number of vertices
# and whether the graph is directed or weighted from the user.
# Input: None
# Output: None
def create_graph_menu():
    graph_type = select_graph_types()
    
    # If a valid graph type is selected, then the user selects the number of 
    # vertices the graph will have.
    if graph_type >= 1 and graph_type <= 3:
        print("How many vertices do you want the graph to have?")
        size = int(input("Enter the number of vertices: "))
        print()
        
        # The user determines whether they want the graph to be weighted or
        # unweighted.
        if size > 0:
            print("Do you want the graph to be weighted or unweighted?")
            print("1. Weighted")
            print("2. Unweighted")
            try:
                weighted = int(input("Select 1 or 2: "))
            except ValueError:
                weighted = 3
            print()
            
            if weighted == 1:
                weighted = True
            elif weighted == 2:
                weighted = False
            else:
                print("Invalid selection. The graph will be unweighted.\n")
                weighted = False
            
            # The user determines whether they want the graph to be directed or
            # undirected.
            print("Do you want the graph to be directed or undirected?")
            print("1. Directed")
            print("2. Undirected")
            try:
                directed = int(input("Select 1 or 2: "))
            except ValueError:
                directed = 3
            print()
            
            if directed == 1:
                directed = True
            elif directed == 2:
                directed = False
            else:
                print("Invalid selection. The graph will be undirected.\n")
                directed = False
            
            #Creates an adjacency list graph based on the user chosen attributes.
            if graph_type == 1:
                graph = al.Graph(size, weighted, directed)
                
            #Creates an adjacency matrix graph based on the user chosen attributes.
            elif graph_type == 2:
                graph = am.Graph(size, weighted, directed)
                
            #Creates an edge list graph based on the user chosen attributes.
            else:
                graph = el.Graph(size, weighted, directed)
            
            # Allows users to perform operations on the created graph.
            custom_graph_interface(graph)
            
        else:
            print("A graph has to have at least one vertex. Program terminating")
    else:
        print("Invalid menu number. Program terminating.")

# Main method that allows the user to determine whether they want to create
# their own graph, solve the riddle, run the provided tests, or run automated
# tests.
# Input: None
# Output: None
sys.setrecursionlimit(7000)
print("Welcome")
print("1. Create your own graph")
print("2. Chicken, Fox, Grain Riddle")
print("3. Run tests")
print("4. Run automated tests")
try:
    menu = int(input("Select 1, 2, 3, or 4: "))
    print()
    
    # Calls the corresponding function based on the user's menu selection.
    if menu == 1:
        create_graph_menu()
    elif menu == 2:
        riddle_menu_selection()
    elif menu == 3:
        run_test_graphs()
    elif menu == 4:
        automated_test_setup()
    else:
        print("Invalid menu number. Program terminating.")
except ValueError:
    print("Invalid input. Program terminating.")