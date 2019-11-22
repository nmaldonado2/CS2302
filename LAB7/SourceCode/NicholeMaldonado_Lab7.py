import graph_AL as al
import graph_AM as am
import graph_EL as el
import random
import HashTable as ht
import time
import sys




#g = al.Graph(5)
#g.insert_edge(0,2)
#g.insert_edge(0,1)
#g.insert_edge(1,2)
#g.insert_edge(1,4)
#g.insert_edge(2,4)
#g.insert_edge(2,3)
#g.insert_edge(3,4)
#g.draw()
#
##g2, subset_of_edges = g.randomized_hamiltonian()
#
#g.backtracking_hamiltonian()
##try:
##if not subset_of_edges is None:
###        g.draw()
##    g.draw_path(subset_of_edges)
##    g2.draw()
##    g2.display()
##except:
##    print("No path")


# Function that returns the graph type based on the graph representation.
# Input: A string of characters that is either "AL", "AM", or "EL".
# Output: A string of the graph type based on the graph's representation.
def representation_to_text(representation):
    if representation == "AL":
        return "Adjacency List"
    if representation == "EL":
        return "Edge List"
    return "Adjacency Matrix"

# Function that displays the graphs and prints the graph if designated by the
# boolean draw_graph.
# Input: The graph to be displayed and a boolean that signifies if the graph
#        fwill be drawn
# Output: None, other than the graph will be displayed and potentially drawn.
def display_graph(graph, draw_graph):
    graph_type = representation_to_text(graph.representation)
    print(graph_type, ":")
    graph.display()
    print()
    if draw_graph:
        print("Graph based on the", graph_type, end = " ")
        print("will be stored in the current directory.\n")
        graph.draw()
        print()

# Function that allows for a list containing graphs to be displayed.
# Input: A 1D list that contains the graphs that will be displayed.
# Output: None.
def display_all_graphs(list_of_graphs, draw_graphs):
    for graph in list_of_graphs:
        display_graph(graph, draw_graphs)

# Creates a hash table with edge combinations based on the number of edges
# needed. Each edge's source vertex will be hashed based on the vertex number.
# Only non-duplicate edges are hashed to the table.
# Input: The number of vertices the graph will have and the number of edges
#        that need to be hashed to the table.
# Output: A list of the hash table with linear chaining's buckets.
def compute_edge_combos(num_vertices, num_edges, edges_hash_table):
    i = 0
    while i != num_edges:
        
        # Creates random vertices and weights.
        vertex_one = random.randint(0,num_vertices - 1)
        vertex_two = random.randint(0, num_vertices - 1)
        weight = random.randint(1,99)
        
        # Hashes the edge to the table. If the insertion is successful, then
        # i is incremented.
        if vertex_one != vertex_two:
            if edges_hash_table.insert([vertex_one, vertex_two, weight]) != -1:
                i += 1

def randomization_test(list_of_graphs, print_edges, small_graph):
    
    # Runs the tests for breadth first search for each graph.
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        print(graph_type, ":")
        start_time = time.perf_counter()
        subset_graph, subset_edges = graph.randomized_hamiltonian()
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))
        
        if print_edges:
            print("Edges:", subset_edges, "\n")

            if small_graph and not subset_graph is None:
                subset_graph.draw()
        else:
            print()



# Function that initiates the tests for the graphs' display.
# Input: The size of graphs to be created.
# Output: None     
def run_automated_randomization(graph_size, print_graphs, small_graphs):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs_with_hamiltonian(graph_size)
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs Display")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0], small_graphs)
    randomization_test(list_of_graphs[0], print_graphs, small_graphs)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs Display")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1], small_graphs)
    randomization_test(list_of_graphs[1], print_graphs, small_graphs)
    
def backtracking_test(list_of_graphs, print_edges, small_graph, start_vertex):    
    # Runs the tests for breadth first search for each graph.
    for graph in list_of_graphs:
        graph_type = representation_to_text(graph.representation)
        print(graph_type, ":")
        start_time = time.perf_counter()
        cycle, subset_graph = graph.backtracking_hamiltonian(start_vertex)
        end_time = time.perf_counter()
        print("Runtime: %0.6f seconds"%(end_time - start_time))

        if print_edges:
            print("Cycle:", cycle)
            print()
            if small_graph and not subset_graph is None:
                print("The subset graph will be stored in the current directory.\n")
                subset_graph.draw()
            elif not subset_graph is None:
                print("Subset graph:")
                subset_graph.display()
                print()
        else:
            print()

# Function that initiates the tests for the graphs' display.
# Input: The size of graphs to be created.
# Output: None     
def run_automated_backtracking(graph_size, print_graphs, small_graphs):
    
    # Receives populated graphs.
    list_of_graphs = generate_test_graphs(graph_size)
    list_of_graphs_hamiltonian = generate_test_graphs_with_hamiltonian(graph_size)
    start_vertex = random.randint(0, graph_size - 1)
    print("For all tests, the start vertex is", start_vertex, end = ".\n")
    
    print("----------------------------------------------")
    print("|    Graphs with Known Hamiltonian Cycles    |")
    print("----------------------------------------------")
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs_hamiltonian[0], small_graphs)
    backtracking_test(list_of_graphs_hamiltonian[0], print_graphs, small_graphs, start_vertex)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs_hamiltonian[1], small_graphs)
    backtracking_test(list_of_graphs_hamiltonian[1], print_graphs, small_graphs, start_vertex)
    
    print("------------------------------------------------")
    print("|    Graphs with Unknown Hamiltonian Cycles    |")
    print("------------------------------------------------")
    
    # Runs tests for undirected graphs.
    print("\nUndirected Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[0], small_graphs)
    backtracking_test(list_of_graphs[0], print_graphs, small_graphs, start_vertex)
    
    # Runs tests for weighted graphs.
    print("\nWeighted Graphs")
    print("________________________________________________")
    if print_graphs:
        print("Current Graphs:",end = "\n")
        display_all_graphs(list_of_graphs[1], small_graphs)
    backtracking_test(list_of_graphs[1], print_graphs, small_graphs, start_vertex)

# Function that creates a list_of_graphs that contains four sublists of directed,
# undirected and weighted, undirected graphs.
# Input: the graph size to be created.
# Output: returns a list of populated undirected and weighted, undirected graphs.
#         represented as adjacency lists, adjacency matrics, and edge lists.
def generate_test_graphs(graph_size):
    edge_combos = ht.HashTableChain(graph_size)
    
    # Recieves combinations of valid edges.
    compute_edge_combos(graph_size, int(graph_size * 1.5), edge_combos)
    edge_combos = edge_combos.bucket
    
    list_of_graphs_undirected = [al.Graph(graph_size), am.Graph(graph_size), 
                                 el.Graph(graph_size)]
    list_of_graphs_weighted = [al.Graph(graph_size, True), 
                               am.Graph(graph_size, True),
                               el.Graph(graph_size, True)]
    
    # Creates lists of unpopulated graphs.
    list_of_graphs = [list_of_graphs_undirected, list_of_graphs_weighted]

    # Populates all the graphs with the edges from edge_combos.
    for i in range(len(list_of_graphs)):
        for j in range(len(list_of_graphs[i])):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i][j].weighted:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1])
    return list_of_graphs

def generate_hamiltonian_cycle(num_vertices):
    vertices_remaining = [i for i in range(num_vertices)]
    edges_hash_table = ht.HashTableChain(num_vertices)
    
    prior_vertex = random.randint(0, len(vertices_remaining) - 1)
    
    vertices_remaining[-1], vertices_remaining[prior_vertex] = vertices_remaining[prior_vertex], vertices_remaining[-1]
    first_vertex = vertices_remaining.pop(-1)

    while len(vertices_remaining) > 0:
        
        # Swap values to avoid popping and instead perform constant time removal.
        vertex_to_add = random.randint(0,len(vertices_remaining) - 1)
        vertices_remaining[-1], vertices_remaining[vertex_to_add] = vertices_remaining[vertex_to_add], vertices_remaining[-1]
        
        weight = random.randint(1,99)
        
        if edges_hash_table.insert([prior_vertex, vertices_remaining[-1], weight]) == 1:
            prior_vertex = vertices_remaining.pop(-1)
            
    edges_hash_table.insert([prior_vertex, first_vertex, random.randint(0,99)])
    
    compute_edge_combos(num_vertices, int(num_vertices * 1.5) - num_vertices - 1, edges_hash_table)
            
    return edges_hash_table.bucket

def generate_test_graphs_with_hamiltonian(graph_size):
    edge_combos = generate_hamiltonian_cycle(graph_size)
    
    list_of_graphs_undirected = [al.Graph(graph_size), am.Graph(graph_size), 
                                 el.Graph(graph_size)]
    list_of_graphs_weighted = [al.Graph(graph_size, True), 
                               am.Graph(graph_size, True),
                               el.Graph(graph_size, True)]
    
    # Creates lists of unpopulated graphs.
    list_of_graphs = [list_of_graphs_undirected, list_of_graphs_weighted]

    # Populates all the graphs with the edges from edge_combos.
    for i in range(len(list_of_graphs)):
        for j in range(len(list_of_graphs[i])):
            for bucket in edge_combos:
                for edge_pair in bucket:
                    if list_of_graphs[i][j].weighted:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1], edge_pair[2])
                    else:
                        list_of_graphs[i][j].insert_edge(edge_pair[0], edge_pair[1])
    return list_of_graphs

# Function that allows users to select which graph function they would like
# to test on selected graph sizes.
# Input: None
# Output: None
def automated_test_setup():
    print("Select a function to test")
    print("1. Randomization Hamiltonian Path")
    print("2. Backtracking Hamiltonian Path")
    print("3. Dynamic Programming Instance Function")
    
    menu = int(input("Select 1, 2, or 3: "))
    print()
    if menu >= 1 and menu <= 3:
        
        if menu == 1:
            # Prompts users to select the graph size to be tested.
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 500 vertices and 150 edges")
            print("3. 1000 vertices and 750 edges")
            print("4. 10000 vertices and 1500 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 500, 1000, 10000]
        if menu == 2:
                        # Prompts users to select the graph size to be tested.
            print("Select a graph size")
            print("1. 10 vertices and 15 edges")
            print("2. 20 vertices and 150 edges")
            print("3. 27 vertices and 750 edges")
            print("4. 37 vertices and 1500 edges")
            size_selection = int(input("Select 1 - 4: "))
            print()
            graph_size = [10, 20, 27, 37]
        graph_size = graph_size[size_selection - 1]

            
        # Determines if the user wants the graphs displayed.
        print("Would you like to display the graph?")
        print("1. Yes")
        print("2. No")
        print_graphs = int(input("Select 1 or 2: "))
        print()
                
        if print_graphs >= 1 and print_graphs <= 2:
            if print_graphs == 1:
                print_graphs = True
            else:
                print_graphs = False
            
            if graph_size == 10:
                small_graphs = True
            else:
                small_graphs = False
            
            # Calls the corresponding run_automated function based on the
            # menu number selected.
            if menu == 1:
                run_automated_randomization(graph_size, print_graphs, small_graphs)
            elif menu == 2:
                run_automated_backtracking(graph_size, print_graphs, small_graphs)
            elif menu == 3:
#                run_automated_diff_rep(graph_size, print_graphs)
                pass
            else:
                print("Invalid menu number. Program terminating")
        else:
            print("Invalid menu number. Program terminating.")
    else:
        print("Invalid menu number. Program terminating.")

# Function that allows users to insert their own edge.
# Input: The current customized graph.
# Output: None, other than the runtime for the insertion method.
def custom_insert(graph):
    
    # Retrieves the source and destination vertex from the user.
    print("Enter the following attributes")
    source = int(input("Source Vertex: "))
    dest = int(input("Destination Vertex: "))
    if graph.weighted:
        weight = int(input("Weight: "))
    else:
        weight = 1
    
    # Inserts the edge.
    start_time = time.perf_counter()
    graph.insert_edge(source, dest, weight)
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))
 
# Function that allows users to delete an edge from the graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the deletion method.
def custom_delete(graph):
    
    # Retrieves the source and destination vertex from the user.
    print("Enter the following attributes")
    source = int(input("Source Vertex: "))
    dest = int(input("Destination Vertex: "))
    
    # Deletes the edge.
    start_time = time.perf_counter()
    graph.delete_edge(source, dest)
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))
    
# Function that allows users to delete an edge from the graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the deletion method.
def custom_randomization(graph):
    
    # Retrieves the source and destination vertex from the user.
    print("Hamiltonian Path Using Randomization:") 
    
    # Deletes the edge.
    start_time = time.perf_counter()
    subset_graph, subset_of_edges = graph.randomized_hamiltonian()
    end_time = time.perf_counter()
    
    print("Path: ", subset_of_edges)
    if not subset_graph is None:
        print("The subset graph will stored in the current directory.")
        subset_graph.draw()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))
    
# Function that allows users to delete an edge from the graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the deletion method.
def custom_backtracking(graph):
    
    # Retrieves the source and destination vertex from the user.
    print("Hamiltonian Path Using Backtracking:") 
    
    # Deletes the edge.
    start_time = time.perf_counter()
    subset_of_edges, subset_graph = graph.backtracking_hamiltonian()
    end_time = time.perf_counter()
    
    print("Path: ", subset_of_edges)
    if not subset_graph is None:
        print("The subset graph will stored in the current directory.")
        subset_graph.draw()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))

# Function that displays the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the display function.       
def custom_display(graph):
    print(representation_to_text(graph.representation), ":")
    
    # Displays graph.
    start_time = time.perf_counter()
    graph.display()
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))
    
# Function that draws the current graph.
# Input: The current customized graph.
# Output: None, other than the runtime for the display function.       
def custom_draw(graph):
    print("The graph will be stored in the current directory.")
    
    # Draws graph.
    start_time = time.perf_counter()
    graph.draw()
    end_time = time.perf_counter()
    
    print("Runtime: % 0.6f seconds\n" % (end_time - start_time))

# Function that allows the user to select an operation to perform on the graph.
# Input: None
# Output: An integer 1 through 8 that represents the menu selection or negative
#         one if an incorrect menu number was selected.
def custom_graph_function_selection_menu():
    print("Select an operation")
    print("1. Insert an edge")
    print("2. Delete an edge")
    print("3. Hamiltonian Cycle Randomization")
    print("4. Hamiltonian Cycle Backtracking")
    print("5. Display Graph")
    print("6. Draw Graph")
    print("7. Exit")
    menu = int(input("Select 1 - 7: "))
    if menu < 1 or menu > 7:
        print("Invalid menu selection. Exiting program")
        menu = -1
    return menu

# Function that determines which custom function to call based on the user's
# menu selection.
# Input: The current graph created by the user.
# Output: None.
def custom_graph_interface(graph):
    menu = custom_graph_function_selection_menu()
    print()
    
    # Continues to allow the user to perform the operations on the custom graph
    # as long as a valid menu number is selected.
    while  menu >= 1 and menu <= 6:
        try:
            # Insert edge.
            if menu == 1:
                custom_insert(graph)
            
            # Delete edge.
            elif menu == 2:
                custom_delete(graph)
            
            # Convert to a different graph representation.
            elif menu == 3:
                custom_randomization(graph)
                
            # Perform breadth first search.
            elif menu == 4:
                custom_backtracking(graph)
                
            # Perform depth first search.
            elif menu == 5:
                custom_display(graph)
                
            # Draw the graph.
            else:
                custom_draw(graph)
        except ValueError:
            print("Invalid input. Please try again.\n")
        menu = custom_graph_function_selection_menu()
        print()

# Function that allows users to select the graph implementation.
# Input: None
# Output: The menu number based on the user's selection.  If the menu is one,
#          adjacency list is selected.  If two is selected, the matrix is selected.
#          If three is chosen,  the edge list is selected.
def select_graph_types():
    print("Choose your graph implementation")
    print("1. Adjacency List")
    print("2. Adjacency Matrix")
    print("3. Edge List")
    menu = int(input("Select 1, 2, or 3: "))
    print()
    return menu

# Allows the user to create a custom graph. Retrieves the number of vertices
# and whether the graph is directed or weighted from the user.
# Input: None
# Output: None
def create_graph_menu():
    graph_type = select_graph_types()
    
    # If a valid graph type is selected, then the user selects the number of 
    # vertices the graph will have.
    if graph_type >= 1 and graph_type <= 3:
        print("How many vertices do you want the graph to have?")
        size = int(input("Enter the number of vertices: "))
        print()
        
        # The user determines whether they want the graph to be weighted or
        # unweighted.
        if size > 0:
            print("Do you want the graph to be weighted or unweighted?")
            print("1. Weighted")
            print("2. Unweighted")
            try:
                weighted = int(input("Select 1 or 2: "))
            except ValueError:
                weighted = 3
            print()
            
            if weighted == 1:
                weighted = True
            elif weighted == 2:
                weighted = False
            else:
                print("Invalid selection. The graph will be unweighted.\n")
                weighted = False
            
            #Creates an adjacency list graph based on the user chosen attributes.
            if graph_type == 1:
                graph = al.Graph(size, weighted)
                
            #Creates an adjacency matrix graph based on the user chosen attributes.
            elif graph_type == 2:
                graph = am.Graph(size, weighted)
                
            #Creates an edge list graph based on the user chosen attributes.
            else:
                graph = el.Graph(size, weighted)
            
            # Allows users to perform operations on the created graph.
            custom_graph_interface(graph)
            
        else:
            print("A graph has to have at least one vertex. Program terminating")
    else:
        print("Invalid menu number. Program terminating.")

# Main method that allows the user to determine whether they want to create
# their own graph, solve the riddle, run the provided tests, or run automated
# tests.
# Input: None
# Output: None
sys.setrecursionlimit(7000)
print("Welcome")
print("1. Create your own graph")
print("2. Run automated tests")
#try:
menu = int(input("Select 1 or 2: "))
print()

# Calls the corresponding function based on the user's menu selection.
if menu == 1:
    create_graph_menu()
elif menu == 2:
    automated_test_setup()
else:
    print("Invalid menu number. Program terminating.")
#except ValueError:
#    print("Invalid input. Program terminating.")