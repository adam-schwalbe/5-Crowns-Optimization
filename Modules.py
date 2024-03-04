import random
from csv import *
import Checking
from Checking import *


def s_B(n):
    a = [11, 11, 10, 10, 11, 11, 12, 11]
    return a[n - 3]
def p_B(n):
    a = [3, 2, 1, 3, 3, 4, 3, 3]
    return a[n - 3]

def write_1d_list_to_csv(input_list,firstRow, csv_filename):
    import csv
    with open(csv_filename, 'w',newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(firstRow)
        for k in range(len(input_list)):
            csv_writer.writerow(input_list[k])

    print(f'CSV file "{csv_filename}" has been created in the Downloads folder.')
def transpose(list):
    'Takes 2-D list and returns the list transposed'
    list1 = list.copy()
    formatted = []
    for k in range(len(list1[0])):
        formatted.append([])
        for i in list1:
            formatted[k].append(i[k])
    return formatted

def createDeck(): #Creates the deck.
    deck = []
    for j in range(1,3):
        for n in range(1,6):
            for i in range(3,13):
                deck.append([n,i])
        #print(deck)
    return deck

def countPoints(hand):
    '''Counts the number of points in a given hand.'''
    hand1 = hand.copy()
    hand1_original = hand.copy()
    triples = checkTuples(hand1)
    runs = checkRuns(hand1)
    points = 0

    # print("original hand:",hand1)
    # Firstly, we remove the triples which don't need wilds.
    for i in triples:
        if i[1] > 2:
            hand1 = [x for x in hand1 if x[1] != i[0]]
    #Then, we remove the sets w/o wilds
    for i in runs:
        if i[2] == 0:
            hand1 = [x for x in hand1 if not ((x[1] >= runs[i][0] and x[1] <= runs[i][1]) and (x[0]==runs[i][3]))]
    # print("hand with (supposedly removed) tuples:",hand1)

    #print("new hand:",hand1)
    if not (hand1 == hand1_original):
        triples = checkTuples(hand1)
        runs = checkRuns(hand1)

    #Joker script
    j = 0
    for i in range(0,len(hand1)):
        if hand1[i][1] == "j":
            j = j+1
            #print("joker added at",i)
    for i in range(0,j):
        hand1.remove([0,'j'])

    if not hand1:
        return 0

    """Next, we need to allocate jokers.
    We want to take the combinations with the highest potential number of points, and use the jokers there.
    Idea will be to look at the number of points in a hand when a possible combination of sets is eliminated"""
    possibleMoves = triples + runs

    #Calculates how many points you can save through each possible allocation of wilds.
    for i in range(0,len(possibleMoves)):
        if isinstance(possibleMoves[i][1],int):   #If it's a tuple
            x = 0
            x = possibleMoves[i][0] * possibleMoves[i][1]   #You can save this many points
            possibleMoves[i].append(x/(3-possibleMoves[i][1]))
        else:
            x = sum(possibleMoves[i][1])
            a = possibleMoves[i][2]
            possibleMoves[i][2] = (x/possibleMoves[i][2])
            possibleMoves[i].append(a)
    #print(possibleMoves)

    #Orders possibleMoves so that better moves are ahead.
    possibleMoves.sort(key=lambda x: x[2],reverse=True)
    # print("Possible moves (before any processing):",possibleMoves)

    toDelete = []
    repeats = False
    #print("Wilds:",j)
    #Allocates jokers, while there are them.
    for move in possibleMoves:
        if isinstance(move[1],int) and (j >= (3-move[1])):
            # print("registered triple")
            j -= (3-move[1])

            #Removes cards from the hand
            hand1 = [card for card in hand1 if card[1] != move[0]]
            #print("Hand after removal:",hand1)

        elif isinstance(move[1],list) and (j>=move[3]):
            toDelete = []
            j -= move[3]
            # print("Used joker on ",move,"with remaining jokers ",j)
            hand1 = [card for card in hand1 if not ((card[1] in move[1]) and (card[0] == move[0]))]
    #
    # print('Hand with cards removed:',hand1)
    # print("points before adding:",points)
    #Add up remaining number of points
    for i in range(0, len(hand1)):
        points += hand1[i][1]
        #print("added",hand1[i][1],"to point total")
    # print("points: ",points)
    return points

def oneTurn(player, breakpointSets, breakpointPoints,rounds,deck):
    global discard
    # print(player,"'s turn. Starting hand:",player.hand,"with points",player.points,"and sets",Checking.checkTuples(player.hand)+Checking.checkRuns(player.hand))
    # print("In the discard:",discard)
    dChoice = player.evalDiscardSmart(discard, breakpointSets, breakpointPoints)
    # print("Taking discard?",dChoice)
    if dChoice == True:
        player.hand.append(discard)
    else:
        b = random.randrange(0, len(deck) - 1)
        player.hand.append(deck[b])
        del deck[b]
    discard = player.discard_card()
    player.hand.remove(discard)
    player.points = countPoints(player.hand)
    player.pointHistory.append(player.points)
    if player.points == 0:
        player.out = True
        player.turnsToGoOut = rounds
    # print(player, "'s end of turn. Hand:", player.hand, "with points", player.points, "and sets", Checking.checkTuples(player.hand) + Checking.checkRuns(player.hand))

def initialize_deck():
    deck = createDeck()
    b = random.randrange(0, len(deck) - 1)
    global discard
    discard = deck[b]
    # print("In the discard:",discard)
    del deck[b]
    # Adds jokers. We treat kings as jokers (i.e. not adding kings separately) since functionally, it does not (really) matter which card is wild.
    for i in range(0, 14):
        deck.append([0, "j"])

    return (deck,discard)

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []  # Player's hand will be a list of card objects
        self.takenDiscard = False
        self.createSets = False
        self.points = 1000
        self.pointHistory = []
        self.out = False

    def receive_hand(self, size, deck): #For recieving a hand. Selects random element from the deck, adds it to the hand, and removes it from the deck
        for i in range(0,size):
            a = random.randrange(0,len(deck))
            self.hand.append(deck[a])
            del deck[a]

    def takeDiscard(self,faceUpCard):
        self.hand.append(faceUpCard)
        self.discard = faceUpCard

    def evalDiscardSmart(self,faceUpCard,breakpointRuns,breakpointPoints):    #Smart evaluating i.e. not just looking at the total number of points.
        '''Determines if the card should be taken from the discard pile'''
        self.createSets = False
        handWithDiscard = self.hand.copy()
        handWithDiscard.append(faceUpCard)
        #print(handWithDiscard)
        tuplesA = Checking.checkTuples(self.hand)
        tuplesB = Checking.checkTuples(handWithDiscard)
        runsA = Checking.checkRuns(self.hand)
        runsB = Checking.checkRuns(handWithDiscard)
        #If the discarded card means fewer points, period (i.e. fits into or creates set). Includes wilds (so we don't need to worry about those)
        if countPoints(self.hand) >= countPoints(handWithDiscard):
            # print("Can add to sets")
            return True
        #Or if it creates runs/tuples, and doesn't pose too big a risk to take
        elif (len(tuplesA) < len(tuplesB)) or (len(runsA) < len(runsB)):
            if faceUpCard[1] >= breakpointRuns:
                # print("Can create set potential, but too expensive")
                return False
            elif faceUpCard[1] < breakpointRuns:
                # print("Can create set potential")
                self.createSets = True
                return True
        else:
        #If there's a good discard card (to save points)
            for i in range(0,len(self.hand)-1):
                if self.hand[i][1] == "j":
                    pass
                elif self.hand[i][1] >= breakpointPoints + faceUpCard[1]:
                    # print("Can lead to lower points")
                    return True
        return False

    def discard_card_losepts(self):
        """Method to discard a card from the player's hand.
        ONLY considers how many points you can shed per turn.
        #Compares the points you can get by discarding non-set cards"""
        possiblePts = []
        placeholderHand = self.hand.copy()
        for i in range(0,len(placeholderHand)): #Cycles through cards, looks at how many points can be gotten rid of.

            deleted = placeholderHand[0]
            placeholderHand.remove(deleted)
            #print("Placeholder:",placeholderHand)

            triples = Checking.checkTuples(placeholderHand)
            runs = Checking.checkRuns(placeholderHand)
            possiblePts.append(countPoints(placeholderHand))
            #print("Points for this iteration:",possiblePts[i])

            #print("points if",deleted,"is removed:",countPoints(placeholderHand, triples, runs))
            placeholderHand.append(deleted)

        #print(possiblePts)
        t = Checking.checkTuples(placeholderHand)
        r = Checking.checkRuns(placeholderHand)
        partOfSet = []

        #Iterates through hands, and marks which cards are part of sets
        for card in placeholderHand:
            partOfSetPlaceholder = False
            #We treat tuples and runs differently.
            for set in t+r:
                if isinstance(set[1],int):
                    if card[1] == set[0]:
                        partOfSetPlaceholder = True
                if isinstance(set[1], list):
                    for i in range(0,len(set[1])):
                        if card[1] == set[1][i]:
                            partOfSetPlaceholder = True
            partOfSet.append(partOfSetPlaceholder)

        #If no cards are set-less, it will mark for ejection those part of weaker sets (i.e. those which require more wilds)
        noSets = 0
        for i in partOfSet:
            if i == False:
                noSets += 1
        if noSets == 0:
            for k in t+r: #Iterating through all sets
                if isinstance(k[1],int):  #For tuples,
                    if k[1] <= 2: #If it requires a wild,
                        for i in range(0,len(placeholderHand)): #Iterates through hand and marks cards
                            if placeholderHand[i][1] == k[0]:
                                partOfSet[i] = False
                if isinstance(k[1],list): #For runs,
                    if k[2] >= 1: #If it requires a wild,
                        for i in range(0,len(placeholderHand)): #Iterates through hand and marks cards
                            if placeholderHand[i][1] == k[1][len(k[1])-1]: #If it is equivalent to the largest number in the run
                                partOfSet[i] = False

        toEject = [0, 999]
        # Figuring out which cards specifically to eject. Iterates, only remembers those cards which are better than the previous best choice.
        for i in range(0, len(possiblePts)):
            if (possiblePts[i] < toEject[1]):  # If its lower than the previous lowest and not part of a set
                toEject[1] = possiblePts[i]
                toEject[0] = i
                # print("lowered for",i,"with points",possiblePts[i])
        # If there are no cards which are not part of sets, it will choose a card which belongs to a weaker set.
        if toEject[1] == 999:
            for i in range(0, len(possiblePts)):
                if (possiblePts[i] < toEject[1]):
                    toEject[1] = possiblePts[i]
                    toEject[0] = i
                    # print("lowered for",i,"with points",possiblePts[i])

        # print(toEject)
        return self.hand[toEject[0]]

        #print(placeholderHand)
        #print(partOfSet)
    def discard_card(self):
        """Method to discard a card from the player's hand. Works to preserve potential sets."""
        possiblePts = []
        placeholderHand = self.hand.copy()

        # Iterates through hands, and marks which cards are part of sets
        t = Checking.checkTuples(placeholderHand)
        r = Checking.checkRuns(placeholderHand)
        partOfSet = []
        for card in placeholderHand:
            partOfSetPlaceholder = False
            # We treat tuples and runs differently.
            if card[1] == "j":
                partOfSetPlaceholder = True
            else:
                for set in t + r:
                    if isinstance(set[1], int):
                        if (card[1] == set[0]) and not (set[1] == 1):
                            partOfSetPlaceholder = True
                    if isinstance(set[1], list):
                        for i in range(0, len(set[1])):
                            if card[1] == set[1][i]:
                                partOfSetPlaceholder = True
            partOfSet.append(partOfSetPlaceholder)

        # If no cards are set-less, it will mark for ejection those part of weaker sets (i.e. those which require more wilds)
        noSets = 0
        for i in partOfSet:
            if i == False:
                noSets += 1
        if noSets == 0:
            for k in t + r:  # Iterating through all sets
                if isinstance(k[1], int):  # For tuples,
                    if k[1] <= 2:  # If it requires a wild,
                        for i in range(0, len(placeholderHand)):  # Iterates through hand and marks cards
                            if placeholderHand[i][1] == k[0]:
                                partOfSet[i] = False
                if isinstance(k[1], list):  # For runs,
                    if k[2] >= 1:  # If it requires a wild,
                        for i in range(0, len(placeholderHand)):  # Iterates through hand and marks cards
                            if placeholderHand[i][1] == k[1][
                                len(k[1]) - 1]:  # If it is equivalent to the largest number in the run
                                partOfSet[i] = False

        for i in range(0, len(placeholderHand)):  # Cycles through cards, looks at how many points can be gotten rid of.
            if partOfSet[i] == False:
                deleted = placeholderHand[0]
                placeholderHand.remove(deleted)
                # print("Placeholder:",placeholderHand)

                possiblePts.append(countPoints(placeholderHand))
                # print("Points for this iteration:",possiblePts[i])

                # print("points if",deleted,"is removed:",countPoints(placeholderHand, triples, runs))
                placeholderHand.append(deleted)

            else:
                deleted = placeholderHand[0]
                placeholderHand.remove(deleted)
                placeholderHand.append(deleted)
                possiblePts.append(999)

        # print(placeholderHand)
        # print(partOfSet)

        toEject = [0, 999]
        # Figuring out which cards specifically to eject. Iterates, only remembers those cards which are better than the previous best choice.
        for i in range(0, len(possiblePts)):
            if (possiblePts[i] < toEject[1]) and (partOfSet[i] == False):  # If its lower than the previous lowest and not part of a set
                toEject[1] = possiblePts[i]
                toEject[0] = i
                # print("lowered for",i,"with points",possiblePts[i])
        # If there are no cards which are not part of sets, it will choose a card which belongs to a weaker set.
        if toEject[1] == 999:
            for i in range(0, len(possiblePts)):
                if (possiblePts[i] < toEject[1]):
                    toEject[1] = possiblePts[i]
                    toEject[0] = i
                    # print("lowered for",i,"with points",possiblePts[i])

        # print(toEject)
        return self.hand[toEject[0]]