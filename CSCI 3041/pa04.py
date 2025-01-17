def scrabbleWordList():
    with open("scrabble.txt", 'r') as fp:
        return set(fp.read().split()) #Reads the .txt file line by line, splitting each line (word) to generate a set of the words

#filters valid words from a letter pool and scrambled letters
def validWords(letter_pool, scrambledLetters):
    validWordSet = set() # create an empty set to add onto later
    for word in scrambledLetters:
        if all(word.count(letter) <= letter_pool.count(letter) for letter in word): # check to see if each letter in the word appears fewer times in the word than in the letter pool
            validWordSet.add(word)
    return validWordSet


def get_anagrams(letter_pool):
    anagrams = set()
    testScrabbleWords = scrabbleWordList() #Get all of the scrabble words from the file
    testValidWords = validWords(letter_pool, testScrabbleWords) #get the valid words from the set of scrabble words and the word
    for word1 in testValidWords:
        for word2 in testValidWords: #loop through each word and determine if they are an anagram
            anagram = f'{word1} {word2}'
            if sorted(anagram.replace(" ", "")) == sorted(letter_pool): #check if it has the same letters as the pool of letters
                    anagrams.add(anagram)
    return anagrams
                


print(get_anagrams('MOHABICALAIC'))
