from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{'roundtotal':0,'gametotal':0,'name':''},
         1:{'roundtotal':0,'gametotal':0,'name':''},
         2:{'roundtotal':0,'gametotal':0,'name':''},
        }

roundNum = 0
dictionary = []
turntext = ''
wheellist = []
roundWord = ''
blankWord = []
vowels = {'a', 'e', 'i', 'o', 'u'}
roundstatus = ''
finalroundtext = ''

def readDictionaryFile():
    global dictionary
    dictionaryfile = open(dictionaryloc,'r')
    dictionarystring = dictionaryfile.read()
    dictionaryfile.close()
    dictionary = dictionarystring.split('\n')

def readTurnTxtFile():
    global turntext   
    turntextfile = open(turntextloc,'r')
    turntext = turntextfile.read()
    turntextfile.close()

def readFinalRoundTxtFile():
    global finalroundtext   
    finalroundtextfile = open(finalRoundTextLoc)
    finalroundtext = finalroundtextfile.read()
    finalroundtextfile.close()

def readRoundStatusTxtFile():
    global roundstatus
    roundstatusfile = open(roundstatusloc)
    roundstatus = roundstatusfile.read()
    roundstatusfile.close()

def readWheelTxtFile():
    global wheellist
    wheellistfile = open(wheeltextloc)
    wheellist = wheellistfile.read()
    wheellistfile.close()

    wheellist = wheellist.split('\n')
    wheellist = list(wheellist)

def getPlayerInfo():
    global players
    player1 = players[0]
    player1['name'] = input('Enter your name Player 1: ')
    players[0] = player1

    player2 = players[1]
    player2['name'] = input('Enter your name Player 2: ')
    players[1] = player2

    player3 = players[2]
    player3['name'] = input('Enter your name Player 3: ')
    players[2] = player3


def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile() 
    
def getWord():
    global dictionary
    global roundWord
    global roundUnderscoreWord
    global blankWord
    roundWord = random.choice(dictionary)
    roundUnderscoreWord = []
    #choose random word from dictionary
   
    for a in roundWord:
        roundUnderscoreWord.append('_')
    
    blankWord = ''.join(roundUnderscoreWord)
    #make a list of the word with underscores instead of letters.
    return roundWord, roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    player1 = players[0]
    player1['roundtotal'] = 0
    players[0] = player1

    player2 = players[1]
    player2['roundtotal'] = 0
    players[1] = player2

    player3 = players[2]
    player3['roundtotal'] = 0
    players[2] = player3
    # Return the starting player number (random)
    playerrandom = [0,1,2]
    initPlayer = random.choice(playerrandom)
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    getWord()
    return initPlayer


def spinWheel(playerNum):
    global wheellist
    global players
    global vowels
    global playerstats
    global revealWord
    global stillinTurn

    # Get random value for wheellist
    spinValue = random.choice(wheellist)
    # Check for bankrupcy, and take action.
    if spinValue == 'BANKRUPT':
        print('Uh-oh! Your spin landed on bankrupt! You now have 0 in your bank.')
        stillinTurn = False
        playerstats['roundtotal'] = 0

    # Check for loose turn
    elif spinValue == 'LOSE A TURN':
        print('Uh-oh! Your spin landed on LOSE A TURN! Your turn is over.')
        stillinTurn = False
    # Get amount from wheel if not loose turn or bankruptcy
    else:
        print('\nWord: ' + blankWord)
        print(f'Your spin landed on {spinValue}')
# Ask user for letter guess
        #global letter
        letter = input('Please guess a consonant: ')
        
        while len(letter) != 1:
            print('Only guess 1 letter.')
            letter = str(input('Please guess a consonant: '))
        
        letter = letter.strip().lower()
        vowel_check = letter in vowels
        
        list_check = [a for a in range(len(blankWord)) if blankWord.startswith(letter, a)]


        while vowel_check == True or list_check != []:
            if vowel_check == True:
                print('Sorry, you have to pay for that one! Try again.')
                letter = str(input(' Please guess a consonant: '))
                letter = letter.strip().lower()
                vowel_check = letter in vowels
                list_check = [a for a in range(len(blankWord)) if blankWord.startswith(letter, a)]
            elif list_check != []:
                print('You already guessed that letter. Try again')
                letter = str(input(' Please guess a consonant: '))
                letter = letter.strip().lower()
                vowel_check = letter in vowels
                list_check = [a for a in range(len(blankWord)) if blankWord.startswith(letter, a)]
        
        else:
            guessletter(letter, playerNum)
            
# Use guessletter function to see if guess is in word, and return count
# Change player round total if they guess right.     
            if goodGuess == True:
                print('Correct!')
                print('The word now looks like this: ' + blankWord)
                playerstats['roundtotal'] += int(spinValue)
                stillinTurn = True
                print(f'{spinValue} has been added to your bank.')
                print('Total: $' + str(playerstats['roundtotal']))

                if roundWord == blankWord:
                    revealWord = True
                else:
                    print('\n(S)pin the wheel, (b)uy a vowel, or (g)uess the word')
            else:
                print ('Incorrect! Next Player')
                stillinTurn = False
   
    return stillinTurn


def guessletter(letter, playerNum): 
    global players
    global blankWord
    global roundUnderscoreWord
    global goodGuess
    global playerstats

    check = [a for a in range(len(roundWord)) if roundWord.startswith(letter, a)]

    for a in check:
        roundUnderscoreWord[a] = letter

    if check == []:
        goodGuess = False
    else:
        goodGuess = True
        blankWord = ''.join(roundUnderscoreWord)

    return goodGuess

def buyVowel(playerNum):
    global players
    global vowels
    global playerstats
    global stillinTurn
    global revealWord

    print('\nWord: ' + blankWord)
    print('\nBank amount: $' + str(playerstats['roundtotal']))
    letter = str(input('Select a vowel: '))
    letter = letter.strip().lower()
    vowel_check = letter in vowels

    while vowel_check == False:
        print('Not a vowel, try again')
        letter = str(input('Select a vowel: '))
        letter = letter.strip().lower()
        vowel_check = letter in vowels
    else:
        playerstats['roundtotal'] -= vowelcost
        guessletter(letter, playerNum)
        print('\nBank amount: $' + str(playerstats['roundtotal']))
        print('\nWord: ' + blankWord)
        print('\n(S)pin the wheel, (B)uy a vowel, or (G)uess the word')

    if blankWord == roundWord:
        revealWord = True

    return goodGuess
        
def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    global revealWord

    print('Word: ' + blankWord)
    
    # Ask for input of the word and check if it is the same as wordguess
    wordGuess = str(input('Guess a word: '))
    wordGuess = wordGuess.lower()

    if wordGuess == roundWord:
        blankWord = roundWord
        print('Congratulations! You guessed the word correctly!')
        revealWord = True
    else:
        print('Sorry. That guess is incorrect.')

    # Fill in blankList with all letters, instead of underscores if correct 
    
    # return False ( to indicate the turn will finish)  
    
    return False
    
    
def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players
    global revealWord
    global playerstats
    global stillinTurn

    # take in a player number. 
    # use the string.format method to output your status for the round
    # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    playerstats = players[playerNum]
    
    print(turntext.format(name = players[playerNum]['name']))
    print('Would you like to (S)pin the wheel, (B)uy a vowel, or (G)uess the word? ')
    stillinTurn = True
    
    while stillinTurn:
        if revealWord == True:
            break
        else: 
            choice = input('Select: ')
        # use the string.format method to output your status for the round
        # Get user input S for spin, B for buy a vowel, G for guess the word
            if(choice.strip().upper() == "S"):
                stillinTurn = spinWheel(playerNum)
            elif(choice.strip().upper() == "B"):
                if playerstats['roundtotal'] >= vowelcost:
                    stillinTurn = buyVowel(playerNum)
                else:
                    print('You do not have enough money to buy a vowel.')
                stillinTurn = buyVowel(playerNum)
            elif(choice.upper() == "G"):
                stillinTurn = guessWord(playerNum)
            else:
                print("Not a correct option")        
    
    # Check to see if the word is solved, and return false if it is,
    # Or otherwise break the while loop of the turn.     


def wofRound():
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundcounter
    global revealWord

    print('Round ' + str(roundcounter))
    
    initPlayer = wofRoundSetup()

    print('Word: ' + str(blankWord))

    turns = 3
    revealWord = False

    while revealWord == False:
        wofTurn((turns + initPlayer) % 3)
        turns += 1
    else:
        print('\n' + str(playerstats['name']) + ' wins!')
        playerstats['gametotal'] += playerstats['roundtotal']
        print('\nRound total: $' + str(playerstats['roundtotal']))
        print('Game total: $' + str(playerstats['gametotal']) + '\n')

    # Keep doing things in a round until the round is done ( word is solved)
        # While still in the round keep rotating through players
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext

    freebies = {'r','s','t','l','n','e'}
    
    player1 = players[0]
    player2 = players[1]
    player3 = players[2]
    # Find highest gametotal player.  They are playing.
    if player1['gametotal'] > player2['gametotal'] and player1['gametotal'] > player3['gametotal']:
        finalplayernum = 0
    elif player2['gametotal'] > player1['gametotal'] and player2['gametotal'] > player3['gametotal']:
        finalplayernum = 1
    elif player3['gametotal'] > player1['gametotal'] and player3['gametotal'] > player2['gametotal']:
        finalplayernum = 2
    
    finalplayer = players[finalplayernum]
    # Print out instructions for that player and who the player is.
    print(finalroundtext)
    print('''Here is what you need to know:
    Because we are kind we are going to give you the letters R, S, T, L, N and E for free.
    You will also be able to guess 3 consonants and 1 vowel free of charge.
    You only have one opportunity to guess the final word. If you guess the word
    correctly, you will receive an extra $5000!! If you guess wrong, you will not receive the extra cash.''')

    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    print('Word: ' + str(blankWord))
    print('First, we will give you all the freebies within the word.')
    for a in freebies:
        guessletter(a, finalplayer)

    print('\nWord: ' + str(blankWord))
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    
    # Gather 3 consonats and 1 vowel and use the guessletter function to see if they are in the word
    for i in range(3):
        guessedConsonants = []
        while True:
            consonant = input(f'Enter number {i+1} consonant you would like to guess: ')
            if consonant.isalpha == False or len(consonant) != 1:
                print('That is not a letter, try again')
            elif consonant in vowels:
                print('You can only guess a consonant for now, try again.')
            elif consonant in roundUnderscoreWord:
                print('That letter is already a freebie, try again')
            elif consonant in guessedConsonants:
                print('You already guessed that letter, try again')
            else:
                guessletter(consonant, finalplayer)
                guessedConsonants.append(consonant)
                break

    while True:
        vowel = input('Enter your guess for a vowel: ')
        if vowel.isalpha == False or len(vowel) != 1:
            print('That is not a letter, try again')
        elif vowel not in vowels:
            print('That is not a vowel, try again')
        elif vowel in roundUnderscoreWord:
            print('That vowel is already being displayed. Try again')
        else:
            guessletter(vowel, finalplayer)
            break
    
    print(f'After considering your guesses, the word now looks like this: {roundUnderscoreWord}')
    # Print out the current blankWord again
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    finalWordGuess = input('It is time to make your final guess for the word. Enter your guess: ')
    if finalWordGuess == roundWord:
        finalplayer['gametotal'] += finalprize
        print(f'Congratulations! You guessed the word correctly! Your total winnings are $ !' + str(finalplayer['gametotal']))
    else:
        print(f'Oof! Sorry that guess was incorrect. The word was {roundWord}. Better luck next time!')
    # If they do, add finalprize and gametotal and print out that the player won 


def main():
    global roundcounter
    global players
    roundcounter = 1

    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound()
            roundcounter += 1

            player1 = players[0]
            player2 = players[1]
            player3 = players[2]

            print('Round totals:')
            print(str(player1['name']) + ': $' + str(player1['gametotal']))
            print(str(player2['name']) + ': $' + str(player2['gametotal']))
            print(str(player3['name']) + ': $' + str(player3['gametotal']))
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()
    
    
