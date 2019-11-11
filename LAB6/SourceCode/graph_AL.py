# Adjacency list representation of graphs
import numpy as np
import matplotlib.pyplot as plt
import math
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
#    def breadth_first_search(self, v):
#        if v >= len(self.al) or v < 0:
#            print("Error, vertex is out of range.")
#            return
#        frontier_queue = []
#        discovered_elements = []
#        
#        frontier_queue.append(self.al[v])
#        discovered_elements.append(v)
#        prev = [[-1] for i in range(len(self.al))]
#        
#        while len(frontier_queue) > 0:
#            current_vertex = frontier_queue.pop(0)
#            for adj_vertex in current_vertex:
#                if not adj_vertex.dest in discovered_elements:
#                    discovered_elements.append(adj_vertex.dest)
#                    prev[adj_vertex.dest] = 
#                    frontier_queue.append(self.al[adj_vertex.dest])
#        print(discovered_elements)
#        return discovered_elements
        
    
#    def breadth_first_search_recur(self, frontier_queue, discovered_elements, 
#                                   path_of_paths, current_path, end_vertex):
#        if len(frontier_queue) < 1:
#            return
#        current_vertex = frontier_queue.pop(0)
#        if current_vertex[1] == end_vertex:
#            path_of_paths.append([current_path + [current_vertex[1]]])
#            return
#        
#        for adj_vertex in current_vertex[0]:
#                if not adj_vertex.dest in discovered_elements:
#                    new_frontier = [[self.al[adj_vertex.dest], adj_vertex.dest]] + frontier_queue
#                    new_discovered = discovered_elements + [adj_vertex.dest]
#                    self.breadth_first_search_recur(new_frontier, new_discovered, path_of_paths,
#                                                    current_path + [current_vertex[1]], end_vertex)   
    
#    def breadth_first_search_recur(self, frontier_queue, discovered_elements, 
#                                   path_of_paths, current_path, end_vertex):
#        if len(frontier_queue) < 1:
#            return
#        current_vertex = frontier_queue.pop(0)
#        if current_vertex == end_vertex:
#            path_of_paths.append([current_path + [current_vertex]])
#            return
#        
#        for adj_vertex in self.al[current_vertex]:
#                if not adj_vertex.dest in discovered_elements:
#                    new_frontier = [adj_vertex.dest] + frontier_queue
#                    new_discovered = discovered_elements + [adj_vertex.dest]
#                    self.breadth_first_search_recur(new_frontier, new_discovered, path_of_paths,
#                                                    current_path + [current_vertex], end_vertex) 
#    
#        
#    def breadth_first_search_helper(self, v):
#        if v >= len(self.al) or v < 0:
#            print("Error, vertex is out of range.")
#            return
#        frontier_queue = []
#        discovered_elements = []
#        
##        frontier_queue.append([self.al[v], v])
#        frontier_queue.append(v)
#        discovered_elements.append(v)
#        
#        path_of_paths = []
#        
#        self.breadth_first_search_recur(frontier_queue, discovered_elements, path_of_paths, [], 15)
#        print(path_of_paths)
    
#    def breadth_first_search(self, v):
#        if v >= len(self.al) or v < 0:
#            print("Error, vertex is out of range.")
#            return
#        frontier_queue = []
#        discovered_elements = []
#        
#        frontier_queue.append([self.al[v], v])
#        discovered_elements.append(v)
#        prev = [[] for i in range(len(self.al))]
#        count = 0
#        while len(frontier_queue) > 0:
#            count += 1
#            current_vertex = frontier_queue.pop(0)
#            for adj_vertex in current_vertex[0]:
##                if adj_vertex.dest > current_vertex[1] or not adj_vertex.dest in discovered_elements:
#                if not adj_vertex.dest in prev[current_vertex[1]]:
#                    prev[adj_vertex.dest].append(current_vertex[1])
#                if not adj_vertex.dest in discovered_elements:
#                    discovered_elements.append(adj_vertex.dest)
#                    
#                    frontier_queue.append([self.al[adj_vertex.dest], adj_vertex.dest])
#        print(count)
#        print(discovered_elements)
#        print()
#        print(prev)
#        path_of_paths = []
#        self.interpret_results(prev, [], path_of_paths, 15)
#        print(path_of_paths)
#        return discovered_elements
    
# FINDS ALL VALUES: KEEP IF SHE WANTS ALL
#    def breadth_first_search(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
#        frontier_queue = [[start_vertex]]
#        path_of_paths = []
#        
#        while len(frontier_queue) > 0:
#            discovered = frontier_queue.pop(0)
#            
#            if discovered[-1] == end_vertex:
#                path_of_paths.append(discovered)
#            
#            for adj_vertex in self.al[discovered[-1]]:
#                if not adj_vertex.dest in discovered:
#                    frontier_queue.append(discovered + [adj_vertex.dest])
#        return path_of_paths

# POPS PATH TO QUEUE: USE IF ALL ELSE FAILS
#    def breadth_first_search(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
#        frontier_queue = [[start_vertex]]
#        
#        while len(frontier_queue) > 0:
#            discovered = frontier_queue.pop(0)
#            
#            if discovered[-1] == end_vertex:
#                return discovered
#            
#            for adj_vertex in self.al[discovered[-1]]:
#                if not adj_vertex.dest in discovered:
#                    frontier_queue.append(discovered + [adj_vertex.dest])
#        return []
    
#    def breadth_first_search(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
#        if start_vertex > end_vertex:            
#            vertex_index = end_vertex
#        else:
#            vertex_index = start_vertex
#        
#        discovered = [False for i in range(len(self.al))]
#        frontier_queue = [[start_vertex]]
#
#        while len(frontier_queue) > 0:
#            current_vertex_path = frontier_queue.pop(0)
#            
#            if current_vertex_path[-1] == end_vertex:
#                return current_vertex_path
#            
#            for adj_vertex in self.al[current_vertex_path[-1]]:
#                if not discovered[adj_vertex.dest - vertex_index]:
#                    discovered[adj_vertex.dest - vertex_index] = True
#                    frontier_queue.append(current_vertex_path + [adj_vertex.dest])
#        return []

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

    
#    def breadth_first_search(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        frontier_queue = []
#        discovered_elements = []
#        
#        frontier_queue.append(start_vertex)
#
#        prev = [[] for i in range(len(self.al))]
#        while len(frontier_queue) > 0:
#            current_vertex = frontier_queue.pop(0)
#            # We can't do this right because then 15 could point to 4 which points to 0
#            if current_vertex != 15:
#                for adj_vertex in self.al[current_vertex]:
#                    
#                    # If we have not seen the vertex, add it to the queue.
#                    if adj_vertex.dest != start_vertex and len(prev[adj_vertex.dest]) == 0:
#                        frontier_queue.append(adj_vertex.dest)
#    
#                    if not adj_vertex.dest in prev[current_vertex]:
#                        prev[adj_vertex.dest].append(current_vertex)
#
#        print(discovered_elements)
#        print()
#        print(prev)
#        path_of_paths = []
#        self.interpret_results(prev, [], path_of_paths, end_vertex, start_vertex)
#        print(path_of_paths)
#        return path_of_paths
#    
#    def interpret_results(self, prev, path, path_of_paths, i, start_vertex):
#        if i == start_vertex:
#            path_of_paths.append([i] + path)
#            return
#        if len(prev[i]) == 0:
#            return 
#        for j in range(len(prev[i])):
#            self.interpret_results(prev, [i] + path, path_of_paths, prev[i][j], start_vertex)
    
#    def breadth_first_search_shortest_path(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        frontier_queue = []
#        frontier_queue.append(start_vertex)
#        prev = [[] for i in range(len(self.al))]
#        
#        while len(frontier_queue) > 0:
#            current_vertex = frontier_queue.pop(0)
#            # We can't do this right because then 15 could point to 4 which points to 0
##            if current_vertex != end_vertex:
##                for adj_vertex in self.al[current_vertex]:
#            for adj_vertex in self.al[current_vertex]:
#
#                
#                # If we have not seen the vertex, add it to the queue.
#                if adj_vertex.dest != start_vertex and len(prev[adj_vertex.dest]) == 0:
#                    frontier_queue.append(adj_vertex.dest)
#
#                if not adj_vertex.dest in prev[current_vertex]:
#                    prev[adj_vertex.dest].append(current_vertex)
#        print(prev)
#        path_of_paths = []
#        self.interpret_results(prev, [], path_of_paths, end_vertex, start_vertex)
#        return path_of_paths
    
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
 
#  NEXT TWO KEEP IF SHE WANTS ALL PATHS BFS
#    def depth_first_search(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
#        visited_vertices = []
#        path_of_paths = []
#        if start_vertex > end_vertex:
#            vertex_index = end_vertex
#        else:
#            vertex_index = start_vertex
#        self.depth_first_search_recur(visited_vertices, path_of_paths,start_vertex, end_vertex, [], vertex_index)
#        return path_of_paths
#    def depth_first_search_recur(self,visited_vertices, path_of_paths, current_vertex, terminating_vertex, curr_path):
#        if current_vertex == terminating_vertex:
#            path_of_paths.append(curr_path + [current_vertex])
#            return
#        
#        visited_vertices.append(current_vertex)
#        
#        curr_path = curr_path + [current_vertex]
#        for edge in self.al[current_vertex]:
#
#            if not edge.dest in  visited_vertices:
#                self.depth_first_search_recur(visited_vertices, path_of_paths, 
#                                              edge.dest, terminating_vertex, curr_path)
#        visited_vertices.remove(current_vertex)
##        curr_path.pop(0)
    
    
#    def depth_first_search_single_recur(self,visited_vertices, current_vertex, terminating_vertex, curr_path):
#        if current_vertex == terminating_vertex:
#            return curr_path + [current_vertex]
#        
#        visited_vertices.append(current_vertex)
#        curr_path = curr_path + [current_vertex]
#        for edge in self.al[current_vertex]:
#            if not edge.dest in  visited_vertices:
#                path = self.depth_first_search_single_recur(visited_vertices, 
#                                              edge.dest, terminating_vertex, curr_path)
#                if path[-1] == terminating_vertex:
#                    return path
#        visited_vertices.remove(current_vertex)
#        curr_path.pop(0)
#        return curr_path
#    
#    def depth_first_search_single_path(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
##        visited_vertices = []
#        
#        return self.depth_first_search_single_recur([], start_vertex, end_vertex, [])
        

    
#    def depth_first_search_single_path(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
#        visited_vertices = []
#        stack_vertices = []
#        stack_vertices.append(start_vertex)
#        prev = [[] for i in range(len(self.al))]
#        
#        while len(stack_vertices) > 0:
#            current_vertex = stack_vertices.pop()
#            if current_vertex == end_vertex:
#                break
#            if not current_vertex in visited_vertices:
#                visited_vertices.append(current_vertex)
#                for adj_vertex in self.al[current_vertex]:
#                    if not adj_vertex.dest in prev[current_vertex]:
#                        prev[adj_vertex.dest].append(current_vertex)                        
#                    stack_vertices.append(adj_vertex.dest)
#                
#        print(visited_vertices)
#        print(prev)
#        print()
#        path_of_paths = []
#        self.interpret_results(prev, [], path_of_paths, end_vertex, start_vertex)
#        return path_of_paths
    
    
#    def depth_first_search(self, start_vertex, end_vertex):
#        if start_vertex >= len(self.al) or end_vertex >= len(self.al) or start_vertex < 0 or end_vertex < 0:
#            print("Error, vertex is out of range.")
#            return
#        
#        visited_vertices = []
#        stack_vertices = []
#        stack_vertices.append(start_vertex)
#        prev = [[] for i in range(len(self.al))]
#        
#        while len(stack_vertices) > 0:
#            current_vertex = stack_vertices.pop()
#            if current_vertex == end_vertex:
#                break
#            if not current_vertex in visited_vertices:
#                visited_vertices.append(current_vertex)
#                for edge in self.al[current_vertex]:
#                    if not edge.dest in prev[current_vertex]:
#                        prev[edge.dest].append(current_vertex)                        
#                    stack_vertices.append(edge.dest)
#                
#        print(visited_vertices)
#        print(prev)
#        print()
#        path_of_paths = []
#        self.interpret_results(prev, [], path_of_paths, end_vertex)
#        print(path_of_paths)
#        return visited_vertices
        
    