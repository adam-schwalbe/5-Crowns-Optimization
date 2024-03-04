from Modules import *
from statistics import median
from random import randrange

def trials(n,trial_var,nRounds,handsize):
    alice = Player("Alice")
    bob = Player("Bob")
    charlotte = Player("Charlie")
    players = [alice, bob, charlotte]

    data = []

    for blah in range(0, n):
        '''setting up game'''
        placeholder1 = initialize_deck()
        deck = placeholder1[0].copy()
        deckOriginal = deck.copy()
        discard = placeholder1[1].copy()

        for person in players:
            person.receive_hand(handsize, deck)
            assert deck != deckOriginal #Checking the deck variable is actually messed with.
            person.points = countPoints(person.hand)
            person.pointHistory.append(person.points)

        stop = False
        out = False
        rounds = 0

        'Playing the game'
        while not stop:
            rounds += 1
            for player in players:
                oneTurn(player, trial_var[rounds-1], 3, rounds, deck)
            if rounds >= nRounds:
                stop = True

        for player in players:
            # print(player.pointHistory)
            for i in range(1,len(player.pointHistory)):
                if player.pointHistory[i-1] == 0:
                    data.append((i,player.pointHistory[i-1]-player.pointHistory[i],False))
                else:
                    data.append((i,player.pointHistory[i-1]-player.pointHistory[i],round((player.pointHistory[i-1]-player.pointHistory[i])/player.pointHistory[i-1],4)))

        'Setting up for next round'
        for player in players:
            player.hand = []
            player.pointHistory = []
            player.out = False

    return data

def adjacent_points(original_point, epsilon_vector):
    '''Adds original_point and epsilon_vector.
    THEY NEED TO BE THE SAME DIMENSION!!!'''
    new_point = list(original_point)
    for i in range(len(original_point)):
        new_point[i] += epsilon_vector[i]
        if new_point[i] < 0:
            new_point[i] = 0
    return tuple(new_point)

def data_crunching(d,nRounds):
    '''Takes in the set of data we have (represented below) and outputs the median number of points LEFT for that hand combination.'''
    placeholder = 1 #Total points removed
    placeholder1 = []
    for i in range(nRounds):
        placeholder1.append(median([y[2] for y in d if (not (y[2] == False)) and (y[0] == i+1)]))
    for i in placeholder1:
        placeholder *= (1-i)
    return round(placeholder,10)

def test_keyError(test,dict):
    try:
        placeholder = dict[test]
        return True
    except KeyError:
        return False

def optomize(t_v_start,n,n_trials=300):
    '''Optomizes for a certain variable (in this case point breakpoints) with n rounds.
    Can be generalized.
    Assumes function structure concave down.
    Format for d: (round number,amount of points the player could remove,PORPORTION of points they could remove)'''
    dTotalDiscarded = {}
    t_v = t_v_start
    stop = False
    dStorage = {}
    while not stop:
        #Establishing baseline
        d = trials(n_trials,trial_var=t_v,handsize=7,nRounds=n)
        dStorage[t_v] = data_crunching(d,n)
        #Testing adjacent points
        delta = [-999,(-1,-1,-1,-1)]
        print("Trial Variable:",t_v)
        for i in range(4):
            for j in range(2):
                epsilon = [0, 0, 0, 0]
                if j == 0:
                    epsilon[i] -= 1
                else:
                    epsilon[i] += 1
                t_v_testing = adjacent_points(t_v,tuple(epsilon))
                if not test_keyError(t_v_testing,dStorage):
                    dStorage[t_v_testing] = data_crunching(trials(n_trials,trial_var=t_v_testing,handsize=7,nRounds=n),n)
                if delta[0] < dStorage[t_v] - dStorage[t_v_testing]:
                    delta[0] = round(dStorage[t_v] - dStorage[t_v_testing],10)
                    delta[1] = t_v_testing

        if delta[0] <= 0:
            print('Minimum found at', t_v)
            stop = True
        if delta[0] > 0:
            t_v = delta[1]

        print('Direction of steepest descent:',delta)
        print('Storage var:',dStorage)
        print('-----------------------')

    return (t_v, dStorage[t_v])

if __name__ == "__main__":
    '''
    Improving optimization algorithm:
        Once a max is found, maybe sample around?
        
    Basic problem = that of local maxima and minima. What if the maximum you find is not the global max???
    One solution is more sampling, but that is super computationally expensive!
    
    
    Solution I have right now: 5 passes, started in random spots. Compare results and see which is a better min.
    '''
    # Setting up players
    t_v = 0
    collector = []
    for i in range(5):
        collector.append(optomize(t_v_start=(randrange(1,6),randrange(1,6),randrange(1,6),randrange(1,6)),n=4,n_trials=5000))

    print(collector)





