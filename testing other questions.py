import random
import Modules
import Checking
from statistics import stdev
from statistics import mean
from statistics import median

"""
Tests the question: how many points can you reliably shed on the first hand?
"""

aggregateResults = []

def trial(bkptssets,bkpts,trials,sizeOfHand):

    #Setting up
    pointzzz = []
    delta = []

    for i in range(0,trials):
        #Sets up piles
        deck = Modules.createDeck()
        b = random.randrange(0,len(deck)-1)
        discard = deck[b]
        #print("Faceup:",discard)
        del deck[b]
        #Adds jokers. We treat kings as jokers (i.e. not adding kings separately) since functionally, it does not (really) matter which card is wild.
        for j in range(0,14):
            deck.append([0,"j"])
        alice = Modules.Player("Alice")
        alice.receive_hand(sizeOfHand,deck)
        #print("Starting hand:",alice.hand)
        hand = alice.hand
        t = Checking.checkTuples(hand)
        #print("tuples: ",t)
        r = Checking.checkRuns(hand)
        #print("runs: ",r)
        initialP = Modules.countPoints(hand,t,r)
        pointzzz.append(initialP)
        dChoice = alice.evalDiscardSmart(discard, bkptssets, bkpts)
        #print("Take the face-up card?", dChoice)
        if dChoice == True:
            hand.append(discard)
            # print("taken discard:",discard)
        else:
            b = random.randrange(0, len(deck) - 1)
            hand.append(deck[b])
            del deck[b]
        # Now run the discard script
        toDiscard = alice.discard_card()
        #print("To discard:", toDiscard)
        alice.hand.remove(toDiscard)
        #print("New hand:",alice.hand)
        newP = Modules.countPoints(alice.hand,Checking.checkTuples(alice.hand),Checking.checkRuns(alice.hand))
        delta.append(initialP-newP)
        #print("Point change:",initialP-newP)
        #print("Done percentage:",(i+1)*100/trials)
        #print("----------------------------")

    #print("Points:",pointzzz)
    #print("Median points:",median(pointzzz))
   # print("Changes:",delta)
    #print("Median change:",median(delta))
    #print("StDev:",stdev(delta))
    return [round(mean(delta),2),round(stdev(delta),2)]

print("RESULTS: (columns = point break points, rows = set break points)")
print("Format is [mean point changes, standard deviation]")
print("=============================================================================================")
print("__|       1      |       2      |     3      |       4      |      5      |     6     |     7     |")

for ij in range(5,10):
    for jk in range(1,8):
        aggregateResults.append(trial(ij,jk,300,5))
    print(ij,"|",aggregateResults)
    aggregateResults = []

print("=============================================================================================")