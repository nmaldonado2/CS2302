# Instructions

The main program is implemented in NicholeMaldonado_Lab4.py. The BSTClass.py, BTreeClass.py, and WordEmbedding.py
are necessary for the BST, BTree, and WordEmbedding objects used in the program.

For the program, the user must first enter the path of the file that contains the word embeddings. Please enusre that
you include the full directory with the txt file included. For example, valid input would be:
/Users/nichole_maldonado/Desktop/glove.6B.50d.txt

With the file path successfully obtained, the user can then determine if they want to find the similairities of pairs
from a file (enter 1) or enter a pair of words to compare (enter 2). If the user wants to find the similairies of pairs
from a file, then the user must enter the file path of the file.

Afterwards, the user can deterine whethr they want to use a BST or B-Tree to store the WordEmbeddings and perform the
searches and computations for the pairs. Note that after all searches have been made and the entire file with the
word pairs has been read, the program will terminate.  If the user entered pairs, the program will also terminate
after finding the pairs and their similarity.

Additionally, the TestTrialFile contains all the files used during testing. The performance time based on each file is 
recorded in the report.

The FileCreation.py file found in SourceCode was the code used to generate the test files.  It is not integral to the
functionality of the program but is still provided for reference.
