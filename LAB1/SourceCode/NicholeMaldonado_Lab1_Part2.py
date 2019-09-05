# Course: CS2302 Data Structures
# Date of Last Modification: September 2, 2019
# Assignment: Lab 1 Recursion, Part 2
# Author: Nichole Maldonado
# Professor: Olac Fuentes
# TA: Anindita Nath
# Purpose: The purpose of this lab is to use a recursive function to add all
#          anagrams of the user provided word to a set.  The set is then
#          displayed. The words_alpha.txt is read to populate the set of valid 
#          english words that the anagrams will be compared against.

import time

# Opens the file containing all english words and populates englishWordSet
# with these words.
# Input: The path of the file containing the english words and the sets for the
#        english words and prefixes that will be populated.
# Output: None
# Assume that englishWordSet and prefixWordSet are initially empty sets.
def ReadAndStoreTextFromFile(filePath, englishWordSet, prefixWordSet):
    # Opens file to be read and evaluated.
    file = open(filePath, "r")
    line = file.readline()
    
    # Iterates through each line of the file adding all non-white space words
    # to englishWordSet and prefixWordSet.
    while line:
        if not line.isspace():
            englishWordSet.add(line.rstrip("\n"))
            AddPrefixes(line.rstrip("\n"), prefixWordSet)
        line = file.readline()
    file.close()

# Function that adds all possible prefixes of word that do not already exist in
# prefixWordSet.
# Input: word whose prefixes will be extracted and the set, prefixWordSet.
# Output: None
def AddPrefixes(word, prefixWordSet):
    if not word in prefixWordSet:
        prefix = word[:len(word) - 1]
        
        # Adds prefixes by removing the last letter of the word until the 
        # prefix exists in the set or ultimately an empty string is reached.
        while not prefix in prefixWordSet:
            prefixWordSet.add(prefix)
            prefix = prefix[:len(prefix) - 1]
            
# Recursive function that finds all anagrams of originalWord
# Input: lettersToAppend which contains the letters of originalWord 
#        that will later be added to permutation, permutation which is 
#        the current combination, the set of EnglishWords, the set of prefixes
#        the set of anagrams that will be populated, and the original word.
# Output: None, however, anagrams may be populated if anagrams of originalWord
#         are found. 
# Assumptions: This method should initially be  called with permutation
#              as an empty string and lettersToAppend as the word whose
#              anagrams we are searching for.
def FindAnagrams(lettersToAppend, englishWordSet, prefixWordSet, anagrams, 
                 originalWord, permutation = ""):

    ## Base case that signifies that the current permutation includes all the
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
    
    # Base case that stops recursive calls if the current permutation is
    # not a valid prefix.
    if not permutation in prefixWordSet:
        return
    
    charUsedSet = set()
    
    # Makes recursive calls by appending every letter in lettersToAppend to the 
    # end of permutation and updates lettersToAppend by removing the
    # letter that was added for that instance.
    for i in range(len(lettersToAppend)):
        
        # If a recursive call appending the current letterToAppend has already 
        # been made, then another recursive call is not made.
        if not lettersToAppend[i] in charUsedSet:
            charUsedSet.add(lettersToAppend[i])
            remainingLetters = lettersToAppend[:i] + lettersToAppend[i + 1:]
            
            FindAnagrams(remainingLetters, englishWordSet, prefixWordSet, 
                         anagrams, originalWord, permutation + lettersToAppend[i])


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
                    
# Main program execution that prompts the user to enter the file with the
# English words and then prints all the anagrams of the user's words.
# Input: None
# Output: None
print("Enter the file path for the English word set below.")
print("Please remember to include the file's directory and name.")
filePath = input("File Path: ")

if CheckIfTxtFile(filePath):
    
    englishWordSet = set()
    prefixWordSet = set()
    try:
        # Calls ReadStoreTextFromFile to open the file and fill the 
        # set arguements accordingly.
        ReadAndStoreTextFromFile(filePath, englishWordSet, prefixWordSet)
        
        wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
    
        # Finds and prints the anagrams of the user's choice as long as 
        # wordOrEmptyString is not empty.
        while len(wordOrEmptyString) > 0:
            
            # Finds anagrams as long as wordOrEmpty string has letter 
            # characters only.
            if wordOrEmptyString.isalpha():
                anagrams = []
                
                # Calculates time for the FindAnagram's recursive method.
                startTime = time.perf_counter()
                FindAnagrams(wordOrEmptyString, englishWordSet, prefixWordSet, 
                             anagrams, wordOrEmptyString)
                elapsedTime = time.perf_counter() - startTime

                # Prints the anagrams in alphabetical order and reports the 
                # performance time.
                print("The word", wordOrEmptyString, end = " ") 
                print("has the following", len(anagrams), "anagrams: ")
                anagrams.sort()
                for i in anagrams:
                   print(i)
                print("It took %.6f seconds to find the anagrams\n" % elapsedTime)
            else:
                print("The word you entered is incorrect. ", end = "")
                print("Please make sure that the word contains letters only and no spaces\n")
            
            # Allows the user to enter new word or empty string to quit.
            wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
            
        print("Bye, thanks for using this program!")
        
    # Catches a FileNotFoundError or IOError, signifying the end of 
    # the program.
    except FileNotFoundError:
        print("\nThe file containing the list of English words could not be found.")
        print("Program terminating")
    except IOError:
        print("\nThe file containing the list of English words could not be accessed.")
        print("Program terminating")
else:
    print("Program terminating")
