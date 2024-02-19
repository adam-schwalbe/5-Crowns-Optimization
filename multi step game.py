import random
from Modules import *
from Checking import *
import csv

#Setting up game and trials
dataCollector = [[]]

for handsize in range(0,8):
    sizeOfHand = handsize + 3
    #print(sizeOfHand)
    for blah in range(0,100):
        #Sets up piles
        deck = createDeck()
        b = random.randrange(0,len(deck)-1)
        discard = deck[b]
        #print("In the discard:",discard)
        del deck[b]
        #Adds jokers. We treat kings as jokers (i.e. not adding kings separately) since functionally, it does not (really) matter which card is wild.
        for i in range(0,14):
            deck.append([0,"j"])

        #Sets up players
        alice = Player("Alice")
        bob = Player("Bob")
        charlie = Player("Charlie")

        alice.receive_hand(sizeOfHand,deck)
        print("Alice's hand:",alice.hand)
        alice.points = countPoints(alice.hand)
        bob.receive_hand(sizeOfHand,deck)
        bob.points = countPoints(bob.hand)
        charlie.receive_hand(sizeOfHand,deck)
        charlie.points = countPoints(charlie.hand)

        stop = False
        out = False
        rounds = 0

        alice.turnsToGoOut = 16
        bob.turnsToGoOut = 16
        charlie.turnsToGoOut = 16
        while stop is False:
            rounds += 1
            #print("Round",rounds)
            playersLeft = 3

            if alice.out is False:
                #print("Alice's starting hand:",alice.hand,"with points",alice.points,"and sets",Checking.checkTuples(alice.hand)+Checking.checkRuns(alice.hand))
                dChoice = alice.evalDiscardSmart(discard,10,8)
                if dChoice == True:
                    alice.hand.append(discard)
                    #print("taken discard:",discard)
                else:
                    b = random.randrange(0,len(deck)-1)
                    alice.hand.append(deck[b])
                    del deck[b]
                #print("Hand with extra card:", alice.hand)
                #Now run the discard script
                discard = alice.discard_card()
                alice.hand.remove(discard)
                alice.points = countPoints(alice.hand)
                alice.pointHistory.append(alice.points)
                #print("A's new hand:",alice.hand,"with points",alice.points,"and sets",Checking.checkTuples(alice.hand)+Checking.checkRuns(alice.hand))
                #print("To discard:",discard)
                if alice.points == 0:
                    alice.out = True
                    alice.turnsToGoOut = rounds
                    playersLeft -= 1

                #print("")
                #print("")

            if charlie.out is False:
                #Charlie's turn!
                #print("charlie's starting hand:",charlie.hand,"with points",charlie.points,"and sets",Checking.checkTuples(charlie.hand)+Checking.checkRuns(charlie.hand))
                dChoice = charlie.evalDiscardSmart(discard,10,8)
                if dChoice == True:
                    charlie.hand.append(discard)
                    #print("taken discard:",discard)
                else:
                    b = random.randrange(0,len(deck)-1)
                    charlie.hand.append(deck[b])
                    del deck[b]
                #print("Hand with extra card:", charlie.hand)
                #Now run the discard script
                discard = charlie.discard_card()
                charlie.hand.remove(discard)
                charlie.points = countPoints(charlie.hand)
                charlie.pointHistory.append(charlie.points)
                #print("C's new hand:",charlie.hand,"with points",charlie.points,"and sets",Checking.checkTuples(charlie.hand)+Checking.checkRuns(charlie.hand))
                #print("To discard:",discard)
                if charlie.points == 0:
                    charlie.out = True
                    charlie.turnsToGoOut = rounds
                    playersLeft -= 1

                #print("")
                #print("")

            #Now, Bob's turn

            if bob.out is False:
                #print("Bob's starting hand:",bob.hand,"with points",bob.points)
                #print("Sets:",Checking.checkTuples(bob.hand)+Checking.checkRuns(bob.hand))
                dChoice = bob.evalDiscardSmart(discard,10,8)
                if dChoice == True:
                    bob.hand.append(discard)
                    #print("taken discard:",discard)
                else:
                    b = random.randrange(0,len(deck)-1)
                    bob.hand.append(deck[b])
                    del deck[b]
                #print("Hand with extra card:",bob.hand)
                #Now run the discard script
                discard = bob.discard_card()
                bob.hand.remove(discard)
                bob.points = countPoints(bob.hand)
                bob.pointHistory.append(bob.points)
                #print("B's new hand:",bob.hand,"with points",bob.points,"and sets:",Checking.checkTuples(bob.hand)+Checking.checkRuns(bob.hand))
                #print("To discard:",discard)
                if bob.points == 0:
                    bob.out = True
                    bob.turnsToGoOut = rounds
                    playersLeft -= 1

            #print("")
            #print("---------------------------------")
            #print("")

            if rounds > 14:
                stop = True

            #Resolves issue where players remaining do not get to have a good discard pile. Only really activates if one person is left.
            if playersLeft < 2:
                b = random.randrange(0, len(deck) - 1)
                discard = deck[b]
                del deck[b]



        #print("It took",rounds,"rounds to go out.")
        #print("Bob:",bob.pointHistory,bob.turnsToGoOut)
        #print("Alice:",alice.pointHistory,alice.turnsToGoOut)
        #print("Charlie:",charlie.pointHistory,charlie.turnsToGoOut)

        dataCollector[handsize].append(bob.turnsToGoOut)
        dataCollector[handsize].append(alice.turnsToGoOut)
        dataCollector[handsize].append(charlie.turnsToGoOut)

        print(blah*100/3333,"percent done with handsize",(handsize+3))

    dataCollector.append([])
    #print(dataCollector)


dataCollectorFormatted = [[]]
for i in range(0,len(dataCollector[0])):
    dataCollectorFormatted.append([dataCollector[0][i],dataCollector[1][i],dataCollector[2][i],dataCollector[3][i],dataCollector[4][i],dataCollector[5][i],dataCollector[6][i],dataCollector[7][i]])

print(dataCollectorFormatted)

def write_1d_list_to_csv(input_list, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['three','four','five','six','seven','eight','nine','ten'])
        for k in range(len(dataCollectorFormatted)):
            csv_writer.writerow(dataCollectorFormatted[k])

    print(f'CSV file "{csv_filename}" has been created in the Downloads folder.')

write_1d_list_to_csv(dataCollector, '5cData.csv')