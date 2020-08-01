# Instructions

The main program is implemented in NicholeMaldonado_Lab7.py. The HashTable.py, graph_AL, graph_AM.py, graph_EL.py,
and DisjointSetForest.py are necessary for the HashTableChain, adjacency list, adjcency matrix, edge list, and
DSF objects used in the program.

For the program, the user can choose one of three options:

1) Create your own tests for backtracking or randomization - This allows the user to select the number of vertices
  that they want their graph to contain along with the edge factor which will be used to compute the number of edges.
  Then users can determine if they want to use randomization or backtracking to find a Hamiltonian cycle. For the 
  randomization, the user can choose the generalized randomization, which follows the psuedocode provided, or the graph 
  implementation which allows users to test an adjacency list, edge list, or adjacency matrix.

2) Evaluate your own edit distance - This allows users to test the edit distance function. Users are given the option to
   either enter two of their own words or select two string lengths.  If the user selects two string lengths, then random
   words from a file will be used.  The user will be prompted to enter the directory of the file.  The WordSample.txt
   file was used for the tests and can be found in the Files folder.  Additionally, Distribution.txt denotes
   how many strings of a given length are included in WordSample.txt.  This is crucial since the program will not allow
   words with an absence length to be tested.
 
 3) Run automated tests - allows users to run tests on any of the methods for the lab. For all automated tests,
   if the user decides to print the graph, the graphs with 10 vertices will be drawn.  Only graphs with 10 vertices will
   be drawn.  All other graph sizes will have the graph representation displayed.  Additionally, for the automated tests, the 
   generalized randomization refers to the randomization algorithm that follows the provided pseudocode.
   
 Key points: Use the WordSample.txt file when deciding to run custom tests for the edit distance function. The 
            Distribution.txt contains all words in the file of a given length. The generalized randomization refers
            to the randomization funciton that follows the provided pseudocode and can be found in NicholeMaldonado7Lab7.py.
