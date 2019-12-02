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
import random
import DisjointSetForest as djsf

# Class Edge
# Attributes: the destination vertex and edge weight.
# Behaviours: None
class Edge:
    
    # Provided by the instructor
    # Constructor for Edge class.
    # Input: the destination vertex and edge weight.
    # Output: None
    def __init__(self, dest, weight=1):
        self.dest = dest
        self.weight = weight

# Class Graph
# Attributes: an adjacency list, a boolean that represents if the graph is
#             weighted, a boolean that represents if the graph is directed,
#             and a string representation of the graph.
# Behaviours: insert_edge, delete_edge, display, draw, randomized_hamiltonian,
#              and backtracking_hamiltonian.  
class Graph:
    
    # Provided by the instructor
    # Constructor for the adjacency list representaion of a graph.
    # Input: the number of vertices the graph will contain and whether the
    #         graph is weighted or directed.
    # Output: None
    def __init__(self, vertices, weighted=False, directed = False):
        self.al = [[] for i in range(vertices)]
        self.weighted = weighted
        self.directed = directed
        self.representation = 'AL'
    
    # Provided by the instructor.
    # Function that inserts the edge between the source and dest by adding the
    # edge to the adjacency list.
    # Input: The source, destination, and weight of the edge.
    # Output: None.
    def insert_edge(self,source,dest,weight=1):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        elif weight!=1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
        else:
            self.al[source].append(Edge(dest,weight)) 
            if not self.directed:
                self.al[dest].append(Edge(source,weight))
    
    # Provided by the instructor.
    # Helper function that deletes the edge between the source and dest.
    # Input: The source and destination that form the edge.
    # Output: Returns True if the edge was successfully removed. False otherwise.
    def delete_edge_(self,source,dest):
        i = 0
        for edge in self.al[source]:
            if edge.dest == dest:
                self.al[source].pop(i)
                return True
            i+=1    
        return False
    
    # Provided by the instructor.
    # Function that deletes the edge between the source and dest.
    # Input: The source and destination that form the edge.
    # Output: None.
    def delete_edge(self,source,dest):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            print('Error, vertex number out of range')
        else:
            deleted = self.delete_edge_(source,dest)
            if not self.directed:
                deleted = self.delete_edge_(dest,source)
            if not deleted:        
                print('Error, edge to be deleted was not found.')      
    
    # Provided by the instructor.
    # Function that prints the edge list.
    # Input: None.
    # Output: None. 
    def display(self):
        print('[',end='')
        for i in range(len(self.al)):
            print('[',end='')
            for edge in self.al[i]:
                print('('+str(edge.dest)+','+str(edge.weight)+')',end='')
            print(']',end=' ')    
        print(']')   
     
    # Provided by the instructor.
    # Function that draws the edge list.
    # Input: None.
    # Output: None. 
    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        for i in range(len(self.al)):
            for edge in self.al[i]:
                d,w = edge.dest, edge.weight
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
        
        # Added to save the graph rather than display on the terminal.
        fig.set_size_inches(15,9)
        title = "al" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        plt.savefig(title, dpi = 200)
        plt.ioff()

    # Function that ensures that each vertex of an undirected graph has an
    # indegree of two.
    # Input: None
    # Output: A boolean that is true, if the indegree of each vertex is two
    #         or false otherwise.
    # Assume that the graph is undirected.
    def correct_num_in_degrees(self):
        for edges in self.al:
            if len(edges) != 2:
                return False
        return True
    
    # Function that inserts an edge into a graph and ensures that the edge does
    # not exist in the graph.
    # Input: The source, dest, and weight of the edge to be inserted.
    # Output: One is returned if the edge is inserted, -1 is returned otherwise.
    def insert_edge_no_duplicates(self, source, dest, weight = 1):
        if source >= len(self.al) or dest>=len(self.al) or source <0 or dest<0:
            return -1
        elif weight!=1 and not self.weighted:
            return -1
        else:
            
            # Ensures the edge does not exist before inserting into the graph.
            for edge in self.al[source]:
                if edge.dest == dest:
                    return -1
            if not self.directed:
                for edge in self.al[dest]:
                    if edge.dest == source:
                        return -1
                self.al[dest].append(Edge(source,weight))
            self.al[source].append(Edge(dest,weight)) 
            return 1
    
    # Function that generates a random subset graph of V edges where V is the
    # number of vertices. Assume the graph has at least V edges.
    # Input: None
    # Output: If the subset graph has no more than two edges per vertex and at
    #         a maximum only contains a cycle connecting the first and last
    #         vertex, then the populated adjacency list graph is returned.
    #         Otherwise None is returned.
    # For undirected graphs only. Assume the graph has at least V edges.
    def generate_random_subset(self):
        num_vertices = len(self.al)
        forest = djsf.DSF(len(self.al))
        subset_graph = Graph(len(self.al), weighted = self.weighted)
        
        # Continues to crate an adjacency list with random edges as long as
        # the number of edges is less than the number of vertices.
        while num_vertices > 0:
            
            # Generates random edges.
            vertex_one = random.randint(0, len(self.al) - 1)
            if len(self.al[vertex_one]) > 0:
                vertex_two = random.randint(0, len(self.al[vertex_one]) - 1)
 
                # Ensures that the random edge has not already been inserted into the subgraph.
                if subset_graph.insert_edge_no_duplicates(vertex_one, 
                    self.al[vertex_one][vertex_two].dest, 
                    self.al[vertex_one][vertex_two].weight) == 1:
                    
                    # If the edges create a cycle and the expected amount of edges have
                    # not been reached, then the subset is not a hamiltonian path.
                    if forest.union(vertex_one, self.al[vertex_one][vertex_two].dest) == 0:
                        if num_vertices > 1:
                            return None

                    # If the number of indegrees for the edges is greater
                    # than two, then the graph is not a hamiltonian cycle.
                    if len(subset_graph.al[vertex_one]) > 2 or len(
                            subset_graph.al[self.al[vertex_one][vertex_two].dest]) > 2:
                        return None
                    num_vertices -= 1    
        return subset_graph
    
    # Function that converts an adjacency list that only contains a Hamiltonian
    # cycle into a list of ordered edges.
    # Input: None
    # Output: A list containing a Hamiltonian cycle.
    # Assume the graph contains the edges of an undirected Hamiltonian cycle 
    # only.
    def al_to_cycle(self):
        if len(self.al[0]) != 2:
                return None
        prev_vertex = 0
        curr_vertex = self.al[0][1].dest
        cycle = [[self.al[0][0].dest, 0],[0, curr_vertex]]
        
        # Iterates through the edges inorder and populates a list of the
        # Hamiltonian cycle.
        while len(cycle) < len(self.al):
            if len(self.al[curr_vertex]) != 2:
                return None
            for edge in self.al[curr_vertex]:
                if edge.dest != prev_vertex:
                    cycle.append([curr_vertex, edge.dest])
                    prev_vertex = curr_vertex
                    curr_vertex = edge.dest
                    break
        return cycle
    
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
            subset_graph = self.generate_random_subset()
            
            # Checks if the subset graph contains a Hamiltonian cycle.
            if not subset_graph is None:
                if subset_graph.correct_num_in_degrees():
                    return subset_graph, subset_graph.al_to_cycle()
        return None, None
    
    # Function that determines if an edge exists between source and target in
    # an undirected graph.
    # Input: The source and target of the potential edge to be found.
    # Output: If the edge exists, an adjacency list with the edge is created
    #         along with a list of the edges. Otherwise None, None is returned.
    def find_edge(self, source, target):
        for edge in self.al[source]:
            if edge.dest == target:
                subset_graph = Graph(len(self.al), self.weighted, self.directed)
                subset_graph.insert_edge(edge.dest, source, edge.weight)
                return [[edge.dest, source]], subset_graph
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
        
        # Base case that returns a subset graph if an edge exists between the last
        # vertex seen and the first vertex.
        if num_seen == len(self.al):
            return self.find_edge(curr_vertex, start_vertex)
        
        # Base case that returns None and -1 if a vertex only has one edge.
        if len(self.al[curr_vertex]) <= 1:
            return None, -1
        
        # Iterates through the adjacent edges and if they do not create a
        # a cycle and the destination vertices have not been visited, then
        # a recursive call is made.
        for edge in self.al[curr_vertex]:
            if forest.parent[edge.dest] == -1 and forest.union(curr_vertex, edge.dest) == 1:
                subset, subset_graph = self.backtracking_hamiltonian_recur(
                        edge.dest, forest, start_vertex, num_seen + 1)
                
                # If the subset is not None, then a Hamiltonian cycle has been
                # found, so the current edge is appended.
                if not subset is None:
                    subset.append([edge.dest, curr_vertex])
                    subset_graph.insert_edge(edge.dest, curr_vertex, edge.weight)
                    return subset, subset_graph
                
                # If the subset_graph is a -1, then a vertex with one edge has
                # been found, so a Hamiltonian cycle cannot exist.
                if subset_graph == -1:
                    return subset, subset_graph
                
                forest.parent[edge.dest] = -1
        return None, None
    
    # Function that intitates the backtracking recursive function to find a 
    # Hamiltonian cycle.
    # Input: The starting vertex of the search for the Hamiltonian cycle.
    # Output: None, None if a Hamiltonian cycle was not found. Otherwise, the
    #         the adjacency list representing the Hamiltonian cycle and the
    #         subset graph is returned.
    def backtracking_hamiltonian(self, start_vertex):
        forest = djsf.DSF(len(self.al))
        subset, subset_graph = self.backtracking_hamiltonian_recur(start_vertex, forest, start_vertex)
        if subset is None:
            return None, None
        return subset, subset_graph  