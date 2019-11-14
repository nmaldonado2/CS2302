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
import graph_AL as al
import graph_EL as el
import datetime
from scipy.interpolate import interp1d

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
                    if (i, j) in set_of_edges or (j, i) in set_of_edges:
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
    
    # Populates a directed graph passed in as a parameter based off the edges in
    # the current graph.
    # Input: The directed graph to be populated.
    # Output: None.
    def convert_directed_graph(self, graph):
        
        # Iterates through the entire adjacency matrix and only inserts edges
        # if the matrix does not have a negative one in the cell.
        for i in range(len(self.am)):
                for j in range(i, len(self.am[i])):
                    if self.am[i][j] != -1:
                        if graph.representation == "AL":
                            graph.insert_edge(i, j, self.am[i][j])
                            
                        # Since the adjacency matrix naturally orders the edges,
                        # they are simply appended to the edge list.
                        elif graph.representation == "EL":
                            graph.el.append(el.Edge(i, j, self.am[i][j]))
    
    # Populates an undirected graph passed in as a parameter based off the edges
    # in the current graph.
    # Input: The undirected graph to be populated.
    # Output: None.
    def convert_undirected_graph(self, graph):
        
        # Iterates through all elements right of the matix's diagonal line and
        # only inserts edges if the matrix does not have a negative one in the
        # cell.
        for i in range(len(self.am)):
                for j in range(i, len(self.am)):
                    if self.am[i][j] != -1:
                        if graph.representation == "AL":
                            graph.insert_edge(i, j, self.am[i][j])
                            
                        # Since the adjacency matrix naturally orders the edges,
                        # they are simply appended to the edge list.
                        elif graph.representation == "EL":
                            graph.el.append(el.Edge(i, j, self.am[i][j]))
    
    # Converts the current adjacency matrix into an edge list.
    # Input: None
    # Output: The edge list created based off the current adjacency matrix.
    def as_EL(self):
        
        # Creates the edge list.
        edge_list = el.Graph(len(self.am), self.weighted, self.directed)
        if self.directed:
            self.convert_directed_graph(edge_list)
        else:
            self.convert_undirected_graph(edge_list)
        return edge_list    
    
    # Converts the current adjacency matrix into an adjacency matrix.
    # Input: None
    # Output: Returns the current instance of the adjacnecy matrix.
    def as_AM(self):
        return self
    
    # Converts the current adjacency matrix into an adjacency list.
    # Input: None
    # Output: The adjacency list created based off the current adjacency matrix.
    def as_AL(self):
        
        # Creates the adjacency list.
        adj_list = al.Graph(len(self.am), self.weighted, self.directed)
        if self.directed:
            self.convert_directed_graph(adj_list)
        else:
            self.convert_undirected_graph(adj_list)
        return adj_list
    
    
    
    # Performs breadth first search on the current graph starting at start_vertex
    # and will terminate if a path to the end_vertex is found.
    # Input: The start and end vertex used in the breadth first search.
    # Output: The path from the start vertex to the end vertex if it exists.
    def breadth_first_search(self, start_vertex, end_vertex):
        
        # Ensures that start_vertex and end_vertex are within the bounds of the
        # adjacency matrix.
        if start_vertex >= len(self.am) or end_vertex >= len(self.am) or start_vertex < 0 or end_vertex < 0:
            print("Error, vertex is out of range.")
            return
        
        # Creates a queue that will store the paths and the next vertex to be
        # visited. Discovered keeps track of the discovered vertices.
        discovered = [False for i in range(len(self.am))]
        discovered[start_vertex] = True
        frontier_queue = [start_vertex]
        path = np.zeros(len(self.am), dtype = np.int) - 1
        
        # Continues to iterate while the queue is not empty or until the end
        # vertex is not found.
        while len(frontier_queue) > 0:
            
            # Pops the current vertex
            current_vertex = frontier_queue.pop(0)
            
            # Returns the path if the end vertex is found.
            if current_vertex == end_vertex:
                return self.interpret_path(path, current_vertex)
            
            # Pushes all adjacent vertices to the queue if the adjacent
            # vertex has not been discovered.
            for am_column in range(len(self.am[current_vertex])):
                if self.am[current_vertex][am_column] != -1 and not discovered[am_column]:
                    discovered[am_column] = True
                    frontier_queue.append(am_column)
                    path[am_column] = current_vertex
        return []

    # Function that traces a path that for each index has the previous vertex
    # from the path created by BFS ending at current_vertex.
    # Input: A path from BFS that has the previous vertex that came before
    #        the vertex represented by the current vertex.  If there was not a
    #        previous vertex, then -1 is located at the index.
    # Output: A path to the current vertex from the origin created by BFS.
    def interpret_path(self, path, current_vertex):
        if path[current_vertex] == -1:
            return [current_vertex]
        return self.interpret_path(path, path[current_vertex]) + [current_vertex]

    # Recursive function that performs depth first search based on the current 
    # and end vertex.
    # Input: A list that keeps track of the visisted vertices, the current
    #        vertex, the end vertex, and the current path.
    # Output: None
    def depth_first_search_recur(self,visited_vertices, current_vertex, end_vertex, curr_path):
        
        # If current_vertex matches the end_vertex, the current vertex is 
        # appended to the curr_path and the recursive call ends.
        if current_vertex == end_vertex:
            curr_path.append(current_vertex)
            return
        
        # Marks current_vertex as visited.
        visited_vertices[current_vertex] = True
            
        # Makes recursive calls for each adjacent vertex.
        for am_column in range(len(self.am[current_vertex])):
            if self.am[current_vertex][am_column] != -1 and not visited_vertices[am_column]:
                self.depth_first_search_recur(visited_vertices, 
                                              am_column, end_vertex, curr_path)
                
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
        if start_vertex >= len(self.am) or end_vertex >= len(self.am) or start_vertex < 0 or end_vertex < 0:
            print("Error, vertex is out of range.")
            return
        
        # Creates the visisted_vertices list that will keep track of the vertices
        # visited.
        visited_vertices = [False for i in range(len(self.am))]
        curr_path = []
        
        # Performs the depth first search.
        self.depth_first_search_recur(visited_vertices, start_vertex, end_vertex, curr_path)
        return curr_path