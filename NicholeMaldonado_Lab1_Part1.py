# CS2302 Data Structures
# Nichole Maldonado
# Lab 1 - Recursion, Part 1
# Dr. Fuentes
# Anindita Nath
import time
import os

# Opens the file containing all english words and populates a set with these 
# words.
# Input: The path of the file containing the english words.
# Output: A set of english words or None if an error occurred.
def ReadAndStoreTextFromFile(fileName):
    try:
        # Opens file to be read and evaluated
        file = open(fileName, "r")
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
        print("\nThe file containing the list of English words could not be found.")
        print("Please edit the file path\n")
        return None
    except IOError:
        print("\nThe file containing the list of English words could not be accessed.")
        print("Please edit the file path\n")
        return None
    return englishWordSet

# Recursive function that finds all anagrams of originalWord
# Input: letterCombination which contains the originalWord that will later
#        represent all the possible letter combinations, the set
#        of EnglishWords, the set of anagrams that will be populated, the 
#        orginal word, and the prefix index which divides letterCombination
#        into the prefix [0, prefixIndex) and the words to be appended to the 
#        prefix [prefix, length of letterCombination).
# Output: None, however anagrams may be populated if anagrams of originalWord
#         are found. 
def FindAnagrams(letterCombination, englishWordSet, anagrams, 
                 originalWord, prefixIndex = 0):
    
    global recursiveCallCounter
    recursiveCallCounter += 1
    
    # Base case that adds letterCombination to anagrams if it is an anagram and
    # there are no more remaining letters.
    if prefixIndex == len(letterCombination):
        
        # If the letterCombination is the orginal word, then it is not added
        # to the anagram set.
        if letterCombination == originalWord:
            return
        
        if letterCombination in englishWordSet:
            anagrams.append(letterCombination)
        return
        
    remainingLetters = letterCombination[prefixIndex:]
    
    # Makes recursive calls for every letter in remainingLetter by 
    # appending the current remaining letter to the prefix and then
    # appending the rest of the remaining letters.
    for i in range(len(remainingLetters)):
        prefixLetters = letterCombination[:prefixIndex] + remainingLetters[i]
        newRemainingLetters = remainingLetters[:i] + remainingLetters[i + 1:]
        FindAnagrams(prefixLetters + newRemainingLetters, 
                     englishWordSet, anagrams, originalWord, prefixIndex + 1)

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
# all the english words.
# Input: A list, fileAttributes, which contains [directory, filename]
# Output: None, however fileAttributes will contain a new file name or 
#         directory based on the user's choice.
# Assume fileAttributes only has the directory and file name as elements.
def FilePathSetup(fileAttributes):
    # menuNum is initialized to 0 to initially enter the while loop.
    menuNum = 0
    
    print("Current file name:",fileAttributes[1])
    print("Current directory:", fileAttributes[0],"\n")
    
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
                    fileAttributes[1] = input("File Name (do not include directory):")
            
            # Notifies the user if they entered a value other than 1 or 2.
            else:
                print("\nInvalid menu number. Please try again.")
                
        # Notifies the user if they entered a menu value other than 1 or 2. 
        except ValueError:
            print("\nInvalid menu selection. Please try again.")     
            
recursiveCallCounter = 0  
directory = os.getcwd()
fileName = "words_alpha.txt"
englishWordSet = ReadAndStoreTextFromFile(os.path.join(directory, fileName))

# If englishWordSet is None, then the file path is continously edited by the
# user until ReadAndStoreText is able to successfully populate englishWordSet.
if englishWordSet is None:
    fileAttributes = [directory, fileName]
    while englishWordSet is None:
        FilePathSetup(fileAttributes)
        englishWordSet = ReadAndStoreTextFromFile(os.path.join(fileAttributes[0], fileAttributes[1]))
        
wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()

# Finds and prints the anagrams of the user's choice as long as 
# wordOrEmptyString is not empty.
while len(wordOrEmptyString) > 0:
    
    # Finds anagrams as long as wordOrEmpty string has letter characters only.
    if wordOrEmptyString.isalpha():
        anagrams = []
        
        # Calculates time for the FindAnagrams recursive method.
        startTime = time.perf_counter()
        FindAnagrams(wordOrEmptyString, englishWordSet, anagrams, wordOrEmptyString)
        elapsedTime = time.perf_counter() - startTime
        
        # print("Testing, words in anagrams set: ", anagrams)
        print("Testing, number of recursive calls:", recursiveCallCounter)
        recursiveCallCounter = 0
        
        # Removes duplicates and orders elements.
        anagrams = list(set(anagrams))
        
        # Prints the anagrams in alphabetical order and reports the 
        # performance time.
        print("The word", wordOrEmptyString, "has the following", len(anagrams), " anagrams: ")
        for i in anagrams:
           print(i)
        print("It took %.6f seconds to find the anagrams\n" % elapsedTime)
    else:
        # FIXME: is this statment ok if there are white spaces only?
        print("The word you entered is incorrect. Please make sure that the word contains letters only and no spaces\n")
    
    # Allows the user to enter new word or empty string to quit.
    wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
    
print("Bye, thanks for using this program!")