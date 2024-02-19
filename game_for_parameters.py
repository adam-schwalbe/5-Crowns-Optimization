import random
from Modules import *
from csv import *
from statistics import median
from statistics import stdev


for sizeOfHand in range(3,11):
    #Setting up game and trials
    dataCollector = []
    temp_dataCollector = []
    for parameter_blah in range(0,13):
        for parameter_pointSave in range(0,13):
            #print(sizeOfHand)
            for blah in range(150):
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
                #print("Alice's hand:",alice.hand)
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
                        dChoice = alice.evalDiscardSmart(discard,parameter_blah,parameter_pointSave)
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
                        dChoice = charlie.evalDiscardSmart(discard,parameter_blah,parameter_pointSave)
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
                        dChoice = bob.evalDiscardSmart(discard,parameter_blah,parameter_pointSave)
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

                temp_dataCollector.append(bob.turnsToGoOut)
                temp_dataCollector.append(alice.turnsToGoOut)
                temp_dataCollector.append(charlie.turnsToGoOut)

                # print(blah,"percent done with trial",parameter_pointSave)

            print("Done with trial",parameter_blah,parameter_pointSave)
            dataCollector.append([parameter_pointSave,parameter_blah,median(temp_dataCollector),round(stdev(temp_dataCollector),4)])
            # print(dataCollector)
            temp_dataCollector = []

    print('data:',dataCollector)

    # Formatting data
    # Creating collectors
    dataCollector_formatted = []
    dataCollector_formatted2 = []
    for k in range(13):
        dataCollector_formatted.append([])
        dataCollector_formatted2.append([])


    for k in dataCollector:
        dataCollector_formatted[k[0]].append([k[2],k[3]])
    print(dataCollector_formatted[0])

    for foo in range(len(dataCollector_formatted)):
        for j in range(len(dataCollector_formatted[foo])):
            dataCollector_formatted2[foo].append(round(dataCollector_formatted[foo][j][0] * (dataCollector_formatted[foo][j][1]/2),4))
            # dataCollector_formatted2[foo].append(round(dataCollector_formatted[foo][j][0],4))

    print('First data collector:',dataCollector_formatted)
    print('Second data collector:',dataCollector_formatted2)

    filename = str('5cData_parameters'+str(sizeOfHand)+'.csv')
    write_1d_list_to_csv(dataCollector_formatted2, filename)