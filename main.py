'''
Further questions:
- How random is the game? Test by looking at median TTGO vs wilds.
- How many turns does the average game last with n players?
- Does applying optimal variable strategy actually DO anything?
- Neural network/machine learning approach?
'''

import random
import Modules
import Checking

#Setting up game
sizeOfHand = 10
#Sets up piles
deck = Modules.createDeck()
b = random.randrange(0,len(deck)-1)
discard = deck[b]
del deck[b]
#discard = [2, 3]
print("Discard:",discard)

#Adds jokers. We treat kings as jokers (i.e. not adding kings separately) since functionally, it does not (really) matter which card is wild.
for i in range(0,14):
    deck.append([0,"j"])

alice = Modules.Player("Alice")
alice.receive_hand(sizeOfHand,deck)
alice.points = Modules.countPoints(alice.hand)

print("Alice's starting hand:",alice.hand,"with points",alice.points,"\nand sets",Checking.checkTuples(alice.hand)+Checking.checkRuns(alice.hand))
dChoice = alice.evalDiscardSmart(discard,10,10)
if dChoice == True:
    alice.hand.append(discard)
    print("taken discard:",discard)
else:
    b = random.randrange(0,len(deck)-1)
    alice.hand.append(deck[b])
    del deck[b]
print("Hand with extra card:", alice.hand)
#Now run the discard script
discard = alice.discard_card()
alice.hand.remove(discard)
alice.points = Modules.countPoints(alice.hand)
alice.pointHistory.append(alice.points)
print("A's new hand:",alice.hand,"with points",alice.points,"and sets",Checking.checkTuples(alice.hand)+Checking.checkRuns(alice.hand))
print("To discard:",discard)
