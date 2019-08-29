# CS2302 Data Structures
# Nichole Maldonado
# Lab 1 - Recursion, Part 1
# Dr. Fuentes
# Anindita Nath

import time
import requests
import os


# 
# Inputs:
# Outputs:
def ReadAndStoreTextFromFile(fileName):
#    try:
        # Opens file to be read and evaluated
    file = open(fileName, "r")
    
    englishWordSet = set()
    
    line = file.readline()
    while line:
        # Adds each word to englishWordSet without the appended endline
        englishWordSet.add(line.rstrip("\n"))
        line = file.readline()
#    except: 
#        return None
    
    file.close()
    return englishWordSet

def FindAnagrams(remaining_word, appending_word, englishWordSet, anagrams, original_word):
    if len(remaining_word) == 0:
        if appending_word in englishWordSet:
            anagrams.append(appending_word)
        return
    # FIXME: Should I prevent original word from being added initially or delete
    # it at the end
    if len(remaining_word) == 1 and (appending_word + remaining_word) == original_word:
        return
        
    charUsedSet = set()
    for i in range(len(remaining_word)):
        charUsedSet.add(remaining_word[i])
        newLetterToAppend = remaining_word[i]
        newRemainingWord = remaining_word[:i] + remaining_word[i + 1:]
        FindAnagrams(newRemainingWord, appending_word + newLetterToAppend, englishWordSet, anagrams, original_word)
    
    
response = requests.get("https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt")
if response:
    print("In here")
    fileName = os.path.join(getcwd(), "words_alpha.txt")
    print(fileName)
    englishWordSet = ReadAndStoreTextFromFile(fileName)
    wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
    
    while len(wordOrEmptyString) > 0:
        
        # Finds anagrams as long as wordOrEmpty string has letter characters only.
        if wordOrEmptyString.isalpha():
            anagrams = []
            startTime = time.perf_counter()
            FindAnagrams(wordOrEmptyString, "", englishWordSet, anagrams, wordOrEmptyString)
            elapsedTime = time.perf_counter() - startTime
            print("The word", wordOrEmptyString, "has the following", len(anagrams), " anagrams: ")
            anagrams = list(set(anagrams))
            for i in anagrams:
               print(i)
            print("It took %.6f seconds to find the anagrams\n" % elapsedTime)
        else:
            #is this statment ok if there are white spaces only?
            print("The word you entered is incorret. Please make sure that the word contains letters only and no spaces\n")
        wordOrEmptyString = input("Enter a word or empty string to finish: ").lower()
        
    print("Bye, thanks for using this program!")
else:
    print("An error occured while loading the file. Program terminating")
