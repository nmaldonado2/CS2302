# Course: CS2302 Data Structures
# Date of Last Modification: December 3, 2019
# Assignment: Lab 7 - Algorithm Design Techniques
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to verify if a Hamiltonian cycle exists
#          using randomization or identify if a Hamiltonian cycle exists using
#           randomization. The generalized randomization algorithm
#          follows the pseudocode provided and a function to evaluate the edit
#          distance between two strings is defined in the file below. The main
#          program allows user to test the randomization, backtracking,
#          dynammic programing edit distance functions, and create their own
#          tests.

import graph_AL as al
import graph_AM as am
import graph_EL as el
import random
import HashTable as ht
import time
import sys
import numpy as np
import DisjointSetForest as dj
import pandas

# Prints the matrix with the two strings as the column and and row headers.
# Input: two strings whose edit distances are represented by the matrix.
# Output: None other than the matrix printed.
def print_matrix_format(s1, s2, matrix):
    row = ["\"\""]
    for char in s1:
        row.append(char)
    column = ["\"\""]
    for char in s2:
        column.append(char)

    matrix = pandas.DataFrame(matrix, columns=column, index = row)
    print(matrix)

# Edit distance function that computes the minimum edit distance between s1
# and s2. If necessary, replacements can only be made between vowels or consonants.
# Input: two strings whose edit distance will be calculated.
# Output: The edit distance and the matrix used to compute the edit distance.
def edit_distance(s1,s2):
    vowels = set(["a","e","i","o","u"])
    
    d = np.zeros((len(s1)+1,len(s2)+1),dtype=int)
    d[0,:] = np.arange(len(s2)+1)
    d[:,0] = np.arange(len(s1)+1)

    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            if s1[i-1].lower() ==s2[j-1].lower():
                d[i,j] =d[i-1,j-1]
            else:
                
                # Insert, replace, delete
                n = [d[i,j-1],d[i-1,j-1],d[i-1,j]]
                order = np.argsort(np.array(n))
                
                # If the minimum value is for replace, then only vowels or consants
                # can be replaced.
                if order[0] == 1:
                    if (s1[i - 1].lower() in vowels) == (s2[j - 1].lower() in vowels):
                        d[i, j] = n[order[0]] + 1
                        
                    # Otherwise, the current cell's value is assigned to the
                    # next minimum value plus one.
                    else:
                        d[i, j] = n[order[1]] + 1
                else:
                    d[i,j] = n[order[0]] + 1
                    
    return d[-1,-1], d

# Generates a random subset of edges of size V and populates a graph with the
# edges.
# Input: The number of vertices in a graph and the edges.
# Output: The subset graph populated with the edges.
# Assume E does not contain duplicate edges.
def generate_random_subset(V, E):
    num_vertices = V
    forest = dj.DSF(V)
    if len(E) > 0 and E[0][2] == 1:
        weighted = False
    else:
        weighted = True
    subset_graph = al.Graph(V, weighted)
    
    # Will continue to populate a subgraph with random edges while the number 
    # of edges in the subgraph does not equal to the number of vertices.
    while num_vertices > 0:
        
        vertex = random.randint(0, len(E) - 1)
 
        # Ensures that the random edge has not already been inserted into the subgraph.
        if subset_graph.insert_edge_no_duplicates(E[vertex][0], E[vertex][1], E[vertex][2]) == 1:
            
            # If the edges create a cycle and the expected amount of edges have
            # not been reached, then the subset is not a hamiltonian path.
            if forest.union(E[vertex][0], E[vertex][1]) == 0:
                if num_vertices > 1:
                    return None

            # If the number of indegrees for the edges is greater
            # than two, then the graph is not a hamiltonian cycle.
            if len(subset_graph.al[E[vertex][0]]) > 2 or len(subset_graph.al[E[vertex][1]]) > 2:
                return None
            
            num_vertices -= 1    
    return subset_graph

# Function that validates if a Hamiltonian path exists based on the edges and
# vertices provided.
# Input: The number of vertices that the graph will contain and the list of 
#        edges.
# Output: The subset graph and cycle will be returned if a cycle is found.
#          Otherwise None, None will be returned.
def randomized_hamiltonian(V, E):
    if len(E) < V:
        return None
    for i in range(10000):
        subset_graph = generate_random_subset(V, E)

        if not subset_graph is None:
            return subset_graph, subset_graph.al_to_cycle()
    return None, None

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

# Function that allows for a list containing graphs to be displayed.
# Input: A 1D list that contains the graphs that will be displayed.
# Output: None.
def display_all_graphs(list_of_graphs, draw_graphs):
    for graph in list_of_graphs:
        display_graph(graph, draw_graphs)

# Creates a hash table with edge combinations based on the number of edges
# needed. Each edge's source vertex will be hashed based on the vertex number.
# Only non-duplicate edges are hashed to the table.
# Input: The number of vertices the graph will have and the number of edges
#        that need to be hashed to the table. only_al signifies if only an
#        adjacency list will be used for the generalized randomization.
# Output: A list of the hash table with linear chaining's buckets.
def compute_edge_combos(num_vertices, num_edges, edges_hash_table, only_al = False):
    i = 0
    if only_al:
            edge_list = [[],[]]
            
    while i != num_edges:
        
        # Creates random vertices and weights.
        vertex_one = random.randint(0,num_vertices - 1)
        vertex_two = random.randint(0, num_vertices - 1)
        weight = random.randint(2,99)

        # Hashes the edge to the table. If the insertion is successful, then
        # i is incremented.
        if vertex_one != vertex_two:
            if edges_hash_table.insert([vertex_one, vertex_two, weight]) != -1:
                i += 1
                if only_al:
                    edge_list[0].append([vertex_one, vertex_two, 1])
                    edge_list[1].append([vertex_one, vertex_two, weight])
    if only_al:
        return edge_list[0], edge_list[1]

# Runs test for the randomization algorithm.
# Input: The list of graphs to be tested, the boolean print edges which
#        determines whether the cycle will be printed, and the boolean small_graph
#        which determines whether or not the graph will drawn.
# Output: None
# Assume list_of_graphs is a list with undirected graphs. For lab demo purposes,
# graphs with only ten edges will be printed.
def randomization_test(list_of_graphs, print_edges, small_graph):
    
    # Runs the tests for radomization for each graph.
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        print(graph_type, end = ":\n")
        start_time = time.perf_counter()
        subset_graph, subset_edges = graph.randomized_hamiltonian()
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
         
        if print_edges:
            print("Edges:", subset_edges, "\n")

            if small_graph and not subset_graph is None:
                print("The subset graph will be stored in the current directory.\n")
                subset_graph.draw()
        else:
            print("Found cycle: ", end = "")
            if not subset_graph is None:
                print("True")
            else:
                print("False")
            print()
            
# Runs test for the generalized randomization algorithm.
# Input: The number of vertices and list of edges to be tested, the boolean 
#        print_edges which determines whether the cycle will be printed, and 
#        the boolean small_graph which determines whether or not the graph will 
#        be drawn.
# Output: None.
# For lab demo purposes, graphs with only ten edges will be printed.
def randomization_generalized_test(V, E, print_edges, small_graph):
    
    # Runs tests for the generalized randomization function.
    start_time = time.perf_counter()
    subset_graph, subset_edges = randomized_hamiltonian(V, E)
    end_time = time.perf_counter()
    print("Runtime: %0.6f seconds"%(end_time - start_time))
    
    # Prints the edges that create a cycle.
    if print_edges:
        print("Edges:", subset_edges, "\n")

        if small_graph and not subset_graph is None:
            print("The subset graph will be stored in the current directory.\n")
            subset_graph.draw()
    else:
        print("Found cycle: ", end = "")
        if not subset_graph is None:
            print("True")
        else:
            print("False")
        print()

# Populates a hash table with all the words found in the provided word file.
# Input: The path for the file contaiining the words.
# Output: A hash table with all the words hashed by string length.
def populate_word_list_hash_table(file_path):
    
    # Opens the file to read it.
    # Since file size can change, the max string length needs to be known
    # in order to hash the table properly by string length.
    word_file = open(file_path, "r")
    line = word_file.readline()
    max_length = -1
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            if len(line[0]) > 0 and line[0].isalpha() and len(line[0]) > max_length:
                max_length = len(line[0])
        line = word_file.readline()
    word_file.seek(0)
    line = word_file.readline()
    
    hash_table_words = ht.HashTableChain(max_length + 1)
    
    # Adds each word to hash_table_words as long as the word only contains 
    # letters.
    while line:
        if not line.isspace():
            line = line.rstrip("\n").split(" ")
            if len(line) > 0 and line[0].isalpha():
                hash_table_words.insert_word(line[0])
        line = word_file.readline()
    word_file.close()
    return hash_table_words

# Function that prints the list of edges.
# Input: A 2D list containing undirected edges at index 0 and weighted edges at
#        index 1.
# Output: None
def display_edge_list(edge_combos):
    print("Current Undirected Edges")
    print(edge_combos[0])
    print()
    print("Current Weighted Edges")
    print(edge_combos[1])
    print()

# Function that runs the edit distance test for two words of a given length.
# Input: The boolean print_matrix, that determines whether the matrix will be
#        printed, the word lengths of the words to be tested, the hash table
#        words containing all the words, and the number of trials to be run.
# Output: None, other than the matrix and the distance will be displayed.
def edit_distance_test(print_matrix, word_length_one, word_length_two, words, num_trials):
    
    # Ensures that the hash table words contains at least one word of each
    # word length.
    if (word_length_one >= len(words.bucket) or word_length_two >= len(words.bucket)
        or len(words.bucket[word_length_one]) == 0 or len(words.bucket[word_length_two]) == 0):
        print("The provided strings were longer than the words from the", end = "")
        print(" file provided or a word of the designated length does not exist.")
        print("The edit distance will not be calculated.")
        return
    
    # Runs the edit distance function one time to display a sample output.
    # If the number of trials is one, then only the current test will be run.
    if print_matrix:
        if word_length_one != 0:
            word_one = words.bucket[word_length_one][random.randint(0, len(words.bucket[word_length_one]) - 1)]
        else:
            word_one = ""
        if word_length_two != 0:
            word_two = words.bucket[word_length_two][random.randint(0, len(words.bucket[word_length_two]) - 1)]
        else:
            word_two = ""
            
        if num_trials != 1:
            print("Sample matrix:\n")
        else:
            print("Matrix:")
            start_time = time.perf_counter()
        distance, matrix = edit_distance(word_one, word_two)
        if num_trials == 1:
            end_time = time.perf_counter()
            print("Runtime: %0.6f seconds\n" % (end_time - start_time))
        print_matrix_format(word_one, word_two, matrix)
        print("Distance:", distance)
        print()
    
    # Performs the tests for the given number of trials if the number of trials
    # is greater than one.
    if num_trials > 1:
        start_time = time.perf_counter()
        for i in range(num_trials): 
            word_one = random.randint(0, len(words.bucket[word_length_one]) - 1)
            word_two = random.randint(0, len(words.bucket[word_length_two]) - 1)
            edit_distance(words.bucket[word_length_one][word_one], words.bucket[word_length_two][word_two])
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        print()

# Prepares tests for the edit distance function.
# Input: A boolean that determines whether the matrix will be printed, the word
#       length to to be tested, and a hash table, words, with all the words.
#  Output: None.
def run_automated_edit_distance(print_matrix, word_length, words):
    print("----------------------------------------------")
    print("|  500 Tests for random words of length", word_length, " |")
    print("----------------------------------------------")
    edit_distance_test(print_matrix, word_length, word_length, words, 500)
    
    print("----------------------------------------------")
    print("| 5,000 Tests for random words of length", word_length, " |")
    print("----------------------------------------------")
    edit_distance_test(print_matrix, word_length, word_length, words, 5000)
    
    print("-----------------------------------------------")
    print("| 10,000 Tests for random words of length", word_length, " |")
    print("-----------------------------------------------")
    edit_distance_test(print_matrix, word_length, word_length, words, 10000)

# Ensures that file_path includes a .txt file at the end.
# Input: a string of the file path that will be evaluated.
# Output: Returns false if file_path does not end in .txt and returns
#         true otherwise.
def is_txt_file(file_path):
    
    # Returns false if the file_path does not have at least 5 letters since a
    # valid .txt file name can have a minimum of 5 letters.
    if len(file_path) < 5:
        print("Invalid file.")
        return False
    
    # If the length of file_path is greater than or equal to 5, then true is
    # returned only if file_path ends in ".txt".
    else:
        if file_path[-4:] == ".txt":
            return True
        else:
            print("Invalid file.")
            return False

# Function that retrieves the file path that contains all the words to be used
# by the edit distance function.  Also initiates the storing of the words in a 
# hash table.
# Input: A boolean that determines whether the matrix will be printed, the word
#       lengths to be tested, and a boolean that determines whether a custom test
#       test will be run.
# Output: None.
def edit_distance_setup(print_matrix, word_length_one, word_length_two, custom_test = False):
    
    # Retrieves path for the file containing the word embeddings.
    print("Enter the file path for the words.")
    file_path = input("File Path: ")
    print()
    
    if is_txt_file(file_path):
        
        # Populates the hash table.
        words = populate_word_list_hash_table(file_path)
        
        # Performs a custom test.
        if custom_test:
            edit_distance_test(print_matrix, word_length_one, word_length_two, words, 1)
        
        # Otherwise performs the automated tests.
        else:
            run_automated_edit_distance(print_matrix, word_length_one, words)
    else:
        print("Program terminating.")
    

# Function that initiates the tests for the generalized randomization.
# Input: The size of graphs to be created, booleans print_graphs and small_graphs
#        that determine whether the graph will be printed, and the edge_factor.
# Output: None     
def run_automated_generalized_randomization(graph_size, print_graphs, small_graphs, edge_factor = 1.5):
    
    # Receives populated graphs.
    edge_hash_table = ht.HashTableChain(graph_size)
    edge_combos = compute_edge_combos(graph_size, int(graph_size * edge_factor), edge_hash_table, True)
    edge_combos_hamiltonian = generate_hamiltonian_cycle(graph_size, True, edge_factor)
    
    print("Finding Hamiltonian Cycle Based on Provided Pseudocode:")
    print("----------------------------------------------")
    print("|    Graphs with Known Hamiltonian Cycles    |")
    print("----------------------------------------------")
    if print_graphs:
        display_edge_list(edge_combos_hamiltonian)
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    randomization_generalized_test(graph_size, edge_combos_hamiltonian[0], print_graphs, small_graphs)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    randomization_generalized_test(graph_size, edge_combos_hamiltonian[1], print_graphs, small_graphs)
    
    print("------------------------------------------------")
    print("|    Graphs with Unknown Hamiltonian Cycles    |")
    print("------------------------------------------------")
    if print_graphs:
        display_edge_list(edge_combos)
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    randomization_generalized_test(graph_size, edge_combos[0], print_graphs, small_graphs)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    randomization_generalized_test(graph_size, edge_combos[1], print_graphs, small_graphs)

# Function that initiates the tests for the randomization algorithm based on
# the different graphical representations.
# Input: The size of graphs to be created and booleans print_graphs and
#        small_graphs that determines whether the graphs will be printed.
# Output: None.
def run_automated_randomization(graph_size, print_graphs, small_graphs):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs(graph_size)
    list_of_graphs_hamiltonian = generate_test_graphs_with_hamiltonian(graph_size)
    
    print("----------------------------------------------")
    print("|    Graphs with Known Hamiltonian Cycles    |")
    print("----------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs_hamiltonian[0], small_graphs)
    randomization_test(list_of_graphs_hamiltonian[0], print_graphs, small_graphs)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs_hamiltonian[1], small_graphs)
    randomization_test(list_of_graphs_hamiltonian[1], print_graphs, small_graphs)
    
    print("------------------------------------------------")
    print("|    Graphs with Unknown Hamiltonian Cycles    |")
    print("------------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0], small_graphs)
    randomization_test(list_of_graphs[0], print_graphs, small_graphs)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1], small_graphs)
    randomization_test(list_of_graphs[1], print_graphs, small_graphs)

# Funtion that initiates for the randomization algorithm with varying trials.
# Input: A list of graphs to be tested and booleans, print_edges and small_graphs,
#        that determine whether the graphs will be printed.
# Output: None
def randomization_varying_trials_test(list_of_graphs, print_edges, small_graph):
    
    # Runs the tests for 500 trials.
    for graph in list_of_graphs:
        print(representation_to_text(graph.representation))
        print("-------------------------------------------")
        print("500 Trials")
        print("-----------")
        start_time = time.perf_counter()
        subset_graph, subset_edges = graph.randomized_hamiltonian(500)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_edges:
            print("Edges:", subset_edges, "\n")

            if small_graph and not subset_graph is None:
                print("The subset graph will be stored in the current directory.\n")
                subset_graph.draw()
        else:
            print("Found Cycle: ", end = "")
            if not subset_edges is None:
                print("True")
            else:
                print("False")
        print()
        
        # Runs the tests for 1,000 trials
        print("1,000 Trials")
        print("-----------")
        start_time = time.perf_counter()
        subset_graph, subset_edges = graph.randomized_hamiltonian(1000)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_edges:
            print("Edges:", subset_edges, "\n")

            if small_graph and not subset_graph is None:
                print("The subset graph will be stored in the current directory.\n")
                subset_graph.draw()
        else:
            print("Found Cycle: ", end = "")
            if not subset_edges is None:
                print("True")
            else:
                print("False")
        print()
        
        # Runs tests for 1,500 trials.
        print("1,500 Trials")
        print("-----------")
        start_time = time.perf_counter()
        subset_graph, subset_edges = graph.randomized_hamiltonian(1500)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_edges:
            print("Edges:", subset_edges, "\n")

            if small_graph and not subset_graph is None:
                print("The subset graph will be stored in the current directory.\n")
                subset_graph.draw()
        else:
            print("Found Cycle: ", end = "")
            if not subset_edges is None:
                print("True")
            else:
                print("False")
        print()
 
# Function that prepares the randomization with varying trials.
# Input: The size of graphs to be created, and booleans print_graphs and 
#        small_graphs that determine whether the graphs will be printed..
# Output: None     
def run_automated_randomization_varying_trials(graph_size, print_graphs, small_graphs):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs_with_hamiltonian(graph_size)
    
    # Runs tests for undirected graphs.
    print("---------------------------------------------------")
    print("| Undirected Graphs with Known Hamiltonian Cycles |")
    print("---------------------------------------------------")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0], small_graphs)
    randomization_varying_trials_test(list_of_graphs[0], print_graphs, small_graphs)
    
    # Runs tests for weighted graphs.
    print("---------------------------------------------------")
    print("|  Weighted Graphs with Known Hamiltonian Cycles  |")
    print("---------------------------------------------------")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1], small_graphs)
    randomization_varying_trials_test(list_of_graphs[1], print_graphs, small_graphs)

# Function that tests the backtracking function to detect a Hamiltonian cycle.
# Input: the list_of_graphs to be tested, the start_vertex for the cycle, and
#        booleans small_graph and print_edges that determine whether the graphs
#        will be printed.
# Output: None
def backtracking_test(list_of_graphs, print_edges, small_graph, start_vertex):  
    
    # Runs the tests forbacktracking..
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        print(graph_type, ":")
        start_time = time.perf_counter()
        cycle, subset_graph = graph.backtracking_hamiltonian(start_vertex)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))

        if print_edges:
            print("Cycle:", cycle)
            print()
            if small_graph and not subset_graph is None:
                print("The subset graph will be stored in the current directory.\n")
                subset_graph.draw()
            elif not subset_graph is None:
                print("Subset graph:")
                subset_graph.display()
                print()
        else:
            print()

# Function that initiates the tests for finding a Hamiltonian cycle using
# backtracking.
# Input: The size of graphs to be created and booleans, print_graphs and
# small_graphs that determine whether the graphs will be printed.
# Output: None.
def run_automated_backtracking(graph_size, print_graphs, small_graphs):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs(graph_size)
    list_of_graphs_hamiltonian = generate_test_graphs_with_hamiltonian(graph_size)
    start_vertex = random.randint(0, graph_size - 1)
    print("For all tests, the start vertex is", start_vertex, end = ".\n")
    
    print("----------------------------------------------")
    print("|    Graphs with Known Hamiltonian Cycles    |")
    print("----------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs_hamiltonian[0], small_graphs)
    backtracking_test(list_of_graphs_hamiltonian[0], print_graphs, small_graphs, start_vertex)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs_hamiltonian[1], small_graphs)
    backtracking_test(list_of_graphs_hamiltonian[1], print_graphs, small_graphs, start_vertex)
    
    print("------------------------------------------------")
    print("|    Graphs with Unknown Hamiltonian Cycles    |")
    print("------------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0], small_graphs)
    backtracking_test(list_of_graphs[0], print_graphs, small_graphs, start_vertex)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1], small_graphs)
    backtracking_test(list_of_graphs[1], print_graphs, small_graphs, start_vertex)

# Function that creates a list_of_graphs that contains four sublists of 
# undirected and weighted graphs.
# Input: the graph size to be created.
# Output: returns a list of populated undirected and weighted, undirected graphs.
#         represented as adjacency lists, adjacency matrics, and edge lists.
def generate_test_graphs(graph_size):
    edge_combos = ht.HashTableChain(graph_size)
    
    # Recieves combinations of valid edges.
    compute_edge_combos(graph_size, int(graph_size * 1.5), edge_combos)
    edge_combos = edge_combos.bucket
    

    list_of_graphs_undirected = [al.Graph(graph_size), am.Graph(graph_size), 
                                 el.Graph(graph_size)]
    list_of_graphs_weighted = [al.Graph(graph_size, True), 
                               am.Graph(graph_size, True),
                               el.Graph(graph_size, True)]
    
    # Creates lists of unpopulated graphs.
    list_of_graphs = [list_of_graphs_undirected, list_of_graphs_weighted]

    # Populates all the graphs with the edges from edge_combos.
    for i in range(len(list_of_graphs)):
        for j in range(len(list_of_graphs[i])):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i][j].weighted:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1])
    return list_of_graphs

# Function that creates a hamiltonian graph with extra edges based on the edge
# factor.
# Input: the graph size to be created, boolean only_al which is set to true
#        if the generalized randomization program is used, and the edge factor.
# Output: if only_al is true a list containing all the graphs edges will be
#         returned. Otherwise the hash table bucket with all the edges will be
#         returned.
def generate_hamiltonian_cycle(num_vertices, only_al = False, edge_factor = 1.5):
    vertices_remaining = [i for i in range(num_vertices)]
    edges_hash_table = ht.HashTableChain(num_vertices)
    
    prior_vertex = random.randint(0, len(vertices_remaining) - 1)
    
    vertices_remaining[-1], vertices_remaining[prior_vertex] = vertices_remaining[prior_vertex], vertices_remaining[-1]
    first_vertex = vertices_remaining.pop(-1)

    if only_al:
        edge_combos = [[],[]]
    
    # Creates a hamiltonian cycle.
    while len(vertices_remaining) > 0:
        
        # Swap values to avoid popping and instead perform constant time removal.
        vertex_to_add = random.randint(0,len(vertices_remaining) - 1)
        vertices_remaining[-1], vertices_remaining[vertex_to_add] = vertices_remaining[vertex_to_add], vertices_remaining[-1]
        
        weight = random.randint(2,99)
        
        if edges_hash_table.insert([prior_vertex, vertices_remaining[-1], weight]) == 1:
            if only_al:
                edge_combos[0].append([prior_vertex, vertices_remaining[-1], 1])
                edge_combos[1].append([prior_vertex, vertices_remaining[-1], weight])
            prior_vertex = vertices_remaining.pop(-1)
    
    # Inserts the connecting edge of the Hamiltonian cycle.
    weight = random.randint(2,99)
    edges_hash_table.insert([prior_vertex, first_vertex, weight])
    if only_al:
        edge_combos[0].append([prior_vertex, first_vertex, 1])
        edge_combos[1].append([prior_vertex, first_vertex, weight])
    
    # CAdds random edges to the pre-existing graph edges.
    if only_al:
        unweighted, weighted = compute_edge_combos(num_vertices, int(
                num_vertices * edge_factor) - num_vertices, edges_hash_table, only_al)
        edge_combos[0] += unweighted
        edge_combos[1] += weighted

    else:
        compute_edge_combos(num_vertices, int(
                num_vertices * edge_factor) - num_vertices, edges_hash_table)
    if only_al:
        return edge_combos
    return edges_hash_table.bucket

# Function that creates a list_of_graphs that contains four sublists of 
# undirected and weighted graphs with a Hamiltonian cycle.
# Input: the graph size to be created
# Output: A list with two subcategories, weighted and undirected, that contains
#         for adjacency lists, adjacency matrices, and edge lists.
def generate_test_graphs_with_hamiltonian(graph_size):
    edge_combos = generate_hamiltonian_cycle(graph_size)

    list_of_graphs_undirected = [al.Graph(graph_size), am.Graph(graph_size), 
                                 el.Graph(graph_size)]
    list_of_graphs_weighted = [al.Graph(graph_size, True), 
                               am.Graph(graph_size, True),
                               el.Graph(graph_size, True)]

    
    # Creates lists of unpopulated graphs.
    list_of_graphs = [list_of_graphs_undirected, list_of_graphs_weighted]

    # Populates all the graphs with the edges from edge_combos.
    for i in range(len(list_of_graphs)):
        for j in range(len(list_of_graphs[i])):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i][j].weighted:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1])
    return list_of_graphs
    

# Function that allows users to select which graph function they would like
# to test on selected graph sizes.
# Input: None
# Output: None
def automated_test_setup():
    print("Select a function to test")
    print("1. Generalized Randomization Hamiltonian Cycle")
    print("2. Generalized Randomization Hamiltonian Cycle with Reduced Edges")
    print("3. Randomization Hamiltonian Cycle with Set Trials")
    print("4. Randomization Hamiltonian Cycle with Varying Trials")
    print("5. Backtracking Hamiltonian Cycle")
    print("6. Edit Distance")
    
    menu = int(input("Select 1 - 6: "))
    print()
    if menu >= 1 and menu <= 6:
        if menu == 1 or menu == 3:
            
            # Prompts users to select the graph size to be tested.
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 100 vertices and 150 edges")
            print("3. 250 vertices and 375 edges")
            print("4. 500 vertices and 750 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 100, 250, 500]
        elif menu == 2:
            
            # Prompts users to select the graph size to be tested.
            print("Select a graph size")
            print("1. 10 vertices and 11 edges")
            print("2. 22 vertices and 24 edges")
            print("3. 27 vertices and 29 edges")
            print("4. 45 vertices and 49 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 20, 27, 45]
            
        elif menu == 4:
            
            # Prompts users to select the graph size to be tested.
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 15 vertices and 22 edges")
            print("3. 20 vertices and 30 edges")
            print("4. 500 vertices and 750 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 15, 20, 500]
        elif menu == 5:
            
            # Prompts users to select the graph size to be tested.
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 20 vertices and 30 edges")
            print("3. 27 vertices and 40 edges")
            print("4. 45 vertices and 67 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 20, 27, 45]
            
        else:
            
            # Prompts users to select the matrix size to be tested.
            print("Select a Word Size")
            print("1. 7 X 7 Matrix")
            print("2. 11 X 11 Matrix")
            print("3. 21 X 21 Matrix")
            size_selection = int(input("Select 1 - 4: "))
            print()
            word_length = [6,10,20]
            word_length = word_length[size_selection - 1]
            
        if menu != 6:
            graph_size = graph_size[size_selection - 1]

        # Determines if the user wants the graphs displayed.
        print("Would you like to display the", end = " ")
        if menu == 6:
            print("matrix?")
        else:
            print("graph")
        print("1. Yes")
        print("2. No")
        print_graphs = int(input("Select 1 or 2: "))
        print()
                
        if print_graphs >= 1 and print_graphs <= 2:
            if print_graphs == 1:
                print_graphs = True
            else:
                print_graphs = False
            
            if menu != 6:
                if graph_size == 10:
                    small_graphs = True
                else:
                    small_graphs = False
            
            # Calls the corresponding run_automated function based on the
            # menu number selected.
            if menu == 1:
                run_automated_generalized_randomization(graph_size, print_graphs, small_graphs)
            elif menu == 2:
                run_automated_generalized_randomization(graph_size, print_graphs, small_graphs, 1.1)
            elif menu == 3:
                run_automated_randomization(graph_size, print_graphs, small_graphs)
            elif menu == 4:
                run_automated_randomization_varying_trials(graph_size, print_graphs, small_graphs)
            elif menu == 5:
                run_automated_backtracking(graph_size, print_graphs, small_graphs)
            elif menu == 6:
                edit_distance_setup(print_graphs, word_length, word_length)
            else:
                print("Invalid menu number. Program terminating")
        else:
            print("Invalid menu number. Program terminating.")
    else:
        print("Invalid menu number. Program terminating.")

# Function that intiates custom tests for the randomization algorithm.
# Input: a list_of_graphs which contains four unpopulated graphs based on the
#        users choice, the size of the graphs, and the edge factor.
# Output: None.
def run_custom_randomization(list_of_graphs, graph_size, edge_factor):
    generate_custom_graph_with_hamiltonian(list_of_graphs[0], graph_size, edge_factor)
    generate_custom_test_graphs(list_of_graphs[1], graph_size, edge_factor)
    
    
    print("---------------------------------------------")
    print("|    Graph with Known Hamiltonian Cycles    |")
    print("---------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[0][0], True)
    randomization_test([list_of_graphs[0][0]], True, True)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[0][1], True)
    randomization_test([list_of_graphs[0][1]], True, True)
    
    print("------------------------------------------------")
    print("|    Graph with Unknown Hamiltonian Cycles    |")
    print("------------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[1][0], True)
    randomization_test([list_of_graphs[1][0]], True, True)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[1][1], True)
    randomization_test([list_of_graphs[1][1]], True, True)

# Function that intiates custom tests for the backtracking algorithm.
# Input: a list_of_graphs which contains four unpopulated graphs based on the
#        users choice, the size of the graphs, and the edge factor.
# Output: None.
def run_custom_backtracking(list_of_graphs, graph_size, edge_factor, start_vertex):
    generate_custom_graph_with_hamiltonian(list_of_graphs[0], graph_size, edge_factor)
    generate_custom_test_graphs(list_of_graphs[1], graph_size, edge_factor)
    
    
    print("---------------------------------------------")
    print("|    Graph with Known Hamiltonian Cycles    |")
    print("---------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[0][0], True)
    backtracking_test([list_of_graphs[0][0]], True, True, start_vertex)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[0][1], True)
    backtracking_test([list_of_graphs[0][1]], True, True, start_vertex)
    
    print("------------------------------------------------")
    print("|    Graph with Unknown Hamiltonian Cycles    |")
    print("------------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[1][0], True)
    backtracking_test([list_of_graphs[1][0]], True, True, start_vertex)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    print("Current Graphs:",end = "\n")
    display_graph(list_of_graphs[1][1], True)
    backtracking_test([list_of_graphs[1][1]], True, True, start_vertex)

# Function that populates the graphs in list_of_graphs with edges that contain
# a Hamiltonian cycle.
# Input: the list of graphs to populated, the size of the graphs, and the edge
#        factor.
# Output: None.
def generate_custom_graph_with_hamiltonian(list_of_graphs, graph_size, edge_factor):
    
    # Receives edges with a Hamiltonian cycle.
    edge_combos = generate_hamiltonian_cycle(graph_size, edge_factor = edge_factor)
    
    # Populates the graphs.
    for i in range(len(list_of_graphs)):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i].weighted:
                        list_of_graphs[i].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i].insert_edge(edge_pair[0], edge_pair[1])
                        
# Function that populates the graphs in list_of_graphs with edges based on
# the edge factor.
# Input: the list of graphs to populated, the size of the graphs, and the edge
#        factor.
# Output: None.
def generate_custom_test_graphs(list_of_graphs, graph_size, edge_factor):
    edge_combos = ht.HashTableChain(graph_size)
    
    # Recieves combinations of valid edges.
    compute_edge_combos(graph_size, int(graph_size * edge_factor), edge_combos)
    edge_combos = edge_combos.bucket
    
    # Populates all the graphs with the edges from edge_combos.
    for i in range(len(list_of_graphs)):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i].weighted:
                        list_of_graphs[i].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i].insert_edge(edge_pair[0], edge_pair[1])

# Function that allows users to pick the number of vertices their graphs will
# have and the edge factor.
# Input: None
# Output: The number of vertices and the edge factor of the graphs to be tested.
def graph_attributes():
    print("How many vertices do you want the graph to have?")
    size = int(input("Enter the number of vertices: "))
    print()

    # The user determines the edge factor of the graph.
    if size > 2:
        max_factor = round(((size - 1) / 2), 3)
        
        print("Enter the factor between the number of vertices and edges.", end = "")
        print(" The factor, n, must lie in the following range:")
        print("1 <= n <= %0.3f\n" % max_factor)
       
        edge_factor = float(input("Enter the edge factor: "))
        print()
        if edge_factor < 1 or edge_factor > max_factor:
            print("The edge factor must be in the given range. Program terminating")
            return None, None
    else:
        print("The graph must have at least two vertices. Program terminating")
        return None, None
    return size, edge_factor

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

# Function that allows users to select the function they want to test.
# Input: None
# Output: The menu number based on the user's selection.  If the menu is one,
#          randomization is selected.  If two is chosen, then backtracking is
#          selected.
def select_backtrackng_or_randomization():
    print("Choose the function to create a custom test for")
    print("1. Randomization")
    print("2. Backtracking")
    menu = int(input("Select 1 or 2: "))
    print()
    return menu

# Function that creates a list of graphs based on the graph type.
# If the graph type is one, adjacency lists are created. If the graph type is
# two adjacency matrices are created. Otherwise edge lists are created.
# Assume graph_type is either 1, 2, or 3..
def create_graph(graph_type, size):
    
    # Creates a list with adjacency lists.
    if graph_type == 1:
        return [
                [al.Graph(size, False), al.Graph(size, True)],
                [al.Graph(size, False), al.Graph(size, True)]
               ]
        
    # Creates a list with adjacency matrices.
    if graph_type == 2:
        return [
                [am.Graph(size, False), am.Graph(size, True)],
                [am.Graph(size, False), am.Graph(size, True)]
               ]
        
    # Creates a list with edge lists  
    return [[el.Graph(size, False), el.Graph(size, True)],
            [el.Graph(size, False), el.Graph(size, True)]
            ]

# Allows the user to create a custom graph. Retrieves the number of vertices
# and the edge factor. Once selected, the function intiates the selected tests.
# Input: None
# Output: None
def create_graph_menu():    
    vertices, edge_factor = graph_attributes()
    
    # Based on function chosen, the corresponding tests will be called.
    if not vertices is None:
        backtracking_or_randomization = select_backtrackng_or_randomization()
        
        if backtracking_or_randomization == 1:
            print("What implementation do you want to use?")
            print("1. Generalized randomization")
            print("2. Graphical implementation of randomization")
            function_type = int(input("Select 1 or 2: "))
            print()
            
            # Runs test for the generalized randomization.
            if function_type == 1:
                run_automated_generalized_randomization(vertices, True, True, edge_factor)
                
            # Runs test for the randomization algorithm.
            elif function_type == 2:
                graph_type = select_graph_types()
                if graph_type >= 1 and graph_type <= 3:
                    graph = create_graph(graph_type, vertices)
                    run_custom_randomization(graph, vertices, edge_factor)
                else:
                    print("Invalid selection. Program terminating.")
                    
        # Runs test for the backtracking algorithm.
        elif backtracking_or_randomization == 2:
            graph_type = select_graph_types()
            if graph_type >= 1 and graph_type <= 3:
                graph = create_graph(graph_type, vertices)
                start_vertex = int(input("Enter a start vertex for the cycle: "))
                print()
                if start_vertex >= 0 and start_vertex < vertices:   
                    run_custom_backtracking(graph, vertices, edge_factor, start_vertex)
                else:
                    print("The start vertex must be within the vertice range. Program terminating.")
            else:
                print("Invalid selection. Program terminating.")
        else:
            print("Invalid input. Program terminating.")

# Function that intiates the testing for the edit distance function based on
# words chosen by the user of the word elgnths.
# Input: None
# Output: None.
def custom_edit_distance():
    print("1. Enter words")
    print("2. Select random words of a given length")
    menu = int(input("Select 1 or 2: "))
    print()
    
    # Allows user to enter their own words to be tested.
    if menu == 1:
        word_one = input("Word 1: ")
        word_two = input("Word 2: ")
        print()
        if word_one.isalpha() and word_two.isalpha():
            start_time = time.perf_counter()
            distance, matrix = edit_distance(word_one, word_two)
            end_time = time.perf_counter()
            print_matrix_format(word_one, word_two, matrix)
            print("Distance: ", distance)
            print("Runtime: %0.6f seconds"%(end_time - start_time))
            
            print()
        else:
            print("Invalid input. The words must contain letters only. Program terminating")
         
    # Otherwise runs tests based on the user specified word lengths.
    elif menu == 2:
        print("Enter the word lengths")
        word_length_one = int(input("First Word Length: "))
        word_length_two = int(input("Second Word Length: "))
        print()
        if word_length_one < 0 or word_length_two < 0:
            print("Words must have at least a length of 0. Program terminating.")
            return
        
        edit_distance_setup(True, word_length_one, word_length_two, custom_test = True)
        
        
    else:
        print("Invalid menu number. Program terminating")
        
# Main method that allows useres to create their own custom tests for randomization
# and backtracking, test the edit distance function, and run automated tests.
# Input: None.
# Output: None.
sys.setrecursionlimit(7000)
print("Welcome")
print("1. Create your own tests for backtracking or randomization")
print("2. Evaluate your own edit distance")
print("3. Run automated tests")
try:
    menu = int(input("Select 1, 2, or 3: "))
    print()
    
    # Calls the corresponding function based on the user's menu selection.
    if menu == 1:
        create_graph_menu()
    elif menu == 2:
        custom_edit_distance()
    elif menu == 3:
        automated_test_setup()
    else:
        print("Invalid menu number. Program terminating.")
except FileNotFoundError:
    print("One or more of the files provided for the word embeddings or")
    print("the pair of words could not be found. Program terminating.")
except IOError:
    print("One of more of the files provided for the word embeddings or")
    print("the pair of words could not be accessed. Program terminating.")
except ValueError:
    print("Invalid input. Program terminating.")