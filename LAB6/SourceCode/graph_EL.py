# Course: CS2302 Data Structures
# Date of Last Modification: October 31, 2019
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
from scipy.interpolate import interp1d

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
#             draw_path, breadth first search, and depth first search.        
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
    
    # Function that inserts the edge between the source and dest by adding the
    # edge to the edge list.
    # Input: The source, destination, and weight of the edge.
    # Output: None.
    def insert_edge(self,source,dest,weight=1):
        
        # Ensures that the source and dest are not out of bounds.
        if source >= self.vertices or dest >= self.vertices or source < 0 or dest < 0:
            print("Error, vertex is out of range.")
        
        # Ensures that if the graph is not weighted then the weight must be 1.
        elif weight != 1 and not self.weighted:
            print('Error, inserting weighted edge to unweighted graph')
            
        # Inserts an Edge object populated with the source, dest, and weight.
        else:
            self.el.append(Edge(source, dest, weight))
    
    # Helper function that deletes the edge between the source and dest.
    # Input: The source and destination that form the edge.
    # Output: Returns True if the edge was successfully removed. False otherwise.
    def delete_edge_(self, source, dest):
        i = 0
        for edge in self.el:
            
            # If the edge's source and destination match source and destination, 
            # the edge is removed.
            if edge.source == source and edge.dest == dest:
                self.el.pop(i)
                return True
            
            # If the graph is not directed and the edge's destination and source
            # match source and destination, then the edge is removed.
            elif not self.directed and edge.dest == source and edge.source == dest:
                self.el.pop(i)
                return True
            i += 1
        return False
    
    # Function that deletes the edge between the source and dest.
    # Input: The source and destination that form the edge.
    # Output: None.
    def delete_edge(self, source, dest):
        deleted = self.delete_edge_(source, dest)
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
        print("Please completely close the graph when done to continue the program.")
        plt.show(block = True)
     
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
            if (edge.source, edge.dest) in set_of_edges or (edge.dest, edge.source) in set_of_edges:
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
        print("Please completely close graph when done to continue the program.")
        plt.show(block = True)   
     
    # Converts the current edge list into an edge list.
    # Input: None
    # Output: Returns the current instance of the edge list.
    def as_EL(self):
        return self
    
    # Converts the current edge list into an adjacency matrix.
    # Input: None
    # Output: The adjacency matrix created based off the current edge list.    
    def as_AM(self):
        adj_matrix = am.Graph(self.vertices, self.weighted, self.directed)
        
        # Iterates through the edge list and adds each edge.
        for edge in self.el:
            adj_matrix.insert_edge(edge.source, edge.dest, edge.weight)
        return adj_matrix
    
    # Converts the current edge list into an adjacency list.
    # Input: None
    # Output: The adjacency list created based off the current edge list.
    def as_AL(self):
        adj_list = al.Graph(self.vertices, self.weighted, self.directed)
        
        # Iterates through the edge list and adds each edge.
        for edge in self.el:
            adj_list.insert_edge(edge.source, edge.dest, edge.weight)
        return adj_list 
        
    # Performs breadth first search on the current graph starting at start_vertex
    # and will terminate if a path to the end_vertex is found.
    # Input: The start and end vertex used in the breadth first search.
    # Output: The path from the start vertex to the end vertex if it exists.    
    def breadth_first_search(self, start_vertex, end_vertex):
        
        # Ensures that start_vertex and end_vertex are valid vertices.
        if start_vertex >= self.vertices or end_vertex >= self.vertices or start_vertex < 0 or end_vertex < 0:
            print("Error, vertex is out of range.")
            return
        
        # Creates a queue that will store the paths and the next vertex to be
        # visited. Discovered keeps track of the discovered vertices.
        discovered = [False for i in range(self.vertices)]
        frontier_queue = [[start_vertex]]

        # Continues to iterate while the queue is not empty or until the end
        # vertex is not found.
        while len(frontier_queue) > 0:
            current_vertex_path = frontier_queue.pop(0)
            
            # Pops the path with the current vertex as the last most element.
            if current_vertex_path[-1] == end_vertex:
                return current_vertex_path
            
            # Pushes all adjacent vertices to the queue if the adjacent
            # vertex has not been discovered.  The adjacent vertex is appended
            # to the current_vertex path and pushed.
            for edge in self.el:
                
                # If the edge's source equals the current vertex and the edge 
                # destination has not been discovered, it is appended to the 
                # current vertex path and pushed to the queue.
                if edge.source == current_vertex_path[-1] and not discovered[edge.dest]:
                    discovered[edge.dest] = True
                    frontier_queue.append(current_vertex_path + [edge.dest])
                    
                # If the edge's destination equals the current vertex and the  
                # edge's source has not been discovered, it is appended to the 
                # current vertex path and pushed to the queue.
                elif not self.directed and edge.dest == current_vertex_path[-1] and not discovered[edge.source]:
                    discovered[edge.source] = True
                    frontier_queue.append(current_vertex_path + [edge.source])
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

        # If the current_vertex has not been visisted, then a recursive call
        # is made with for each adjacent vertex.
        if not visited_vertices[current_vertex]:
            visited_vertices[current_vertex] = True

            for edge in self.el:
                
                # If the edge's source matches the current vertex a recursive
                # call is made with the edge's destination.
                if edge.source == current_vertex:
                    self.depth_first_search_recur(visited_vertices, 
                                              edge.dest, end_vertex, curr_path)
                    
                # If the  graph is not directed and the edge's destination
                # matches the current vertex a recursive call is made with the
                # edge's source.
                elif not self.directed and edge.dest == current_vertex:
                    self.depth_first_search_recur(visited_vertices, 
                                              edge.source, end_vertex, curr_path)
                    
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
        
        # Ensures that start_vertex and end_vertex are valid vertices.
        if start_vertex >= self.vertices or end_vertex >= self.vertices or start_vertex < 0 or end_vertex < 0:
            print("Error, vertex is out of range.")
            return
        
        # Creates the visisted_vertices list that will keep track of the vertices
        # visited.
        visited_vertices = [False for i in range(self.vertices)]
        curr_path = []
        
        # Performs the depth first search.
        self.depth_first_search_recur(visited_vertices, start_vertex, end_vertex, curr_path)
        return curr_path        