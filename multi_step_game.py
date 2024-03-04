import random
from Modules import *
from Checking import *
import csv
from statistics import median,stdev

#Setting up game and trials
dataCollector = [[]]

if __name__ == "__main__":
    #Setting up players
    alice = Player("Alice")
    bob = Player("Bob")
    charlotte = Player("Charlie")
    dave = Player("Dave")
    evelyn = Player("Evelyn")
    frank = Player("Frank")
    georgia = Player("Georgia")

    potential_players = [bob,charlotte,dave, evelyn, frank, georgia]
    # potential_players = [charlotte]
    players = [alice]

    dataCollector = []
    dataCollWithKey = []

    for handsize in range(3,11):
        dataCollector.append([])
        for player_add in potential_players:
            temp_data_collector = []
            players.append(player_add)

            #Then doing trials
            for blah in range(0,3000):
                #Sets up piles
                placeholder1 = initialize_deck()
                deck = placeholder1[0].copy()
                discard = placeholder1[1].copy()

                #Sets up players


                for person in players:
                    person.receive_hand(handsize,deck)
                    # print("Alice's hand:",alice.hand)
                    person.points = countPoints(person.hand)

                stop = False
                out = False
                rounds = 0

                while not stop:
                    rounds += 1

                    for player in players:
                        oneTurn(player, s_B(handsize), p_B(handsize),rounds,deck)
                        if player.out:
                            stop = True
                    if rounds > 14:
                        stop = True
                    # print()
                    # print('-------------------------------')
                    # print()

                temp_data_collector.append(rounds)

                for player in players:
                    player.hand = []
                    player.out = False

            dataCollector[handsize-3].append([median(temp_data_collector),round(stdev(temp_data_collector),4)])
            print('For handsize',handsize,'And number of players',len(players),'MEDIAN:',median(temp_data_collector),'STDEV:',stdev(temp_data_collector))
            # print(temp_data_collector)
            # print("done with players",len(players),"and handsize",handsize)

        players = [alice]

    print(dataCollector)


    dataCollectorFormatted = []
    ticker = 0
    for j in dataCollector:
        dataCollectorFormatted.append([])
        for i in j:
            dataCollectorFormatted[ticker].append((round(max(i[0]-(i[1]/2),0),3),round(i[0]+(i[1]/2),3)))
        ticker += 1
    dCF2 = transpose(dataCollectorFormatted)
    dDF3 = []
    ticker = 0
    for i in dCF2:
        dDF3.append([])
        for k in i:
            if isinstance(k,tuple):
                dDF3[ticker].append(k[0])
                dDF3[ticker].append((k[0]+k[1])/2)
                dDF3[ticker].append(k[1])
        ticker += 1

    headings = []
    for i in range(int(len(dDF3[0])/3)):
        headings.append(str(i + 3) + '-CARD-LOWER-BOUND')
        headings.append(str(i + 3) + '-CARD-MEDIAN')
        headings.append(str(i + 3) + '-CARD-UPPER-BOUND')
    print(dataCollectorFormatted)
    print(dCF2)
    print(dDF3)

    write_1d_list_to_csv(dDF3, headings,'5cData.csv')