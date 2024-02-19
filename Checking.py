def checkTuples(hand): #Checks for any triples (or higher). SHOULD BE WORKING.
    #Returns the sets, but also the number which is a triple
    sets = [[0]]
    hand1 = hand.copy()
    placeholder = [] #Placeholder list for the numbers in your hand
    numSets = 0


    #Discards info about the suits
    for i in range(0,len(hand1)):
        placeholder.append(hand1[i][1])
    #Jokers!
    j = placeholder.count("j")
    for i in range(0,j):
        placeholder.remove("j")

    #If there are all jokers and no other cards,
    if not placeholder:
        return [[0,3]]

    unique_numbers = list(set(placeholder))  # Get unique numbers from the input list
    sets = [[x, placeholder.count(x)] for x in unique_numbers]
    #print(sets)

    sets = [x for x in sets if not x[1]==1]
    #Counts how many wilds would be needed to complete the sets
    for k in sets:
        if k[1] < 3:
            j -= (3-k[1])


    #If there aren't any tuples BUT there are jokers, throw them with the highest card(s)
    placeholder.sort(reverse=True)
    while j>1 and placeholder:
        sets.append([placeholder[0],1])
        del placeholder[0]
        j -= 2

    return sets

def Zoom(hand,suit):
    hand1 = hand.copy()
    jUsage = 0
    p1 = [0] + [x[1] for x in hand1 if x[0]==suit]
    p1.sort()
    p1 = list(set(p1))
    p1.sort()
    p1 += [0]
    #print("suit:",suit,"and",p1)

    for i in range(1,len(p1)-1):
        if not ( (p1[i]==p1[i+1]-1) or (p1[i]==p1[i+1]-2) or (p1[i]==p1[i-1]+1) or (p1[i]==p1[i-1]+2) ):
            p1[i]=0
        if (p1[i]==p1[i+1]-2):
            jUsage += 1
    #print(p1)
    p1 = [x for x in p1 if x!=0]
    return [suit,p1,jUsage]

def checkRuns(hand): #Checks for any runs. Basically the same as the triples.
    # Returns the sets, but also the number which is a triple
    sets = []
    hand1 = hand.copy()
    numSets = 0

    #Checks for jokers
    j = 0
    #Checks which are jokers, and how many there are
    for i in range(0,len(hand1)):
        if hand1[i][1] == "j":
            j = j+1
    for i in range(0,j):
        hand1.remove([0,"j"])

    if not hand1:
        return [[0,0,[0,0],0]]

    #print("Wilds:",j)

    #Sorts copy of hand by the number
    hand1.sort(key=lambda x: x[1])
    #print(hand1)
    #print("wilds:",j)

    """The following are all the same.
    Idea is to separate by suit and then look with moving window.
    There's a problem with the first and last - hence the extra if not statements."""


    p1 = Zoom(hand1,1)
    p2 = Zoom(hand1,2)
    p3 = Zoom(hand1, 3)
    p4 = Zoom(hand1, 4)
    p5 = Zoom(hand1, 5)

    sets = [p1]+[p2]+[p3]+[p4]+[p5]
    #print(sets)
    sets = [x for x in sets if x[2]]

    return sets
