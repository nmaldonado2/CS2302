# Course: CS2302 Data Structures
# Date of Last Modification: September 2, 2019
# Assignment: Lab 1 Recursion, Part 1
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab is to use a recursive function to add all
#          anagrams of the user provided word to a set.  The set is then
#          displayed. The words_alpha.txt is read to populate the set of valid 
#          English words that the anagrams will be compared against. The 
#          recursive function eliminates duplicate calls when the word has the 
#          same letters and stops recursive calls if the permutation is not
#          found in the prefix set.

import time

# Opens the file containing all English words and populates a set with these 
# words.
# Input: The path of the file containing the English words.
# Output: A set of English words or None if an error occurred or the file
#         path does not include the name of the .txt file to be read.
def ReadAndStoreTextFromFile(filePath):
    # Ensures that the filePath contains a .txt file at the end.
    if not CheckIfTxtFile(filePath):
        return None
    
    try:
        # Opens file to be read and evaluated.
        file = open(filePath, "r")
        englishWordSet = set()
        
        line = file.readline()
        
        # Iterates through each file line, adding every non-white space word to 
        # englishWordSet.
        while line:
            if not line.isspace():
                englishWordSet.add(line.rstrip("\n"))
            line = file.readline()
        file.close()
    
    # If a FileNotFoundError or IOError occurs, then None is returned.
    except FileNotFoundError: 
        print("The file containing the list of English words could not be found.")
        return None
    except IOError:
        print("The file containing the list of English words could not be accessed.")
        return None
    return englishWordSet

# Recursive function that finds all anagrams of originalWord
# Input: lettersToAppend which contains the letters from originalWord 
#        that will later be added to permutation, permutation which is 
#        the current letter combination, the set of EnglishWords,
#        the set of anagrams that will be populated, and the original word.
# Output: None, however anagrams may be populated if anagrams of originalWord
#         are found. 
# Assumptions: This method should initially be  called with permutation
#              as an empty string and lettersToAppend as the word whose
#              anagrams we are searching for.
def FindAnagrams(lettersToAppend, englishWordSet, anagrams, originalWord, permutation = ""):
    
    # Base case that signifies the that current permutation includes all the
    # letters from the originalWord since there are no more letters to append.
    if len(lettersToAppend) == 0:
        
        # permutation is only added if it is a valid English word.
        if permutation in englishWordSet:
            anagrams.append(permutation)
        return
    
    # Base case that does not allow the originalWord to be added to the set of
    # anagrams.
    if len(lettersToAppend) == 1 and permutation + lettersToAppend == originalWord:
        return

    # Makes recursive calls appending every letter in lettersToAppend to the 
    # end of permutation and updates lettersToAppend by removing the
    # letter that was added for that instance.
    for i in range(len(lettersToAppend)):
        remainingLetters = lettersToAppend[:i] + lettersToAppend[i + 1:]
        
        FindAnagrams(remainingLetters, englishWordSet, anagrams, originalWord, 
                     permutation + lettersToAppend[i])

# Ensures that filePath includes a .txt file at the end.
# Input: a string of the file path that will be evaluated.
# Output: Returns false if filePath does not end in .txt and returns
#         true otherwise.
def CheckIfTxtFile(filePath):
    
    # Returns false if the filePath does not have at least 5 letters since a
    # valid .txt file name can have a minimum of 5 letters.
    if len(filePath) < 5:
        print("Invalid file.")
        return False
    
    # If the length of filePath is greater than or equal to 5, then true is
    # returned only if filePath ends in ".txt".
    else:
        if filePath[-4:] == ".txt" and not "." in filePath[:-4]:
            return True
        else:
            print("Invalid file.")
            return False

# Main program execution that prompts the user to enter the file with English
# words and then prints all the anagrams of the user's words.
# Input: None
# Output: None
print("Enter the file path for the English word set below.")
print("Please remember to include the file's directory and name.")
filePath = input("File Path: ")
print()

englishWordSet = ReadAndStoreTextFromFile(filePath)

# If the englishWordSet was successfully populated, the program continues.
if not englishWordSet is None:
    wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
    
    # Finds and prints the anagrams of the user's choice as long as 
    # wordOrEmptyString is not empty.
    while len(wordOrEmptyString) > 0:
        
        # Finds anagrams as long as wordOrEmpty string has letter characters 
        # only.
        if wordOrEmptyString.isalpha():
            anagrams = []
            
            # Calculates time for the FindAnagrams recursive method.
            startTime = time.perf_counter()
            FindAnagrams(wordOrEmptyString, englishWordSet, anagrams, wordOrEmptyString)
            elapsedTime = time.perf_counter() - startTime
            
            # Removes duplicates and orders elements.
            anagrams = list(set(anagrams))
            
            # Prints the anagrams in alphabetical order and reports the 
            # performance time.
            print("The word", wordOrEmptyString, end = " ")
            print("has the following", len(anagrams), "anagrams: ")
            for i in anagrams:
               print(i)
            print("It took %.6f seconds to find the anagrams\n" % elapsedTime)
        else:
            print("The word you entered is incorrect. ", end = "")
            print("Please make sure that the word contains letters only and no spaces\n")
        
        # Allows the user to enter new word or empty string to quit.
        wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
    print("Bye, thanks for using this program!")
    
# If the englishWordSet was not successfully populated, the program terminates.
else:
    print("Program terminating.")
