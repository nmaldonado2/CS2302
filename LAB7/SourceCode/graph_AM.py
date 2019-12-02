# Course: CS2302 Data Structures
# Date of Last Modification: November 29, 2019
# Assignment: Lab 7 - Algorithm Design Techniques
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab was to verify if a Hamiltonian cycle exists
#          using randomization or identify if a Hamiltonian cycle exists using
#           randomization.  Although the generalized randomization algorithm
#          is instituted in the main program, this class contains the randomization
#          and backtracking functions to compare the analysis between the 
#          different graphical representations.

import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
import DisjointSetForest as djsf
import HashTable as ht
import random

# Class Graph
# Attributes: an adjacency matrix, a boolean that represents if the graph is
#             weighted, a boolean that represents if the graph is directed,
#             and a string representation of the graph.
# Behaviours: insert_edge, delete_edge, display, draw, randomized_hamiltonian,
#              and backtracking_hamiltonian.  
class Graph:
    
    # Provided by the instructor
    # Constructor for the adjacenecy matrix representaion of a graph.
    # Input: the number of vertices the graph will contain and whether the
    #         graph is weighted or directed.
    # Output: None
    def __init__(self, vertices, weighted=False, directed = False):
        self.am = np.zeros((vertices,vertices),dtype=int)-1
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AM'
    
    # Function that inserts the edge between the source and dest by placing the
    # weight in the correct cell of the adjacency matrix.
    # Input: The source, desitnation, and weight of the edge.
    # Output: None.
    def insert_edge(self,source,dest,weight=1):
        
        # Ensures that the source and dest are not out of bounds.
        if source >= len(self.am) or dest >= len(self.am) or source < 0 or dest < 0:
            print('Error, vertex number out of range')
            
        # Ensures that if the graph is not weighted then the weight must be 1.
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
            
        # Inserts the edge.
        else:
            self.am[source][dest] = weight
            
            # If the graph is undirected, the the edge is denoted in the 
            # symmetric adjacnecy matrix cell.
            if not self.directed:
                self.am[dest][source] = weight
     
    # Function that deletes the edge between the source and dest by assigning
    # a -1 to the cell that signifies the edge.
    # Input: The source and destination that form the edge.
    # Output: Returns True if the edge was successfully removed. False otherwise.
    # Assume source and dest are within the bounds of the 2D am list.
    def delete_edge_(self, source, dest):
        if self.am[source][dest] == -1:
            return False
        self.am[source][dest] = -1
        return True
    
    # Function that deletes the edge between the source and dest.
    # Input: The source and destination that form the edge.
    # Output: None.
    def delete_edge(self, source, dest):
        
        # Ensures that the source and dest are not out of bounds.
        if source >= len(self.am) or dest >= len(self.am) or dest < 0 or source < 0:
            print("Error, vertex number out of range")
        else:
            
            # Deletes the edges
            deleted = self.delete_edge_(source, dest)
            
            # If the graph is undirected, then the second instance of the edge
            # is deleted.
            if not self.directed:
                deleted = self.delete_edge_(dest, source)
            if not deleted:
                print('Error, edge to be deleted was not found.') 
    
    # Function that prints the adjacency matrix.
    # Input: None.
    # Output: None.           
    def display(self):
        for row in self.am:
            print(row)
    
    # Function that draws the adjacency matrix.
    # Input: None.
    # Output: None. 
    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        
        # Iterates through the entire adjacnecy matrix and plots the corresponding
        # vertices and edges.
        for i in range(len(self.am)):
            for j in range(len(self.am[i])):
                if self.am[i][j] != -1:
                    d,w = j, self.am[i][j]
                    if self.directed or d>i:
                        x = np.linspace(i*scale,d*scale)
                        x0 = np.linspace(i*scale,d*scale,num=5)
                        diff = np.abs(d-i)
                        if diff == 1:
                            y0 = [0,0,0,0,0]
                        else:
                            y0 = [0,-6*diff,-8*diff,-6*diff,0]
                        f = interp1d(x0, y0, kind='cubic')
                        y = f(x)
                        s = np.sign(i-d)
                        ax.plot(x,s*y,linewidth=1,color='k')
                        if self.directed:
                            xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                            yd = [y0[2]-1,y0[2],y0[2]+1]
                            yd = [y*s for y in yd]
                            ax.plot(xd,yd,linewidth=1,color='k')
                        if self.weighted:
                            xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                            yd = [y0[2]-1,y0[2],y0[2]+1]
                            yd = [y*s for y in yd]
                            ax.text(xd[2]-s*2,yd[2]+3*s, str(w), size=12,ha="center", va="center")
            ax.plot([i*scale,i*scale],[0,0],linewidth=1,color='k')        
            ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
             bbox=dict(facecolor='w',boxstyle="circle"))
        ax.axis('off') 
        ax.set_aspect(1.0)
        
        # Saves graph as a .png.
        fig.set_size_inches(15,9)
        title = "am" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        plt.savefig(title, dpi = 200)
        plt.ioff()
    
    # Function that generates a random subset graph of V edges where V is the
    # number of vertices. Assume the graph has at least V edges.
    # Input: None
    # Output: If the subset graph has no more than two edges per vertex and at
    #         a maximum only contains a cycle connecting the first and last
    #         vertex, then the populated adjacency matrix graph is returned and
    #         a hash table with the edges. Otherwise None is returned.
    # For undirected graphs only. Assume the graph has at least V edges.
    def generate_random_subset(self):
        num_vertices = len(self.am)
        forest = djsf.DSF(len(self.am))
        edges_hash_table = ht.HashTableChain(len(self.am))
        subset_graph = Graph(len(self.am), weighted = self.weighted)
        
        # Continues to populate the adjacency matrix with random edges as long as
        # the number of edges is less than the number of vertices.
        while num_vertices > 0:
            vertex_one = random.randint(0, len(self.am) - 1)
            vertex_two = random.randint(0, len(self.am) - 1)
            edge_to_add = [vertex_one, vertex_two, self.am[vertex_one][vertex_two]]
            
            # Ensures that the random edge has not already been inserted into the subgraph.
            if self.am[vertex_one][vertex_two] != -1 and edges_hash_table.insert_double(edge_to_add) == 1:
               
                # If the number of indegrees for the edges is greater
                # than two, then the graph is not a Hamiltonian cycle.
                if len(edges_hash_table.bucket[vertex_one]) > 2 or len(edges_hash_table.bucket[vertex_two]) > 2:
                    return None, None
                
                # If the edges create a cycle and the expected amount of edges have
                # not been reached, then the subset is not a Hamiltonian cycle.
                if forest.union(vertex_one, vertex_two) == 0:
                    if num_vertices > 1:
                        return None, None

                
                subset_graph.insert_edge(edge_to_add[0], edge_to_add[1], edge_to_add[2])
                num_vertices -= 1    
        return subset_graph, edges_hash_table
    
    # For testing purposes only. For the assigned randomized algorithm, view
    # the NicholeMaldonado.py file.
    # Function that checks random subsets of a graph to determine if the graph
    # contains a Hamiltonian cycle.
    # Input: The number of trials which is defaulted to 1000.
    # Output: The subset graph conatining the Hamiltonian cycle, if it exists,
    #         and a list of the edges. Otherwise, None, None is returned.
    # Assume the graph is undirected and has at least V number of edges where
    # V is the number of vertices.
    def randomized_hamiltonian(self, test_trials = 1000):
        for i in range(test_trials):
            
            # Generates a random subset.
            subset_graph, edges_hash_table = self.generate_random_subset()
            
            # Checks if the subset graph contains a Hamiltonian cycle.
            if not subset_graph is None:
                if edges_hash_table.correct_num_edges():
                    return subset_graph, edges_hash_table.format_elements()
        return None, None
    
    # Function that uses backtracking to determine if a Hamiltonian cycle exists.
    # Input: The current vertex being evaluated, the disjoint set forest, the
    #        original starting vertex, and the number of vertices evaluated.
    # Output: A subset graph containing a Hamiltonian cycle, if it exists, and
    #         a list of the edges. Otherwise, None, None is returned, signifying
    #         that the backtracking needs to continue. None, -1 can also be
    #         returned, signifying that a Hamiltonian cycle cannot exist because
    #         a vertex with one edge was found.
    def backtracking_hamiltonian_recur(self, curr_vertex, forest, start_vertex, num_seen = 1):
        
        # If num_seen is greater than or equalt to the number of vertices, then
        # the subset graph is created if an edge exists between the start and
        # current vertex. Otherwise None, None is returned.
        if num_seen >= len(self.am):
            if self.am[curr_vertex][start_vertex] != -1:
                subset_graph = Graph(len(self.am), self.weighted, self.directed)
                subset_graph.insert_edge(start_vertex, curr_vertex)
                return [[start_vertex, curr_vertex]], subset_graph
            return None, None
        
        # Iterates through adjacent edges and makes recursive calls for unvisited
        # vertices.
        num_adjacent = 0
        for column in range(len(self.am[curr_vertex])):

            if self.am[curr_vertex][column] != -1:
                if curr_vertex != column:
                    num_adjacent += 1
                    
                # If the current edge has not been visited and does not make a 
                # cycle then a recursive call is made.
                if forest.parent[column] == -1 and forest.union(curr_vertex, column) == 1:
                    subset, subset_graph = self.backtracking_hamiltonian_recur(
                            column, forest, start_vertex, num_seen + 1)
                    
                    # If the subset is not None, then a Hamiltonian cycle has been
                    # found, so the current edge is appended.
                    if subset != None:
                        subset.append([column, curr_vertex])
                        subset_graph.insert_edge(column, curr_vertex, self.am[curr_vertex][column])
                        return subset, subset_graph
                    
                    # If the subset_graph is a -1, then a vertex with one edge has
                    # been found, so a Hamiltonian cycle cannot exist.
                    if subset_graph == -1:
                        return subset, subset_graph
                    forest.parent[column] = -1
                    
        # Once the entire row has been iterated through, if only one adjacent
        # edge exists then None, -1 is returned symbolizing that a Hamiltonian
        # cycle does not exist.
        if not self.directed and num_adjacent == 1:
            return None, -1
        return None, None
    
    # Function that intitates the backtracking recursive function to find a 
    # Hamiltonian cycle.
    # Input: The starting vertex of the search for the Hamiltonian cycle.
    # Output: None, None if a Hamiltonian cycle was not found. Otherwise, the
    #         the adjacency matrix representing the Hamiltonian cycle and the
    #         subset graph is returned.
    def backtracking_hamiltonian(self, start_vertex):
        forest = djsf.DSF(len(self.am))
        subset, subset_graph = self.backtracking_hamiltonian_recur(start_vertex, forest, start_vertex)
        if subset is None:
            return None, None
        return subset, subset_graph