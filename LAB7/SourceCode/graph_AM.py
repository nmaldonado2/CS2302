# Course: CS2302 Data Structures
# Date of Last Modification: November 14, 2019
# Assignment: Lab 6 - Graphs
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab ws to represent graphs through adjacency
#          lists, adjacency matrices, and edge lists. These grahical
#          representations were then used to solve the riddle concerning a fox,
#          chicken, sack of grain, and person by using breadth first search and
#          depth first search.  This file provides the class for the adjacency
#          matrix. Functions included with the class are insert edge, delete
#          edge, draw, display, breadth first search, depth first search,
#          draw path, and convert to other graph representations.

import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
import DisjointSetForest as djsf
import HashTable as htc
import random

# Class Graph
# Attributes: an adjacency matrix, a boolean that represents if the graph is
#             weighted, a boolean that represents if the graph is directed,
#             and a string representation of the graph.
# Behaviours: insert_edge, delete_edge, display, draw, as_AM, as_AL, as_EL, 
#             draw_path, breadth_first_search, and depth_first_search.
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
    
    # Function that draws the adjacency matrix and highlights a path, from
    # set_of_edges in red.
    # Input: A set of edges which represent the path to be highlighted.
    # Output: None. 
    def draw_path(self, set_of_edges):
        scale = 30
        fig, ax = plt.subplots()
        
        # Iterates through the adjacnecy matrix and plots the corresponding
        # vertices and edges.
        for i in range(len(self.am)):
            for j in range(len(self.am[i])):
                
                # If an edge exists and it is in the set of edges, then its
                # line color is assigned to red.
                if self.am[i][j] != -1:
                    if set_of_edges.find(i, j) or set_of_edges.find(j, i):
                        line_color = "r"
                        
                    # Otherwise, the line color defaults to black.
                    else:
                        line_color = "k"
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
                        ax.plot(x,s*y,linewidth=1,color=line_color)
                        if self.directed:
                            xd = [x0[2]+2*s,x0[2],x0[2]+2*s]
                            yd = [y0[2]-1,y0[2],y0[2]+1]
                            yd = [y*s for y in yd]
                            ax.plot(xd,yd,linewidth=1,color=line_color)
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
        title = "am_path" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        plt.savefig(title, dpi = 200)
        plt.ioff()
    
    def is_path_connected(self, subset_of_edges):
        forest = djsf.DSF(len(self.am))
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

#    def generate_random_subset(self):
#        num_vertices = len(self.am)
#        subset_of_edges = htc.HashTableChain(len(self.am))
#        num_in_degrees = np.zeros(len(self.am), dtype = np.int)
#        new_subset_graph = Graph(len(self.am), weighted = self.weighted)
#        
#        while num_vertices > 0:
#            vertex_one = random.randint(0, len(self.am) - 1)
#            vertex_two = random.randint(0, len(self.am) - 1)
#            
#            random_edge = [vertex_one, vertex_two, self.am[vertex_one][vertex_two]]
#
#            if self.am[vertex_one][vertex_two] != -1 and subset_of_edges.insert(random_edge) == 1:
#                if num_in_degrees[random_edge[0]] >= 2 or num_in_degrees[random_edge[1]] >= 2:
#                    return None, None, None
#                num_in_degrees[random_edge[0]] += 1
#                num_in_degrees[random_edge[1]] += 1
#                
#                if self.weighted:
#                    new_subset_graph.insert_edge(random_edge[0], random_edge[1], random_edge[2])
#                else:
#                    new_subset_graph.insert_edge(random_edge[0], random_edge[1])
#                
#                num_vertices -= 1    
#        return new_subset_graph, subset_of_edges, num_in_degrees, 
#            
#            
#    def randomized_hamiltonian(self, test_trials = 500):
#        for i in range(test_trials):
#            subset_graph, subset_of_edges, in_degrees = self.generate_random_subset()
#            
#            if not subset_graph == None:
#                if self.correct_num_in_degrees(in_degrees) and self.is_path_connected(subset_of_edges.bucket):
#                    return subset_graph, subset_of_edges
#        return None, None
        
    def generate_random_subset(self):
        num_vertices = len(self.am)
        
        edges_hash_table = htc.HashTableChain(len(self.am))
        forest = djsf.DSF(len(self.am))
        
        num_in_degrees = np.zeros(len(self.am), dtype = np.int)
        subset_graph = Graph(len(self.am), weighted = self.weighted)
        
        while num_vertices > 0:
            vertex_one = random.randint(0, len(self.am) - 1)
            vertex_two = random.randint(0, len(self.am) - 1)
            
            random_edge = [vertex_one, vertex_two, self.am[vertex_one][vertex_two]]
            
            if self.am[vertex_one][vertex_two] != -1 and edges_hash_table.insert(random_edge) == 1:
                
                # If the edges create a cycle and the expected amount of edges have
                # not been reached, then the subset is not a hamiltonian path.
                if forest.union(random_edge[0], random_edge[1]) == -1:
                    if num_vertices > 1:
                        return None, None, None
                
                if num_in_degrees[random_edge[0]] >= 2 or num_in_degrees[random_edge[1]] >= 2:
                    return None, None, None
                num_in_degrees[random_edge[0]] += 1
                num_in_degrees[random_edge[1]] += 1
                
                subset_graph.insert_edge(random_edge[0], random_edge[1], random_edge[2])
                num_vertices -= 1    
                    
        subset_edges = subset_graph.am_to_cycle()
        return subset_graph, subset_edges, num_in_degrees, 
    
    def am_to_cycle(self):
        prev_vertex = 0
        curr_vertex = self.am[0][1].dest
        cycle = [[self.al[0][0].dest, 0],[0, curr_vertex]]
        
        am_column = 0
        while len(cycle) < 2:
            if self.am[0][am_column] != -1:
                if len(cycle) == 0:
                    cycle.append(am_column, 0)
                else:
                    cycle.append(0, am_column)
        
        while len(cycle) < len(self.al):
            for edge in self.al[curr_vertex]:
                if edge.dest != prev_vertex:
                    cycle.append([curr_vertex, edge.dest])
                    prev_vertex = curr_vertex
                    curr_vertex = edge.dest
                    break
        return cycle
                         
    def randomized_hamiltonian(self, test_trials = 1000):
        for i in range(test_trials):
            subset_graph, subset_of_edges, in_degrees = self.generate_random_subset()
            
            if not subset_graph is None:
                if self.correct_num_in_degrees(in_degrees):
                    return subset_graph, subset_of_edges
        return None, None
    
#    def find_edge(self, source, target):
#        for edge in self.am[column]:
#            if edge.dest == target:
#                return True
#        return False
    
#    def backtracking_hamiltonian_recur(self, curr_vertex, visited, forest, num_seen = 1):
#        visited[curr_vertex] = True
#
#        if num_seen == len(self.am):
#            if self.am[curr_vertex][0] != -1:
#                return [0]
#            return None
#        
#        for column in range(len(self.am[curr_vertex])):
#            if self.am[curr_vertex][column] != -1:
#                if not visited[column] and forest.union(curr_vertex, column) == 1:
#                    subset = self.backtracking_hamiltonian_recur(column, visited, forest, num_seen + 1)
#                    
#                    if subset != None:
#                        subset.append(column)
#                        return subset
#                    forest.parent[column] = -1
#                    visited[column] = False
#        return None
#    
#    def backtracking_hamiltonian(self):
#        visited = [False for i in range(len(self.am))]
#        forest = djsf.DSF(len(self.am))
#        
#        subset = self.backtracking_hamiltonian_recur(0, visited, forest)
#        if not subset is None:
#            subset.append(0)
#        print(subset)
#        return subset
        
    def backtracking_hamiltonian_recur(self, curr_vertex, forest, start_vertex, num_seen = 1):
        if num_seen >= len(self.am):
            if self.am[curr_vertex][start_vertex] != -1:
                subset_graph = Graph(len(self.am), self.weighted, self.directed)
                subset_graph.insert_edge(start_vertex, curr_vertex)
                return [[start_vertex, curr_vertex]], subset_graph
            return None, None
        
        for column in range(len(self.am[curr_vertex])):
            if self.am[curr_vertex][column] != -1:
                if forest.parent[column] == -1 and forest.union(curr_vertex, column) == 1:
                    subset, subset_graph = self.backtracking_hamiltonian_recur(
                            column, forest, start_vertex, num_seen + 1)
                    
                    if subset != None:
                        subset.append([column, curr_vertex])
                        subset_graph.insert_edge(column, curr_vertex, self.am[curr_vertex][column])
                        return subset, subset_graph
                    forest.parent[column] = -1
        return None, None
    
    def backtracking_hamiltonian(self, start_vertex):
        forest = djsf.DSF(len(self.am))
        return self.backtracking_hamiltonian_recur(start_vertex, forest, start_vertex)