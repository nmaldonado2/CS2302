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

# Class Edge
# Attributes: the source vertex, destination vertex, and edge weight.
# Behaviours: None
class Edge:
    
    # Provided by the instructor
    # Constructor for Edge class.
    # Input: the source vertex, destination vertex, and edge weight.
    # Output: None
    def __init__(self, source, dest, weight=1):
        self.source = source
        self.dest = dest
        self.weight = weight

# Class Graph
# Attributes: an edge list, a boolean that represents if the graph is
#             weighted, a boolean that represents if the graph is directed,
#             a string representation of the graph, and the number of vertices.
# Behaviours: insert_edge, delete_edge, display, draw, randomized_hamiltonian,
#              and backtracking_hamiltonian.         
class Graph:
    
    # Provided by the instructor
    # Constructor for the edge list representaion of a graph.
    # Input: the number of vertices the graph will contain and whether the
    #         graph is weighted or directed.
    # Output: None
    def __init__(self, vertices, weighted=False, directed = False):
        self.vertices = vertices
        self.el = []
        self.weighted = weighted
        self.directed = directed
        self.representation = 'EL'

    # Function that inserts an edge into the edge list in order. The edges
    # are ordered by the first vertex in ascending order and then for edges
    # with the same first vertex, the edges are ordered by the second vertex.
    # Input: The source vertex, destination vertex, weight, and
    #        bounds of the current portion of the edge list being analyzed
    #        denoted by start and end.
    # Output: None
    # Assume source is less than or equal to dest for undirected graphs.
    def insert_edge_(self, source, dest, weight, start, end):
        if len(self.el) == 0:
            self.el.append(Edge(source, dest, weight))
            return
        if start >= end:
            
            # If the source is less than the current source, the edge is 
            # inserted to the left.
            if source < self.el[start].source:
                self.el.insert(start, Edge(source, dest, weight))
                
            # If the source is greater than the current source, the edge is 
            # inserted to the right.
            elif source > self.el[start].source:
                if start == len(self.el) - 1:
                    self.el.append(Edge(source, dest, weight))
                else:  
                    self.el.insert(start + 1, Edge(source, dest, weight))
                    
            # Otherwise, if the source matches, the edge is inserted based on
            # the relationship between the destinations.
            else:
                if dest < self.el[start].dest:
                    self.el.insert(start, Edge(source, dest, weight))
                elif dest > self.el[start].dest:
                    if start == len(self.el) - 1:
                        self.el.append(Edge(source, dest, weight))
                    else:  
                        self.el.insert(start + 1, Edge(source, dest, weight))
                        
                # If the source and destination match, the the weight is updated
                # with the new weight.
                else:
                    self.el[start].weight = weight
            return
        
        mid = (start + end) // 2
        
        # If the source and destination match, the the weight is updated
        # with the new weight.
        if self.el[mid].source == source and self.el[mid].dest == dest:
            self.el[mid].weight = weight
            return
        
        # Performs binary insertion based on the source and dest relationship
        # with the middle edge's source and dest.
        if source < self.el[mid].source:
            self.insert_edge_(source, dest, weight, start, mid - 1)
        elif source > self.el[mid].source:
            self.insert_edge_(source, dest, weight, mid + 1, end)
        else:
            if dest < self.el[mid].dest:
                self.insert_edge_(source, dest, weight, start, mid - 1)
            else:
                self.insert_edge_(source, dest, weight, mid + 1, end)
                
    # Function that inserts the edge between the source and dest by adding the
    # edge to the edge list in order.
    # Input: The source, destination, and weight of the edge. If the graph
    #        is undirected and source is greater than the destination, then
    #        the edge will be inserted as (destination, source) to preserve
    #        the edge lists order as (min vertex value, max vertex value) for
    #        undirected graphs. For directed graphs, the order of (source, dest)
    #        is preserved.
    # Output: None.
    def insert_edge(self, source, dest, weight = 1):
        
        # Ensures that the source and dest are valid vertices.
        if source >= self.vertices or dest >= self.vertices or source < 0 or dest < 0:
            print("Error, vertex is out of range.")
            
        # Ensures that if the graph is not weighted then the weight must be 1.
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')   
        
        # Inserts edge.
        else:
            if self.directed:
                self.insert_edge_(source, dest, weight, 0, len(self.el) - 1)
            
            # If the graph is undirected, then source and dest can also be reordered
            # to dest and source.  The edge is created as (min, max) to preserve
            # the order.
            else:
                self.insert_edge_(min(source, dest), max(source, dest), weight, 0, len(self.el) - 1)
    
    # Function that deletes the edge with source and destination from the edge
    # list.
    # Input: The source vertex, destination vertex, and bounds for the current
    #        portion of the edge list analyzed.
    # Output: A boolean that denotes whether the edge was successfully deleted.
    def delete_edge_(self, source, dest, start, end):
        if start > end:
            return False
        
        mid = (start + end) // 2
        
        # Removes the edge if found.
        if source == self.el[mid].source and dest == self.el[mid].dest:
            self.el.pop(mid)
            return True
        
        # Searches for the edge to the left of the current middle edge.
        if source < self.el[mid].source:
            return self.delete_edge_(source, dest, start, mid - 1)
        
        # Searches for the edge to the right of the current middle edge.
        if source > self.el[mid].source:
            return self.delete_edge_(source, dest, mid + 1, end)
        
        # Searches for the edge to the left of the current middle edge.
        if dest < self.el[mid].dest:
            return self.delete_edge_(source, dest, start, mid - 1)
         
        # Searches for the edge to the right of the current middle edge.
        return self.delete_edge_(source, dest, mid + 1, end)
    
    # Function that deletes the edge between the source and dest.
    # Input: The source and destination that form the edge.
    # Output: None.
    def delete_edge(self, source, dest):
        if self.directed:
            deleted = self.delete_edge_(source, dest, 0, len(self.el) - 1)
        else:
            deleted = self.delete_edge_(min(source, dest), max(source, dest), 0, len(self.el) - 1)
        if not deleted:
            print('Error, edge to be deleted was not found') 
            
    # Function that prints the edge list.
    # Input: None.
    # Output: None. 
    def display(self):
        print("[", end = "")
        for i, edge in enumerate(self.el):
            print("(%d, %d, %d)" %(edge.source, edge.dest, edge.weight), end = "")
            if i < len(self.el) -1:
                print(end = " ")
        print("]")
    
    # Function that draws the edge list.
    # Input: None.
    # Output: None. 
    def draw(self):
        scale = 30
        fig, ax = plt.subplots()
        
        # Iterates through the entire edge list and plots the corresponding
        # edges.
        for i,edge in enumerate(self.el):
            d,w = edge.dest, edge.weight
            x = np.linspace(edge.source*scale,d*scale)
            x0 = np.linspace(edge.source*scale,d*scale,num=5)
            diff = np.abs(d-edge.source)
            if diff == 1:
                y0 = [0,0,0,0,0]
            else:
                y0 = [0,-6*diff,-8*diff,-6*diff,0]
            f = interp1d(x0, y0, kind='cubic')
            y = f(x)
            s = np.sign(edge.source-d)
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
        
        # Plots all the vertices.
        for i in range(self.vertices):
            ax.plot([i*scale,i*scale],[0,0],linewidth=1,color='k')     
            ax.text(i*scale,0, str(i), size=20,ha="center", va="center",
            bbox=dict(facecolor='w',boxstyle="circle"))
        ax.axis('off') 
        ax.set_aspect(1.0)
        
        # Saves the graph as a .png.
        title = "el" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        fig.set_size_inches(15,9)
        plt.savefig(title, dpi = 200)
        plt.ioff()
        
    # Identifies if an edge exists from the target to the source. Since the graph
    # must be undirected, a list is returned containing the edge from the target
    # to the source and a graph is created with the new edge.
    # Input: The target and source vertex.
    # Output: a list containing the edge from the target to the source and a
    #         graph containing the new edge.
    # Assume the graph is undirected.
    def find_edge(self, source, target):
        for edge in self.el:
            # Since the edge list is ordered, once the edge lies out of the 
            # range, None, None is returned.
            if not self.directed and edge.source > source and edge.source > target:
                return None, None
            
            # If the edge isfound, the subset graph and edge list are returned.
            if edge.source == source and edge.dest == target:
                subset_graph = Graph(self.vertices, self.weighted, self.directed)
                subset_graph.insert_edge(edge.dest, edge.source, edge.weight)
                return [[edge.dest, edge.source]], subset_graph
            if not self.directed and edge.dest == source and edge.source == target:
                subset_graph = Graph(self.vertices, self.weighted, self.directed)
                subset_graph.insert_edge(edge.source, edge.dest, edge.weight)
                return [[edge.source, edge.dest]], subset_graph
        return None, None
    
    # Recursive Backtracking algorithm that finds a Hamiltonian cycle, if it
    # exists, in the graph.
    # Input: The current vertex being evaulated, a disjoint set forest that
    #        ensures no cycles exists, except the final hamiltonian cycle, the
    #        original start vertex of the cycle, and the number of vertices seen.
    # Output: If a Hamiltonian cycle exists, the list of edges and the subset 
    #         graph will be returned.  Othwerwise, None, None or None, -1 will 
    #         be returned.
    def backtracking_hamiltonian_recur(self, curr_vertex, forest, start_vertex, num_seen = 1):
        
        # Base case that returns a subset graph if an edge exists between the last
        # vertex seen and the first vertex.
        if num_seen == self.vertices:
            return self.find_edge(curr_vertex, start_vertex)
        
        num_adjacent = 0
        
        # Iterates through the edge list. If an adjacent edge is found that 
        # has not been visisted and does not create a cycle, then a recursive
        # call is made.
        for edge in self.el:
            
            # Since the edge list is ordered, if the edge's source is greater
            # than the current vertex for undirected graphs, then all possible
            # adjacency edges have been seen.
            if not self.directed and edge.source > curr_vertex:
                break
            
            # Increments counter if an adjacent edge is found.
            if ((edge.source == curr_vertex and edge.dest != curr_vertex ) or 
                (not self.directed and edge.dest == curr_vertex and edge.source != curr_vertex)):
                num_adjacent += 1
            
            # If an adjacent edge is found that has not been visited and does 
            # not create a cycle, a recursive call is made.
            if (edge.source == curr_vertex and forest.parent[edge.dest] == -1 
                and forest.union(curr_vertex, edge.dest) == 1):
                
                subset, subset_graph = self.backtracking_hamiltonian_recur(
                        edge.dest, forest, start_vertex, num_seen + 1)
                
                # If the subset is not None, then a Hamiltonian cycle has been
                # found.
                if subset != None:
                    subset.append([edge.dest, curr_vertex])
                    subset_graph.insert_edge(edge.dest, curr_vertex, edge.weight)
                    return subset, subset_graph
                
                # If the subset_graph is -1, then the graph does not contain
                # a Hamiltonian cycle.
                if subset_graph == -1:
                    return subset, subset_graph
                forest.parent[edge.dest] = -1
        
            # If the graph is undirected and an adjacent edge is found that has
            # not been visited and does not create a cycle, a recursive call is
            # made.
            elif (not self.directed and edge.dest == curr_vertex and 
                  forest.parent[edge.source] == -1 and forest.union(curr_vertex, edge.source) == 1):
                
                subset, subset_graph = self.backtracking_hamiltonian_recur(
                        edge.source, forest, start_vertex, num_seen + 1)
                
                # If the subset is not None, then a Hamiltonian cycle has been
                # found.
                if subset != None:
                    subset.append([edge.source, curr_vertex])
                    subset_graph.insert_edge(edge.source, curr_vertex, edge.weight)
                    return subset, subset_graph
                
                # If the subset_graph is -1, then the graph does not contain
                # a Hamiltonian cycle.
                if subset_graph == -1:
                    return subset, subset_graph
                forest.parent[edge.source] = -1
                
        # If a vertex only has one edge, then the graph cannot a Hamiltonian 
        # cycle.
        if num_adjacent == 1:
            return None, -1
        return None, None
    
    # Function that intitates the backtracking recursive function to find a 
    # Hamiltonian cycle.
    # Input: The starting vertex of the search for the Hamiltonian cycle.
    # Output: None, None if a Hamiltonian cycle was not found. Otherwise, the
    #         the aedge list representing the Hamiltonian cycle and the
    #         subset graph is returned.
    def backtracking_hamiltonian(self, start_vertex):
        forest = djsf.DSF(self.vertices)
        subset, subset_graph = self.backtracking_hamiltonian_recur(start_vertex, forest, start_vertex)
        if subset is None:
            return None, None
        return subset, subset_graph
    
    # Function that generates a random subset graph of V edges where V is the
    # number of vertices. Assume the graph has at least V edges.
    # Input: None
    # Output: If the subset graph has no more than two edges per vertex and at
    #         a maximum only contains a cycle connecting the first and last
    #         vertex, then the populated adjacency matrix graph is returned and
    #         a hash table with the edges. Otherwise None is returned.
    # For undirected graphs only. Assume the graph has at least V edges.
    def generate_random_subset(self):
        num_vertices = self.vertices
        forest = djsf.DSF(self.vertices)
        edges_hash_table = ht.HashTableChain(self.vertices)
        subset_graph = Graph(self.vertices, self.weighted, self.directed)
        
        # Continues to populate the edge list with random edges while the 
        # num_vertices is greater than zero.
        while num_vertices > 0:
            edge = random.randint(0, len(self.el) - 1)
            edge_to_add = [self.el[edge].source, self.el[edge].dest, self.el[edge].weight]
                        
            # Ensures that the random edge has not already been inserted into 
            # the subgraph.
            if edges_hash_table.insert_double(edge_to_add) == 1:

                # If the edges create a cycle and the expected amount of edges 
                # have not been reached, then the subset is not a Hamiltonian 
                # cycle.
                if forest.union(edge_to_add[0], edge_to_add[1]) == 0:
                    if num_vertices > 1:
                        return None, None
                    
                # If the number of indegrees for the edges is greater
                # than two, then the graph is not a Hamiltonian cycle.
                if len(edges_hash_table.bucket[edge_to_add[0]]) > 2 or len(edges_hash_table.bucket[edge_to_add[1]]) > 2:
                    return None, None

                subset_graph.insert_edge(edge_to_add[0], edge_to_add[1], edge_to_add[2])
                num_vertices -= 1    
        return subset_graph, edges_hash_table
    
    # For testing purposes only. For the assigned randomized algorithm, view
    # the NicholeMaldonado.py file.
    # Function that checks random subsets of a graph to determine if the graph
    # contains a Hamiltonian cycle.
    # Input: The number of trials which is defaulted to 1000.
    # Output: The subset graph containing the Hamiltonian cycle, if it exists,
    #         and a list of the edges. Otherwise, None, None is returned.
    # Assume the graph is undirected and has at least V number of edges where
    # V is the number of vertices.
    def randomized_hamiltonian(self, test_trials = 1000):
        if len(self.el) < self.vertices:
            return None, None
        
        for i in range(test_trials):
            
            # Generates a random subset.
            subset_graph, edges_hash_table = self.generate_random_subset()
            
            # Checks if the subset graph contains a Hamiltonian cycle.
            if not subset_graph is None:
                if len(subset_graph.el) == self.vertices:
                    return subset_graph, edges_hash_table.format_elements()
        return None, None