# Instructions

The main program is implemented in NicholeMaldonado_Lab5.py. The HashTableChainClass.py, HashTableLP.py, and WordEmbedding.py
are necessary for the HashTableChain, HashTableLP, and WordEmbedding objects used in the program.

For the program, the user must first enter the path of the file that contains the word embeddings. Please enusre that
you include the full directory with the txt file included. For example, valid input would be:
/Users/nichole_maldonado/Desktop/glove.6B.50d.txt

With the file path successfully obtained, the user can then determine if they want to find the similairities of pairs
from a file (enter 1) or enter a pair of words to compare (enter 2). If the user wants to find the similairies of pairs
from a file, then the user must enter the file path of the file.

The user can then select the hash function that will be used and the load factor.  If the user selects the hash table
with chaining and hash function 1 through 4, then they are given the option to use linear insertion or binary insertion which
inserts the WordEmbedding objects in order.

The user is also given the option to enter the number of valid words the file with the word embeddings contains or allow
the computer to calculate the number of valid words.  Valid words are words with only letters.  If the user enters fewer lines
then the file contains, then the number of WordEmbedding inserted will stop after the load factor is reached. If unsure,
please let the program count the number of valid words.

After the hash table is populated, searches for the pairs and their computations will occur. Note that after all 
searches have been made and the entire file with the word pairs has been read, the program will terminate.  
If the user entered pairs, the program will also terminate after finding the pairs and their similarity.

Additionally, the TestTrialFile contains all the files used during testing. The performance time based on each file is 
recorded in the report. Files that start with "C" are for the medium_glove.txt. Files that start with "LP" are for
the small_glove.txt. Regular files are for the glove.6B.50d.txt.

The lp_file_creation.py file found in SourceCode was the code used to generate the subfiles of the glove.6B.50d.txt file.
It is not integral to the functionality of the program but is still provided for reference.

Lastly, when using the program please use the following files with the table type and hash function to view 
best results. Failing to do so could result in long construction times due to the number of collisions:

glove_6B_50d.txt 
  Chaining with Ordered Chains (Binary Insertions and Finds) – length of string, ascii value of the first letter, 
                                                              ascii value of the first and last letter, and ascii sum
  Chaining Standard (Linear Insertions and Finds) – ascii sum, recursive, custom
  Linear Probing – recursive, custom
  
small_glove.txt – 35% of Original File
  Chaining Standard (Linear Insertions and Finds) – length of string, ascii value of the first letter, 
                                                  ascii value of the first and last letter, and ascii sum
  Linear Probing – length of string, ascii value of the first letter, ascii value of the first and last letter, 
                   and ascii sum
                   
medium_glove.txt – 45% of Original File
  Chaining Standard (Linear Insertions and Finds) – length of string, ascii value of the first letter, 
                                                  ascii value of the first and last letter, and ascii sum
                                                  
The small_glove.txt file and medium_glove.txt file can be also be found in the TestTrialFile.
