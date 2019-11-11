# Course: CS2302 Data Structures
# Date of Last Modification: October 31, 2019
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
import graph_AM as am
import graph_EL as el
from scipy.interpolate import interp1d

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
#             draw_path, breadth first search, and depth first search.  
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
        print("Please completely close the graph when done to continue the program.")
        plt.show(block = True)
    
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
                if (i, edge.dest) in set_of_edges or (edge.dest, i) in set_of_edges:
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
        print("Please completely close the graph when done to continue the program.")
        plt.show(block = True)
    
    # Converts the current adjacency list into an edge list.
    # Input: None
    # Output: The edge list created based off the current adjacency list.
    def as_EL(self):
        
        # Creates the edge list.
        edge_list = el.Graph(len(self.al),self.weighted, self.directed)
        for i in range(len(self.al)):
            for edge in self.al[i]:
                if self.directed or edge.dest > i:
                    edge_list.insert_edge(i, edge.dest, edge.weight)
        return edge_list
    
    # Converts the current adjacency list into an adjacency matrix.
    # Input: None
    # Output: The adjacency matrix created based off the current adjacency list.
    def as_AM(self):
        
        # Creates the adjacency matrix.
        adj_matrix = am.Graph(len(self.al), self.weighted, self.directed)
        for i in range(len(self.al)):
            for edge in self.al[i]:
                if self.directed or edge.dest > i:
                    adj_matrix.insert_edge(i, edge.dest, edge.weight)
        return adj_matrix
    
    # Converts the current adjacency list into an adjacency list.
    # Input: None
    # Output: Returns the current instance of the adjacnecy list.
    def as_AL(self):
        return self

    # Performs breadth first search on the current graph starting at start_vertex
    # and will terminate if a path to the end_vertex is found.
    # Input: The start and end vertex used in the breadth first search.
    # Output: The path from the start vertex to the end vertex if it exists.
    def breadth_first_search(self, start_vertex, end_vertex):
        
        # Ensures that start_vertex and end_vertex are within the bounds of the
        # adjacency list.
        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
            print("Error, vertex is out of range.")
            return
        
        # Creates a queue that will store the paths and the next vertex to be
        # visited. Discovered keeps track of the discovered vertices.
        discovered = [False for i in range(len(self.al))]
        frontier_queue = [[start_vertex]]

        # Continues to iterate while the queue is not empty or until the end
        # vertex is not found.
        while len(frontier_queue) > 0:
            
            # Pops the path with the current vertex as the last most
            # element.
            current_vertex_path = frontier_queue.pop(0)
            
            # Returns the path if the end vertex is found.
            if current_vertex_path[-1] == end_vertex:
                return current_vertex_path
            
            # Pushes all adjacent vertices to the queue if the adjacent
            # vertex has not been discovered.  The adjacent vertex is appended
            # to the current_vertex path and is pushed.
            for adj_vertex in self.al[current_vertex_path[-1]]:
                if not discovered[adj_vertex.dest]:
                    discovered[adj_vertex.dest] = True
                    frontier_queue.append(current_vertex_path + [adj_vertex.dest])
        return []
    
    # Recursive function that performs depth first search based on the current and
    # end vertex.
    # Input: A list that keeps track of the visisted vertices, the current vertex,
    #        the end vertex, and the current path.
    # Output: None
    def depth_first_search_recur(self,visited_vertices, current_vertex, end_vertex, curr_path):
        
        # If current_vertex matches the end_vertex, the current vertex is appended
        # to the curr_path and the recursive call ends.
        if current_vertex == end_vertex:
            curr_path.append(current_vertex)
            return

        # If the current_vertex has not been visited, then a recursive call
        # is made for each adjacent vertex.
        if not visited_vertices[current_vertex]:
            visited_vertices[current_vertex] = True
            for edge in self.al[current_vertex]:
                self.depth_first_search_recur(visited_vertices, 
                                              edge.dest, end_vertex, curr_path)
                
                # Checks curr_path after each recursive call. If the last element
                # has been found, the the current vertex is prepended and ends
                # the recursive call.
                if len(curr_path) > 0 and curr_path[-1] == end_vertex:
                    curr_path.insert(0, current_vertex)
                    return

    # Function that intiates depth first search.
    # Input: The start and end vertex that will be used for the depth first search.
    # Output: The path, if found, from start_vertex to end_vertex.   
    def depth_first_search(self, start_vertex, end_vertex):
        
        # Ensures that start_vertex and end_vertex are within the bounds of the
        # adjacency matrix.
        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
            print("Error, vertex is out of range.")
            return
        
        # Creates the visisted_vertices list that will keep track of the vertices
        # visited.
        visited_vertices = [False for i in range(len(self.al))]
        curr_path = []

        # Performs the depth first search.
        self.depth_first_search_recur(visited_vertices, start_vertex, end_vertex, curr_path)
        return curr_path