import copy
import ttt

root=[0]*9 # Root represents the initial state of the game


global results # results will hold all possible the states of a tic-tac-toe game
results=[root]

def change(whichPlayer):
    ''' Swithces from player 1 to player 2 and vice versa '''
    return 2 if whichPlayer==1 else 1

def states(state,whichPlayer,memo=[]):
    '''
        The objective of the function is to append into results all possible game states
        where player 1 starts the game. Situations where player 2 moves first are covered in states2()
        state - a list representing a game state
        whichPlayer  - 1 or 2, this function should be initially called with whichPlayer=1, 
        memo - a list of visited states. if we run into a state, that we have been at before, it shouldn't be appended
        into results, as we do not want to have duplicate states
    '''
    for i in range(len(state)):
        if state[i]==0:                         #0 means that we have  a potencially legal move
            newState=copy.deepcopy(state)
            newState[i]=whichPlayer
            if newState not in memo:            #if the new state is in memo, that means we have already accounted for it
                results.append(newState)
                memo.append(newState)
                if not ttt.checkForWin(newState,whichPlayer): #here we check if we have not reached a terminal node in graph of states
                    states(newState, change(whichPlayer), memo) #if not, we continue our search

    return None    


## Probably not the most efficient way to check for duplicates, but I need this only once.##
def checkNoDuplicates(L):
    '''
        Takes L - a list. Returns True if there are no duplicates in L and False otherwise
    '''
    for i in range(len(L)):
        newL=copy.deepcopy(L)
        newL.pop(i)
        if L[i] in newL:
            return False
    return True



def states2():
    '''
         First it  calls states, which generates all tic-tac-toe satets given that player1
        starts the game. Now we need to have all states. This is done by taking each state, where
        player 1 starts, replacing 1's with 2's and 2's with 1's and appending into results under the
        condition that it is not there yet. We want to avoid duplicates.
    '''
    states(root,1,[])
    for state in results:
            newState=[0]*9
            for j in range(len(state)):
                if state[j]==1: newState[j]=2
                if state[j]==2: newState[j]=1
            if newState not in results:
                results.append(newState)
    

            

# Takes a long time, but it did return True
#print checkNoDuplicates(results)


def assignScore(state):
    '''
        returns score from perspective of player2 immediately after his move. 
        The higher the score, the better the move for player2 - the ML player. Three rules are implemented:
        -- if 2nd player wins, through a particular move, it'score will be one
        -- if 2nd player will not block 2 marks ni a row of  player 1, then the score will be -0.75 (as platyer 1 will probably win)
        -- if 2nd player will have two in a row, and the missing block is empty, then a score of 0.75 will be assigned
    '''
    Q=0.0
    if ttt.checkForWin(state,2): return 1.0

    matches=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    for match in matches:
        P1=(state[match[0]]+state[match[1]]+state[match[2]]==2 and state[match[0]]!=2 and state[match[1]]!=2 and state[match[2]]!=2) 
        P2=(state[match[0]]+state[match[1]]+state[match[2]]==4 and state[match[0]]!=1 and state[match[1]]!=1 and state[match[2]]!=1) 
        if P1: Q=-0.75
        if P2 and not P1:Q=0.75
    return Q




def fileOutput(L, fileName):
    '''
        This function writes the elements of L into fileName, separated by comma, and without list brackets []
    '''
    for el in L:
        q=assignScore(el)
        el.append(q)
     # Write results into a text file
    counter=0
    f=open(fileName, 'w')
    for el in L:
        if L.index(el)!=len(L)-1:
           f.write(','.join(map(str,el))+'\n')
        else:
            f.write(','.join(map(str,el)))
        counter+=1
    f.close()
    print counter, ' lines written to: ',fileName


states2()
fileOutput(results, 'QTable.txt')
