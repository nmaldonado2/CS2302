# Course: CS2302 Data Structures
# Date of Last Modification: October 31, 2019
# Assignment: Lab 6 - Graphs
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to represent graphs through adjacency
#          lists, adjacency matrices, and edge lists. This file tests the
#          insert edge, delete edge, display, and draw functions for the designated
#          graph object.  The tests below were provided by the instructor.

import matplotlib.pyplot as plt

# Tests provided by the instructor.
# Fuction that runs tests provided by the insructor.
# Input: a list of graphs that contains an undirected, directed, weighted, and
#        weighted, directed graph.
# Output: None, other than the graphs are displayed after the operations are
#         performed.
def run_tests(graph_of_graphs):
    plt.close("all")  
    print("All graphs will be stored in the current directory.")
    
    # Performs insertion, deletion, draw, and display for undirected graphs.
    print("Undirected, unweighted graph")
    g = graph_of_graphs[0]
    g.insert_edge(0,1)
    g.insert_edge(0,2)
    g.insert_edge(1,2)
    g.insert_edge(2,3)
    g.insert_edge(3,4)
    g.insert_edge(4,1)
    g.display()
    g.draw()
    print("Undirected, unwieghted graph with edge from 1 to 2 deleted.")
    g.delete_edge(1,2)
    g.display()
    g.draw()
    
    # Performs insertion, deletion, draw, and display for directed graphs.
    print("\nDirected graph")
    g = g = graph_of_graphs[1]
    g.insert_edge(0,1)
    g.insert_edge(0,2)
    g.insert_edge(1,2)
    g.insert_edge(2,3)
    g.insert_edge(3,4)
    g.insert_edge(4,1)
    g.display()
    g.draw()
    print("Directed graph with edge from 1 to 2 deleted.")
    g.delete_edge(1,2)
    g.display()
    g.draw()
    
    # Performs insertion, deletion, draw, and display for weighted graphs.
    print("\nWeighted graph")
    g = g = graph_of_graphs[2]
    g.insert_edge(0,1,4)
    g.insert_edge(0,2,3)
    g.insert_edge(1,2,2)
    g.insert_edge(2,3,1)
    g.insert_edge(3,4,5)
    g.insert_edge(4,1,4)
    g.display()
    g.draw()
    print("Weight graph with edge from 1 to 2 deleted.")
    g.delete_edge(1,2)
    g.display()
    g.draw()
    
    # Performs insertion, deletion, draw, and display for directed, weighted graphs.
    print("\nWeighted and Directed graph")
    g = g = graph_of_graphs[3]
    g.insert_edge(0,1,4)
    g.insert_edge(0,2,3)
    g.insert_edge(1,2,2)
    g.insert_edge(2,3,1)
    g.insert_edge(3,4,5)
    g.insert_edge(4,1,4)
    g.display()
    g.draw()
    print("Weighted and Directed graph with edge from 1 to 2 deleted.")
    g.delete_edge(1,2)
    g.display()
    g.draw()
    
    # Displays the weigthed and directed graph as an adjacency list.
    print("\nWeighted and Directed graph as an adjacency list.")
    g1=g.as_AL()
    g1.draw()