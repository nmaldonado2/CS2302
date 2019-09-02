# CS2302 Data Structures
# Nichole Maldonado
# Lab 1 - Recursion, Part 2
# Dr. Fuentes
# Anindita Nath

import time
import os

# Opens the file containing all english words and populates englishWordSet
# with these words.
# Input: The path of the file containing the english words and sets for the
#        english words and prefixes that will be populated.
# Output: None
# Assume that englishWordSet and prefixWordSet are initially empty sets.
def ReadAndStoreTextFromFile(filePath, englishWordSet, prefixWordSet):
    # Opens file to be read and evaluated
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
# Input: letterCombination which contains the originalWord that will later
#        represent all the possible letter combinations, the set of english
#        of EnglishWords, the set of prefixes, the set of anagrams that will be 
#        populated, the  orginal word, and the prefix index which divides 
#        letterCombination into the prefix [0, prefixIndex) and the words to be
#        appended to the prefix [prefix, length of letterCombination).
# Output: None, however anagrams may be populated if anagrams of originalWord
#         are found. 
def FindAnagrams(letterCombination, englishWordSet, prefixWordSet, anagrams, 
                 originalWord, prefixIndex = 0):
    global recursiveCallCounter
    recursiveCallCounter += 1
    
    # Base case that adds letterCombination to anagrams if it is an anagram and
    # there are no more remaining letters.
    if prefixIndex == len(letterCombination):
        # If the letterCombination is the orginal word, then it is not added
        # to the anagram set.
        
        
        if letterCombination in englishWordSet:
            anagrams.append(letterCombination)
        return
    

    # Base case that stops the recursive calls if the current prefix is not
    # in prefixWordSet
    if not letterCombination[:prefixIndex] in prefixWordSet:
        return
        
    remainingLetters = letterCombination[prefixIndex:]
    charUsedSet = set()
    
    # Makes recursive calls for every letter in remainingLetter by 
    # appending the current remaining letter to the prefix and then
    # appending the rest of the remaining letters.
    for i in range(len(remainingLetters)):
        if not remainingLetters[i] in charUsedSet:
            charUsedSet.add(remainingLetters[i])
            prefixLetters = letterCombination[:prefixIndex] + remainingLetters[i]
            newRemainingLetters = remainingLetters[:i] + remainingLetters[i + 1:]

            FindAnagrams(prefixLetters + newRemainingLetters, 
                         englishWordSet, prefixWordSet, anagrams, originalWord, prefixIndex + 1)


# Ensures that fileName is a .txt file.
# Input: a string of the file name that will be evaluated.
# Output: Returns false if the fileName does not end in .txt and returns
#         true otherwise.
def CheckIfTxtFile(fileName):
    
    # Returns false if the fileName does not have at least letters since a
    # valid .txt file name can have a minimum of 5 letters.
    if len(fileName) < 5:
        print("Invalid .txt file. Please try again.")
        return False
    
    # If the length of fileName is greater than or equal to 5, then true is
    # returned only if fileName ends in ".txt".
    else:
        if fileName[-4:] == ".txt" and not "." in fileName[:-4]:
            return True
        else:
            print("Invalid .txt file. Please try again.")
            return False
        
# Allows the user to modify the file directory and name for the file containing
# all the english words, in the event the file cannot be found.
# Input: A list, fileAttributes, which contains [directory, filename]
# Output: None, however fileAttributes will contain a new file name or 
#         directory based on the user's choice.
# Assume fileAttributes only has the directory and file name as elements.
def FilePathSetup(fileAttributes):
    # menuNum is initialized to 0 to initially enter the while loop.
    menuNum = 0

    print("Current file name:",fileAttributes[0])
    print("Current directory:", fileAttributes[1],"\n")
    
    # Allows the user to edit the directory or file name for the english word
    # file.
    while menuNum != 1 and menuNum != 2:
        print("1. Change directory")
        print("2. Change file name")
        try:
            menuNum = int(input("Select 1 or 2: "))
            
            # Changes the directory name.
            if menuNum == 1:
                fileAttributes[0] = input("File directory (Do not include file name): ")
            
            # Changes the file name.
            elif menuNum == 2:
                fileAttributes[1] = input("File Name (do not include directory): ")
                
                # Ensures that the new file name is a .txt file.
                while not CheckIfTxtFile(fileAttributes[1]):
                    fileAttributes[0] = input("File Name (do not include directory):")
            
            # Notifies the user if they entered a value other than 1 or 2.
            else:
                print("\nInvalid menu number. Please try again.")
        
        # Notifies the user if they entered a menu velue other than 1 or 2. 
        except ValueError:
            print("\nInvalid menu selection. Please try again.")
    
# FIXME: Would an empty file still have a prefixWordSet with just "" ?
# FIXME: Should the set be alphabatized. I looked and sets are usually "unsorted"
            
# recursiveCallCounter = 0  
englishWordSet = set()
prefixWordSet = set()
fileAttributes = [os.getcwd(), "words_alpha.txt"]
# fileRead assigned to false since the file has not been read yet.
fileRead = False

# Repeatedly attempts to open the file containing all the english words until
# the correct file is found.
while not fileRead:
    try:
        # Calls ReadStoreTextFromFile to open the file and fill the 
        # set arguements accordingly.
        ReadAndStoreTextFromFile(os.path.join(fileAttributes[0], 
                     fileAttributes[1]), englishWordSet, prefixWordSet)
        
        # fileRead assigned to true since the ReadAndStoreTextFromFile function
        # did not throw an error.
        fileRead = True
        
    # Catches a FileNotFoundError or IOError and calls FilePathSetup to ensure
    # that the file path is correct.
    except FileNotFoundError:
        print("\nFile not found. Please edit the file path.\n")
        FilePathSetup(fileAttributes)
    except IOError:
        print("\nFile could not be accessed. Please edit the file path.\n")
        fileAttributes = FilePathSetup(fileAttributes)

wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()

# Finds and prints the anagrams of the user's choice as long as 
# wordOrEmptyString is not empty.
while len(wordOrEmptyString) > 0:
    
    # Finds anagrams as long as wordOrEmpty string has letter characters only.
    if wordOrEmptyString.isalpha():
        anagrams = []
        
        # Calculates time for the FindAnagrams recursive method.
        startTime = time.perf_counter()
        FindAnagrams(wordOrEmptyString, englishWordSet, prefixWordSet, 
                     anagrams, wordOrEmptyString)
        elapsedTime = time.perf_counter() - startTime
        
        # print("Testing, words in anagrams set: ", anagrams)
        # print("Testing, number of recursive calls:", recursiveCallCounter)
        # recursiveCallCounter = 0
        
        # Prints the anagrams in alphabetical order and reports the 
        # performance time.
        print("The word", wordOrEmptyString, "has the following", len(anagrams), " anagrams: ")
        anagrams.sort()
        for i in anagrams:
           print(i)
        print("It took %.6f seconds to find the anagrams\n" % elapsedTime)
    else:
        print("The word you entered is incorret. Please make sure that the word contains letters only and no spaces\n")
    
    # Allows the user to enter new word or empty string to quit.
    wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
    
print("Bye, thanks for using this program!")