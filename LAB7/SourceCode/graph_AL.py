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
#          list. Functions included with the graph are insert edge, delete edge,
#          draw, display, breadth first search, depth first search, draw path,
#          and convert to other graphical representations.

import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import interp1d
import random
import HashTable as htc
import DisjointSetForest as djsf
import LinkedList as ll

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
# Behaviours: insert_edge, delete_edge, display, draw, as_AM, as_AL, as_EL, 
#             draw_path, breadth_first_search, and depth_first_search.  
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
    
    # Function that draws the edge list and highlights a path, from set_of_edges
    # in red.
    # Input: A set of edges which represent the path to be highlighted.
    # Output: None.
    def draw_path(self, set_of_edges):
        scale = 30
        fig, ax = plt.subplots()
        
        # Iterates through the entire adjacnecy list and plots the corresponding
        # vertices and edges.
        for i in range(len(self.al)):
            for edge in self.al[i]:
                
                # If an edge is in the set of edges, then its line color is
                # assigned to red.
                if set_of_edges.find(i, edge.dest) or set_of_edges.find(edge.dest, i):
                    line_color = "r"

                # Otherwise, the line color defaults to black.
                else:
                    line_color = "k"
                
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
        title = "al_path" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        plt.savefig(title, dpi = 200)
        plt.ioff()


#    def bucket_to_al(self, bucket):
#        adj_list = Graph(len(bucket))
#        for b in bucket:
#            for element in b:
#                adj_list.insert_edge(element[0], element[1], element[2])
#        adj_list.draw()

    def is_path_connected(self, subset_of_edges):
        forest = djsf.DSF(len(self.al))
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
#        num_vertices = len(self.al)
#        subset_of_edges = htc.HashTableChain(len(self.al))
#        num_in_degrees = np.zeros(len(self.al), dtype = np.int)
#        new_subset_graph = Graph(len(self.al), weighted = self.weighted)
#        
#        while num_vertices > 0:
#            vertex_one = random.randint(0, len(self.al) - 1)
#            if len(self.al[vertex_one]) > 0:
#                vertex_two = random.randint(0, len(self.al[vertex_one]) - 1)
#                
#                random_edge = [vertex_one, self.al[vertex_one][vertex_two].dest, self.al[vertex_one][vertex_two].weight]
#                if subset_of_edges.insert(random_edge) == 1:
#                    if num_in_degrees[random_edge[0]] >= 2 or num_in_degrees[random_edge[1]] >= 2:
#                        return None, None, None
#                    num_in_degrees[random_edge[0]] += 1
#                    num_in_degrees[random_edge[1]] += 1
#                    
#                    new_subset_graph.insert_edge(random_edge[0], random_edge[1], random_edge[2])
#                    
#                    num_vertices -= 1    
#        return new_subset_graph, subset_of_edges, num_in_degrees, 
#            
#            
#    def randomized_hamiltonian(self, test_trials = 1000):
#        for i in range(test_trials):
#            subset_graph, subset_of_edges, in_degrees = self.generate_random_subset()
#            
#            if not subset_graph is None:
#                if self.correct_num_in_degrees(in_degrees) and self.is_path_connected(subset_of_edges.bucket):
#                    return subset_graph, subset_of_edges
#        return None, None
   
    def generate_random_subset(self):
        num_vertices = len(self.al)
        
        edges_hash_table = htc.HashTableChain(len(self.al))
        forest = djsf.DSF(len(self.al))
        
        num_in_degrees = np.zeros(len(self.al), dtype = np.int)
        subset_graph = Graph(len(self.al), weighted = self.weighted)
        
        while num_vertices > 0:
            vertex_one = random.randint(0, len(self.al) - 1)
            if len(self.al[vertex_one]) > 0:
                vertex_two = random.randint(0, len(self.al[vertex_one]) - 1)
                
                random_edge = [vertex_one, self.al[vertex_one][vertex_two].dest, self.al[vertex_one][vertex_two].weight]
                
                # Ensures that the random edge has not already been inserted into the subgraph.
                if edges_hash_table.insert(random_edge) == 1:
                    
                    # If the edges create a cycle and the expected amount of edges have
                    # not been reached, then the subset is not a hamiltonian path.
                    if forest.union(random_edge[0], random_edge[1]) == -1:
                        if num_vertices > 1:
                            return None, None, None
                    
                    # If the number of indegrees for the edges is greater
                    # than two, then the graph is not a hamiltonian cycle.
                    if num_in_degrees[random_edge[0]] >= 2 or num_in_degrees[random_edge[1]] >= 2:
                        return None, None, None
                    num_in_degrees[random_edge[0]] += 1
                    num_in_degrees[random_edge[1]] += 1
                    
                    subset_graph.insert_edge(random_edge[0], random_edge[1], random_edge[2])
                    num_vertices -= 1    
                    
        subset_edges = subset_graph.al_to_cycle()
        return subset_graph, subset_edges, num_in_degrees
    
    def al_to_cycle(self):
        prev_vertex = 0
        curr_vertex = self.al[0][1].dest
        cycle = [[self.al[0][0].dest, 0],[0, curr_vertex]]
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
     

#    def generate_random_subset(self):
#        num_vertices = len(self.al)
#        
#        edges_hash_table = htc.HashTableChain(len(self.al))
#        forest = djsf.DSF(len(self.al))
#        
#        num_in_degrees = np.zeros(len(self.al), dtype = np.int)
#        subset_graph = Graph(len(self.al), weighted = self.weighted)
#        subset_edges = []
#        
#        while num_vertices > 0:
#            vertex_one = random.randint(0, len(self.al) - 1)
#            if len(self.al[vertex_one]) > 0:
#                vertex_two = random.randint(0, len(self.al[vertex_one]) - 1)
#                
#                random_edge = [vertex_one, self.al[vertex_one][vertex_two].dest, self.al[vertex_one][vertex_two].weight]
#                
#                # Ensures that the random edge has not already been inserted into the subgraph.
#                if edges_hash_table.insert(random_edge) == 1:
#                    
#                    # If the edges create a cycle and the expected amount of edges have
#                    # not been reached, then the subset is not a hamiltonian path.
#                    if forest.union(random_edge[0], random_edge[1]) == -1:
#                        if num_vertices > 1:
#                            return None, None, None
#                    
#                    # If the number of indegrees for the edges is greater
#                    # than two, then the graph is not a hamiltonian cycle.
#                    if num_in_degrees[random_edge[0]] >= 2 or num_in_degrees[random_edge[1]] >= 2:
#                        return None, None, None
#                    num_in_degrees[random_edge[0]] += 1
#                    num_in_degrees[random_edge[1]] += 1
#                    
#                    subset_graph.insert_edge(random_edge[0], random_edge[1], random_edge[2])
#                    subset_edges.append([random_edge[0], random_edge[1]])
#                    
#                    num_vertices -= 1    
#        return subset_graph, subset_edges, num_in_degrees, 
#            
#            
#    def randomized_hamiltonian(self, test_trials = 1000):
#        for i in range(test_trials):
#            subset_graph, subset_of_edges, in_degrees = self.generate_random_subset()
#            
#            if not subset_graph is None:
#                if self.correct_num_in_degrees(in_degrees):
#                    return subset_graph, subset_of_edges
#        return None, None
    
    
#    def find_edge(self, source, target):
#        for edge in self.al[source]:
#            if edge.dest == target:
#                return True
#        return False
#
#    def backtracking_hamiltonian_recur(self, curr_vertex, forest, num_seen = 1):
#        if num_seen == len(self.al):
#            if self.find_edge(curr_vertex, 0):
#                return [0]
#            return None
#        
#        for edge in self.al[curr_vertex]:
#            if forest.parent[edge.dest] == -1 and forest.union(curr_vertex, edge.dest) == 1:
#                subset = self.backtracking_hamiltonian_recur(edge.dest, forest, num_seen + 1)
#                
#                if subset != None:
#                    
#                    subset.append(edge.dest)
#                    return subset
#                forest.parent[edge.dest] = -1
#        return None
#    
#    def backtracking_hamiltonian(self):
#        forest = djsf.DSF(len(self.al))
#        
#        subset = self.backtracking_hamiltonian_recur(0, forest)
#        if not subset is None:
#            subset.append(0)
#        print(subset)
#        return subset
        
    def find_edge(self, source, target):
        for edge in self.al[source]:
            if edge.dest == target:
                subset_graph = Graph(len(self.al), self.weighted, self.directed)
                subset_graph.insert_edge(edge.dest, source, edge.weight)
                return [[edge.dest, source]], subset_graph
        return None, None

    def backtracking_hamiltonian_recur(self, curr_vertex, forest, start_vertex, num_seen = 1):
        if num_seen == len(self.al):
            return self.find_edge(curr_vertex, start_vertex)
        
        for edge in self.al[curr_vertex]:
            if forest.parent[edge.dest] == -1 and forest.union(curr_vertex, edge.dest) == 1:
                subset, subset_graph = self.backtracking_hamiltonian_recur(
                        edge.dest, forest, start_vertex, num_seen + 1)
                
                if not subset is None:
                    subset.append([edge.dest, curr_vertex])
                    subset_graph.insert_edge(edge.dest, curr_vertex, edge.weight)
                    return subset, subset_graph
                forest.parent[edge.dest] = -1
        return None, None
    
    def backtracking_hamiltonian(self, start_vertex):
        forest = djsf.DSF(len(self.al))
        return self.backtracking_hamiltonian_recur(start_vertex, forest, start_vertex)
    
# BACKTRACKING WITHOUT VISITED AND ONLY RETURNING PATH 
#    def find_edge(self, source, target):
#        for edge in self.al[source]:
#            if edge.dest == target:
#                return True
#        return False
#
#    def backtracking_hamiltonian_recur(self, curr_vertex, forest, num_seen = 1):
#        if num_seen == len(self.al):
#            if self.find_edge(curr_vertex, 0):
#                return [[0]]
#            return None
#        
#        for edge in self.al[curr_vertex]:
#            if forest.parent[edge.dest] == -1 and forest.union(curr_vertex, edge.dest) == 1:
#                subset = self.backtracking_hamiltonian_recur(edge.dest, forest, num_seen + 1)
#                
#                if subset != None:
#                    if len(subset[0]) == 1:
#                        subset[0].append(edge.dest)
#                    subset.append([edge.dest, curr_vertex])
#                    return subset
#                forest.parent[edge.dest] = -1
#        return None
#    
#    def backtracking_hamiltonian(self):
#        forest = djsf.DSF(len(self.al))
#        subset = self.backtracking_hamiltonian_recur(0, forest)
#        return subset    

# BACKTRACKING USING VISITED
#    def backtracking_hamiltonian_recur(self, curr_vertex, visited, forest, num_seen = 1):
#        visited[curr_vertex] = True
#        
#        if num_seen == len(self.al):
#            if self.find_edge(curr_vertex, 0):
#                return [0]
#            return None
#        
#        for edge in self.al[curr_vertex]:
#            if not visited[edge.dest] and forest.union(curr_vertex, edge.dest) == 1:
#                subset = self.backtracking_hamiltonian_recur(edge.dest, visited, forest, num_seen + 1)
#                
#                if subset != None:
#                    
#                    subset.append(edge.dest)
#                    return subset
#                forest.parent[edge.dest] = -1
#                visited[edge.dest] = False
#        return None
#    
##    def subset_to_al_and_htc(self, subset):
##        new_subset_al = Graph(len(self.al), weighted = self.weighted)
##        path_of_edges = htc.HashTableChain(len(self.al))
##        for i in range(1, len(subset)):
##            path_of_edges.bucket[i].append(subset[i], subset[i - 1])
##            new_subset_al.insert_edge(subset[i], subset[i - 1])
##            if i == len(subset) - 1:
##                path_of_edges.bucket[i].append(subset[i], subset[0])
#    
#    def backtracking_hamiltonian(self):
#        visited = [False for i in range(len(self.al))]
#        forest = djsf.DSF(len(self.al))
#        
#        subset = self.backtracking_hamiltonian_recur(0, visited, forest)
#        if not subset is None:
#            subset.append(0)
#        return subset
            
        