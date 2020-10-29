import random
import os

wordFile = 'X:\Coding\Python\Practice\words.txt'

def home():
    getName()

def getMinMax():
    try:
        min = int(input('Enter a minimum length word: '))
    except ValueError:
        print('Not an integer')
    try:
        max = int(input('Enter a maximum length word: '))
    except ValueError:
        print('Not an integer')
    
    return min, max

def getName():
    name = input('Welcome What is Your Name? ')
    print('Thanks for joining us', name.capitalize() +'!')

    return name

def getWord(min=1, max=5):
    if min < 1 or min > max or max < min or max > 29:
        return 'fuckoff'
    
    words = open(wordFile).read().splitlines()
    
    randInt = random.randrange(1, 25000)
    returnWord = words[randInt]

    # makes sure the word stays within min and max boundaries
    while len(returnWord) > max or len(returnWord) < min:        
        randInt = random.randrange(1, 25000)
        returnWord = words[randInt]
    
    return returnWord.lower()

def startGame(word, underscores=None):
    if underscores == None:
        underscores = ['_' for underscores in range(len(word))]    
        correct = []
        word = list(word)
        wordCopy = word
    
    tries = 0
    guesses = []

    while True:
        os.system('cls')        
        if tries > 0:
            print(' '.join(underscores), '\t\t\t\t\t\t\nTries: {}\nGuessed Correctly: [{}]\nGuessed[{}]'.format(tries, ''.join(underscores), ', '.join(guesses)))
            guess = input('Enter a letter: ')
            if guess in guesses:
                print('You\'ve already Guessed that!')
                continue
            guesses.append(guess)
        else:
            print(' '.join(underscores), '\n')
            guess = input('Enter a letter: ')
            if guess in guesses:
                print('You\'ve already Guessed that!')
                continue
            guesses.append(guess)
            
        if not isinstance(guess, str) and len(guess) != 1:
            print(' '.join(underscores), '\n')
            guess = input('Enter a letter: here ')
            if guess in guesses:
                print('You\'ve already Guessed that!')
                continue
            guesses.append(guess)
        else:
            guessIndex = 0
            tries += 1
            while guess in word:
                for i, x in enumerate(word):
                    if x == guess:
                        guessIndex = i
            
                word[guessIndex] = 'correct'
                correct.append(guess)
                underscores[guessIndex] = guess

                if checkList(word):
                    print('\nThe Word is',''.join(underscores))
                    return 'You\'ve Wone!'
    
def checkList(lst):
    ele = lst[0]
    chk = True
    for item in lst:
        if ele != item:
            chk = False
            break
    
    return chk

home()
min, max = getMinMax()
word = getWord(min, max)
print(word)
print(startGame(word))