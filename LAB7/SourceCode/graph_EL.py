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
#          depth first search.  This file provides the class for edge lists.
#          Functions included with the class are insert edge, delete edge,
#          draw, display, breadth first search, depth first search, draw path, 
#          and convert to other graphical representations.

import numpy as np
import matplotlib.pyplot as plt
import graph_AL as al
import graph_AM as am
import datetime
from scipy.interpolate import interp1d
import DisjointSetForest as djsf
import HashTable as htc
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
# Behaviours: insert_edge, delete_edge, display, draw, as_AM, as_AL, as_EL, 
#             draw_path, breadth_first_search, and depth_first_search.        
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
     
    # Function that draws the edge list and highlights a path, from set_of_edges
    # in red.
    # Input: A set of edges which represent the path to be highlighted.
    # Output: None.
    def draw_path(self, set_of_edges):
        scale = 30
        fig, ax = plt.subplots()

        # Iterates through the edge list and plots the corresponding edges.
        for i,edge in enumerate(self.el):
            
            # If an edge exists and it is in the set of edges, then its
            # line color is assigned to red.
            if set_of_edges.find(edge.source, edge.dest) or set_of_edges.find(edge.dest, edge.source):
                line_color = "r"
                
            # Otherwise, the line color defaults to black.
            else:
                line_color = "k"
                
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
            ax.plot(x,s*y,linewidth=1,color= line_color)
            if self.directed:
                xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                yd = [y0[2]-1,y0[2],y0[2]+1]
                yd = [y*s for y in yd]
                ax.plot(xd,yd,linewidth=1,color= line_color)
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
        fig.set_size_inches(15,9)
        title = "el_path" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        plt.savefig(title, dpi = 200)  
        plt.ioff()
     
    def is_path_connected(self, subset_of_edges):
        forest = djsf.DSF(self.vertices)
        forest.edges_to_disjoint_set_forest(subset_of_edges)
        num_roots = 0
        for vertex in forest.parent:
            if vertex == -1:
                num_roots += 1
            if num_roots == 2:
                return False
        return num_roots == 1
    
    def correct_num_in_degrees(self, in_degrees):
        for degree in in_degrees:
            if degree != 2:
                return False
        return True

    def generate_random_subset(self):
        num_vertices = self.vertices
        subset_of_edges = htc.HashTableChain(self.vertices)
        num_in_degrees = np.zeros(self.vertices, dtype = np.int)
        new_subset_graph = Graph(self.vertices, weighted = self.weighted)
        
        while num_vertices > 0:
            edge = random.randint(0, len(self.el) - 1)
            random_edge = [self.el[edge].source, self.el[edge].dest, self.el[edge].weight]

            if subset_of_edges.insert(random_edge) == 1:
                if num_in_degrees[random_edge[0]] >= 2 or num_in_degrees[random_edge[1]] >= 2:
                    return None, None, None
                num_in_degrees[random_edge[0]] += 1
                num_in_degrees[random_edge[1]] += 1
                
                if self.weighted:
                    new_subset_graph.insert_edge(random_edge[0], random_edge[1], random_edge[2])
                else:
                    new_subset_graph.insert_edge(random_edge[0], random_edge[1])
                
                num_vertices -= 1    
        return new_subset_graph, subset_of_edges, num_in_degrees, 
            
            
    def randomized_hamiltonian(self, test_trials = 1000):
        for i in range(test_trials):
            subset_graph, subset_of_edges, in_degrees = self.generate_random_subset()
            
            if not subset_graph == None:
                if self.correct_num_in_degrees(in_degrees) and self.is_path_connected(subset_of_edges.bucket):
                    return subset_graph, subset_of_edges
        return None, None     
    
    def find_edge(self, source, target):
        for edge in self.el:
            if not self.directed and edge.source > source and edge.source > target:
                return None, None
            if edge.source == source and edge.dest == target:
                subset_graph = Graph(self.vertices, self.weighted, self.directed)
                subset_graph.insert_edge(edge.dest, edge.source, edge.weight)
                return [[edge.dest, edge.source]], subset_graph
            if not self.directed and edge.dest == source and edge.source == target:
                subset_graph = Graph(self.vertices, self.weighted, self.directed)
                subset_graph.insert_edge(edge.source, edge.dest, edge.weight)
                return [[edge.source, edge.dest]], subset_graph
        return None, None
    
    def backtracking_hamiltonian_recur(self, curr_vertex, forest, start_vertex, num_seen = 1):
        if num_seen == self.vertices:
            return self.find_edge(curr_vertex, start_vertex)

        for edge in self.el:
            
            if not self.directed and edge.source > curr_vertex:
                break
            
            if (edge.source == curr_vertex and forest.parent[edge.dest] == -1 
                and forest.union(curr_vertex, edge.dest) == 1):
                
                subset, subset_graph = self.backtracking_hamiltonian_recur(
                        edge.dest, forest, start_vertex, num_seen + 1)

                if subset != None:
                    subset.append([edge.dest, curr_vertex])
                    subset_graph.insert_edge(edge.dest, curr_vertex, edge.weight)
                    return subset, subset_graph
                forest.parent[edge.dest] = -1
        
            elif (not self.directed and edge.dest == curr_vertex and 
                  forest.parent[edge.source] == -1 and forest.union(curr_vertex, edge.source) == 1):
                
                subset, subset_graph = self.backtracking_hamiltonian_recur(
                        edge.source, forest, start_vertex, num_seen + 1)
                
                if subset != None:
                    subset.append([edge.source, curr_vertex])
                    subset_graph.insert_edge(edge.source, curr_vertex, edge.weight)
                    return subset, subset_graph
                forest.parent[edge.source] = -1

        return None, None
    
    def backtracking_hamiltonian(self, start_vertex):
        forest = djsf.DSF(self.vertices)
        return self.backtracking_hamiltonian_recur(start_vertex, forest, start_vertex)
    
#    def backtracking_hamiltonian_recur(self, curr_vertex, visited, forest, num_seen = 1):
#        visited[curr_vertex] = True
#        
#        if num_seen == self.vertices:
#            if self.find_edge(curr_vertex, 0):
#                return [0]
#            return None
#        
#        for edge in self.el:
#            
#            if not self.directed and edge.source > curr_vertex:
#                break
#            
#            if edge.source == curr_vertex and not visited[edge.dest] and forest.union(curr_vertex, edge.dest) == 1:
#                subset = self.backtracking_hamiltonian_recur(edge.dest, visited, forest, num_seen + 1)
#                
#                if subset != None:
#                    
#                    subset.append(edge.dest)
#                    return subset
#                forest.parent[edge.dest] = -1
#                visited[edge.dest] = False
#        
#            elif (not self.directed and edge.dest == curr_vertex and not 
#                  visited[edge.source] and forest.union(curr_vertex, edge.source) == 1):
#                
#                subset = self.backtracking_hamiltonian_recur(edge.source, visited, forest, num_seen + 1)
#                
#                if subset != None:
#                    
#                    subset.append(edge.source)
#                    return subset
#                forest.parent[edge.source] = -1
#                visited[edge.source] = False
#        return None
#    
#    def backtracking_hamiltonian(self):
#        visited = [False for i in range(self.vertices)]
#        forest = djsf.DSF(self.vertices)
#        
#        subset = self.backtracking_hamiltonian_recur(0, visited, forest)
#        if not subset is None:
#            subset.append(0)
#        return subset