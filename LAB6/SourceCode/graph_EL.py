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
import datetime
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
        
        # Saves the graph as a .png.
        fig.set_size_inches(15,9)
        title = "el_path" + datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        plt.savefig(title, dpi = 200)  
     
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
        discovered[start_vertex] = True
        frontier_queue = [start_vertex]
        path = np.zeros(self.vertices, dtype = np.int) - 1

        # Continues to iterate while the queue is not empty or until the end
        # vertex is not found.
        while len(frontier_queue) > 0:
            
            # Pops the current vertex.
            current_vertex = frontier_queue.pop(0)
            
            # Returns the path if the end vertex is found.
            if current_vertex == end_vertex:
                return self.interpret_path(path, current_vertex)
            
            # Pushes all adjacent vertices to the queue if the adjacent
            # vertex has not been discovered.
            for i in range(len(self.el)):
                
                # Since the edge list is ordered, the adjacent edges for an
                # undirected graph are only those whose source is less than or
                # equal to the current vertex.
                if not self.directed and self.el[i].source > current_vertex:
                    break
                
                # If the edge's source equals the current vertex and the edge 
                # destination has not been discovered, it is  pushed to the 
                # queue.
                if self.el[i].source == current_vertex and not discovered[self.el[i].dest]:
                    discovered[self.el[i].dest] = True
                    frontier_queue.append(self.el[i].dest)
                    path[self.el[i].dest] = current_vertex
                    
                # If the edge's destination equals the current vertex and the  
                # edge's source has not been discovered, it is pushed to the 
                # queue.
                elif not self.directed and self.el[i].dest == current_vertex and not discovered[self.el[i].source]:
                    discovered[self.el[i].source] = True
                    frontier_queue.append(self.el[i].source)
                    path[self.el[i].source] = current_vertex
                
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
    
    # Recursive function that performs depth first search based on the current and
    # end vertex.
    # Input: A list that keeps track of the visited vertices, the current vertex,
    #        the end vertex, and the current path.
    # Output: None
    def depth_first_search_recur(self,visited_vertices, current_vertex, end_vertex, curr_path):
        
        # If current_vertex matches the end_vertex, the current vertex is appended
        # to the curr_path and the recursive call ends.
        if current_vertex == end_vertex:
            curr_path.append(current_vertex)
            return
        
        # The current vertex is marked as visted.
        visited_vertices[current_vertex] = True
            
        # Recursive calls are made for each adjacent vertex.
        for i in range(len(self.el)):
            
            # Since the edge list is ordered, the adjacent edges for an
            # undirected graph are only those whose source is less than or
            # equal to the current vertex.
            if not self.directed and self.el[i].source > current_vertex:
                return
            
            # If the edge's source matches the current vertex a recursive
            # call is made with the edge's destination.
            if self.el[i].source == current_vertex and not visited_vertices[self.el[i].dest]:
                self.depth_first_search_recur(visited_vertices, 
                                          self.el[i].dest, end_vertex, curr_path)
                
            # If the  graph is not directed and the edge's destination
            # matches the current vertex a recursive call is made with the
            # edge's source.
            elif not self.directed and self.el[i].dest == current_vertex and not visited_vertices[self.el[i].source]:
                self.depth_first_search_recur(visited_vertices, 
                                          self.el[i].source, end_vertex, curr_path)
                
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