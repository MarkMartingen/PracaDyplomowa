from graphics import *
import random
import copy


class player(object):
    def __init__(self, symbol):
        self.symbol=symbol
    def getSymbol(self):
        return self.symbol
    def setSymbol(self,newSymbol):
        self.symbol=newSymbol
    def changePlayer(self,whichPlayer):
        ''' Helper function which only flips the player number '''
        if whichPlayer==1:
            return 2
        else:
            return 1


class playerRandom(player):
    def move(self,textObj,win, points, Game, whichPlayer=1):
        '''
            Implements the move for the random player, who chooses randomly from available empty fields
        '''
        if checkForTie(Game) or checkForWin(Game,1) or checkForWin(Game,2) : return  None
        emptyField=[]
        for index in range(9):
            if Game[index]==0:
                emptyField.append(index)
                
        move=random.choice(emptyField)
        return move
    
class playerHuman(player):
    def move(self,textObj,win, points, Game,whichPlayer=1):
        '''
            Implements the move of the human player based on where has she clicked on the canvas
            The human player should always be player number one, therefore the default value
        '''
        if checkForTie(Game) or checkForWin(Game,1) or checkForWin(Game,2): return  None
        EndOfMove=False
        while not EndOfMove: #the loop is needed to wait for the human player to make her move
            mouseCoords=win.checkMouse()
            try:
                x=mouseCoords.getX()
                y=mouseCoords.getY()
                move=0
                for p in points:
                    mytuple=aroundPoint(p,75)
                    if x>=mytuple[0] and x<mytuple[1] and y>=mytuple[2] and y<mytuple[3]:
                        if textObj[move].getText()=='':
                            return move
                    move+=1
            except AttributeError:
                pass


class playerMinimax(player):
    def move(self,textObj,win, points, Game, whichPlayer):
        '''
            Game is the board game that whichPlayer is confronted with and must choose the best possible move
            textObj, win and points are not used. This is only provided, so that the same code can be used to promt a 
            a minimax player to make his move, as well as a human or random player.
            
        '''
        if sum(Game)==0:    # If the board is empty, let the minimax player always choose the middle field. This saves computing time
            move=4
        elif checkForTie(Game) or checkForWin(Game,1) or checkForWin(Game,2):
            return None
        else:               # otherwise use the minimax function to choose the best move
        
            value=-100
            for el in range(9):
                if Game[el]==0:
                    newGame=copy.deepcopy(Game)
                    newGame[el]=whichPlayer
                    nextPlayer=self.changePlayer(whichPlayer)
                    newValue=self.minimax(newGame, False, whichPlayer, nextPlayer,-1000,1000)
                    if newValue>=value:
                        value=newValue
                        move=el
        return move
                        
            
    def minimax(self, Game, maximizing, whichPlayer, nextPlayer,alpha, beta):
        '''
            assumes that whichPlayer has just maded a move which results in a borad configuration given  by Game.
            The next move belongs to the opponent, that is the nextPlayer and she will strive to minimize whichPlayer's total score.
            The maximizing is boolean, and should be True if it is whichPlayer's move and False if nextPlaer's move
            As a result this function will return the final score that whichPlayer will obtain after this move, at the
            end of the game, given off course that the opponent plays accoding to the minimax ideas
        '''
        #check if this is the end of the game and if so return simple score 1 - winning, -1 - loosing, 0 - tie
        if checkForTie(Game): return 0 #This means that we are at terminal node and nobody won, so the score is zero
        if checkForWin(Game,whichPlayer): return 1 # if whichPlayer wins, then the score is 1
        if checkForWin(Game,self.changePlayer(whichPlayer)): return -1 #if the opponent wins, returns -1
        
        if maximizing:
            value=-100
            for el in range(9):
                if Game[el]==0:
                    newGame=copy.deepcopy(Game)
                    newGame[el]=nextPlayer
                    value=max(value, self.minimax(newGame, False,whichPlayer, self.changePlayer(nextPlayer),alpha, beta))
                    alpha=max(alpha, value)
                    if alpha>=beta:
                        break
            return value
        else:
            value=100
            for el in range(9):
                if Game[el]==0:
                    newGame=copy.deepcopy(Game)
                    newGame[el]=nextPlayer
                    value=min(value, self.minimax(newGame, True,whichPlayer, self.changePlayer(nextPlayer),alpha, beta))
                    beta=min(beta, value)
                    if alpha>=beta:
                        break
            return value

                                      
class playerQTable(player):
    def move(self,textObj,win, points, Game, whichPlayer):
        '''
            This function uses a search dictionary QTable which will be read from the file QTable.txt
            For each Game state, the funcion will return legal move for which Qscore is the highest
            textObj, win, points are obsolete - used only by humanPlayer
        '''

        if checkForTie(Game) or checkForWin(Game,1) or checkForWin(Game,2) : return None
        #if QTable does not exist, then we shall upload it from a file and make it global,
        # so that we do not have to upload it for each move seperately
        try:
            QTable
        except NameError:
            global QTable
            QTable={}
            Qfile=open("QTable.txt")
            lines=Qfile.read().splitlines()
            for line in lines:
                numbers=map(float,line.split(","))
                key=tuple(numbers[:9])
                value=float(numbers[-1])
                QTable[key]=value
            QTable[(0,0,0,0,whichPlayer,0,0,0,0)]=1 #if possible, start on the middle of the board
            
            Qfile.close()
        #get all possible moves with the corresponfing Q vale from the dictionary
        possibleMoves=[] 
        for index in range(9):
            if Game[index]==0:
                newGame=copy.deepcopy(Game)
                newGame[index]=whichPlayer
                try:
                    possibleMoves.append((index,QTable[tuple(newGame)]))
                except KeyError:
                    possibleMoves.append((index,0.0))
                    
        #pick the move from possibleMoves with highest Q value
        move=possibleMoves[0] #start with the first possible move
        for element in possibleMoves:
            if element[1]>move[1]:
                move=element
        return move[0]


class playerQTable2(player):
    def move(self,textObj,win, points, Game, whichPlayer):

        #Check if a QTable already exist. If not read it from a file and close the file. The QTable will be global, so that
        # it can live through out the entire game
        try:
            QTable2
        except NameError:
            global QTable2
            QTable2={}
            Qfile=open("QTable2.txt")
            lines=Qfile.read().splitlines()
            for line in lines:
                numbers=map(float,line.split(","))
                t=tuple(numbers[:9])
                key=()
                for e in t: key+=(int(e),)
                value=float(numbers[-1])
                QTable2[key]=value
            Qfile.close()
        
        #get all possible moves with the corresponfing Q vale from the dictionary, if it is not the end of the game. 
        possibleMoves=[]
        if not (checkForTie(Game) or checkForWin(Game,1) or checkForWin(Game,2)):
            for index in range(9):
                if Game[index]==0:
                    newGame=copy.deepcopy(Game)
                    newGame[index]=whichPlayer
                    try:
                        possibleMoves.append((index,QTable2[tuple(newGame)]))
                    except KeyError:
                        possibleMoves.append((index,0.0))
                    
        #pick the move from possibleMoves with highest Q value. If there is more than one with maximum Qvalue, then randomize.
        # If the state is terminal - end of game - then assign zero to Qvalue
        if possibleMoves==[]:
            maxMove=(0,0)
        else:
            maxMoves=[]
            maxMove=possibleMoves[0] #start with the first possible move
            for element in possibleMoves:
                if element[1]>=maxMove[1]:
                    maxMoves.append(element)
            maxMove=random.choice(maxMoves)
            action=copy.deepcopy(Game)
            action[maxMove[0]]=whichPlayer
            action=tuple(action)

        #Check if this is the first move in a game. If no, then update the Qvalue of the previous move/action
        if sum(Game)<=2:
            global actionHistory #This will be a container for states/actions.
            actionHistory=[]
        else:
            #what is the reward? A win renders a reward of +1, a loss -1 and a tie is 0
            if checkForWin(Game, whichPlayer):
                Reward=1
            elif checkForWin(Game, self.changePlayer(whichPlayer)):
                Reward=-1
            else:
                Reward=0

            #Update the Qvalue according to Belleman equations.
            discountRate=0.9
            QTable2[actionHistory[-1]]=Reward+discountRate*maxMove[1]
            
        #Has the game ended? If yes, we need to save QTable into a file with overwritting.
        #Otherwise we append our move/acion into actionHistry and return it and wait for the response of our opponent/system

        if checkForTie(Game) or checkForWin(Game,1) or checkForWin(Game,2):
            self.saveToFile(QTable2,'QTable2.txt')
            del actionHistory
            return None
        else:
            actionHistory.append(action)
            return maxMove[0]


    def saveToFile(self,Dic, fileName):
        f=open(fileName, 'w')
        f.truncate(0)
        for el in Dic.keys():
            if Dic.keys().index(el)!=len(Dic.keys())-1:
               f.write(','.join(map(str,el))+','+str(Dic[el])+'\n')
            else:
                f.write(','.join(map(str,el))+','+str(Dic[el]))
        f.close()
        
        
    
def checkForTie(Game):
    '''
        Takes in a Game board and returns True if is a tie and False otherwise
    '''
    if checkForWin(Game,1)==True or checkForWin(Game,2)==True:
        return False
    else:
        Tie=True
        for el in Game:
            if el==0:
                Tie=False
        return Tie


def checkForWin(Game,whichPlayer):
    '''
        whichPlayer is 1 or 2, depending on what should be checked: winning by player 1 or 2 respectively
        returns True or False
    '''
    matches=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for el in matches:
        if Game[el[0]]==Game[el[1]] and Game[el[1]]==Game[el[2]] and Game[el[0]]==whichPlayer:
            return True
    return False
    
def drawWinLine(t,window):
    '''
        This function takes draws the winning line in case one of the players actually wins the game
        t is a list of textObjects corresponding to the fields on the game board.
        windows is the canvas windows
        The function goes throough all three-in-line textObjects and if all have the same text, a line will be drawn
    '''
    matches=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for el in matches:
        if t[el[0]].getText()==t[el[1]].getText() and  t[el[1]].getText()==t[el[2]].getText() and t[el[0]].getText()!="":
            p1=t[el[0]].getAnchor()
            p2=t[el[2]].getAnchor()
            if el in [(0,1,2),(3,4,5),(6,7,8)]:
                Line(Point(p1.getX()-20,p1.getY()), Point(p2.getX()+20,p2.getY())).draw(window)
            elif el in [(0,3,6),(1,4,7),(2,5,8)]:
                Line(Point(p1.getX(),p1.getY()-20), Point(p2.getX(),p2.getY()+20)).draw(window)
            elif el==(0,4,8):
                Line(Point(p1.getX()-20,p1.getY()-20), Point(p2.getX()+20,p2.getY()+20)).draw(window)
            else:
                Line(Point(p1.getX()+20,p1.getY()-20), Point(p2.getX()-20,p2.getY()+20)).draw(window)
            return True

def drawCommandButton(p1,p2, text):
    ''' Function draws command buttons based on a rectangle given by points p1 and p2.
        Then it adds text to the comand button. Reutrns None.
    '''
    global win
    cmd1=Rectangle(p1,p2)
    cmd1Text=Text(Point(0.5*(p2.getX()+p1.getX()),0.5*(p2.getY()+p1.getY())),text)
    cmd1.setFill('blue')
    cmd1.setOutline('black')
    cmd1Text.setTextColor('white')
    cmd1.draw(win)
    cmd1Text.draw(win)

def checkForPlayer(win, player1):
    '''
        Reutrns the second player (first one is human in this case) depending on whcich button has the user clicked
    '''
    player=None
    
    if player1.getSymbol()=='X':
        playerSymbol='O'
    else:
        playerSymbol='X'
    
            
    while player==None:
        try:
            mouseCoords=win.checkMouse()
            x=mouseCoords.getX()
            y=mouseCoords.getY()
            if x>=20 and x<=100 and y>=560 and y<=590: player=playerHuman(playerSymbol)
            if x>=120 and x<=200 and y>=560 and y<=590:player=playerRandom(playerSymbol)
            if x>=220 and x<=300 and y>=560 and y<=590:player=playerMinimax(playerSymbol)
            if x>=320 and x<=400 and y>=560 and y<=590:player=playerQTable2(playerSymbol)
        except AttributeError:
            pass
    return player
                
def aroundPoint(tuple, extension):
    '''
        take as point represented by a tuple
        takes an extension - float or int 
        creates a tuple representing a frame around the point.
        Will be used to detect if human user has clicked around this point.
    '''
    return (tuple[0]-extension,tuple[0]+extension,tuple[1]-extension,tuple[1]+extension)

def main(player1,player2,display, first=random.choice([1,2]), sleepTime=0.2):
    '''
        main function which governs the process of playing the game.
        Takes player1 and player2, display- which if True will display the canvas, first - 1 or 2 depending
        on who will play first player1 or player2, and sleepTime, so that the computer doesn't make too sudden moves
        The function returns  returns winner=(#wins player1, #wins player2) for statistics
        If player2=None, then display should be True
        The symbol for Player1 should be 'X' or 'O'. Ohterwise player1 will be coerced to 'X' and player2 to 'O'
    '''
    global win
    # setting the canvas and drawing lines
    if display:
        winWidth=600
        winHeight=600
        win=GraphWin("TIC-TAC-TOE", winWidth, winHeight)
        LHT=Line(Point(50,200),Point(550,200))
        LHT.draw(win)
        LHB=Line(Point(50,400),Point(550,400))
        LHB.draw(win)
        LVL=Line(Point(200,50),Point(200,550))
        LVL.draw(win)
        LVR=Line(Point(400,50),Point(400,550))
        LVR.draw(win)

        whoesTurn=Text(Point(500,575),"Pick your oponent...") # will indicate which player is about to make a move
        whoesTurn.draw(win)
        #draw command buttons which enable game mode
        drawCommandButton(Point(20,560), Point(100,590), 'Human Player')
        drawCommandButton(Point(120,560), Point(200,590), 'Ranodm Player')
        drawCommandButton(Point(220,560), Point(300,590), 'Minimax Player')
        drawCommandButton(Point(320,560), Point(400,590), 'QTable Player')

        # Since we are in display mode, the human user may choose his oponent type. Ubless player2 was specified before
        if player2==None:
            player2=checkForPlayer(win,player1)
        
        #prepairing points and text objects around those points
        points=[(125,125),(300,125),(475,125), (125,300),(300,300),(475,300),
               (125,475),(300,475),(475,475)]
        textObj=[] # these are holders for the symbols in the 9 fields of the board game
        for p in points: #initialize textObj with empty string before the start of the game
            textObj.append(Text(Point(p[0],p[1]),""))
            textObj[len(textObj)-1].setSize(36)
    else: #just dummy objects, so that the arguments are passed to functions when display is False
        textObj=[]
        points=[]
        win=[]
    
    # here starts the game
    if first==1:
        first=player1
    else:
        first=player2
    
    Game=[0]*9 #initializing empty game board 0-empty, 1-player1, 2-player2

    endOfGame=False

    while not endOfGame:
        
        if first==player1:
            if display:
                whoesTurn.setText("player's 1 move ....")
                try:
                    whoesTurn.undraw()    
                    whoesTurn.draw(win)
                except GraphicsError:
                    pass
                
                              
            move=player1.move(textObj,win, points,Game,1)
            Game[move]=1                                    
            if display:
                textObj[move].setText(player1.getSymbol())  #set the symbok of the player in the correct text object
                textObj[move].draw(win)                     #draw new game configuration on canvas
            if checkForWin(Game,1):
                if display:
                    drawWinLine(textObj, win)
                endOfGame=True
                player2.move(textObj,win, points,Game,2)    # This is only needed for the QPlayer, so that she can update Qvalues after end of game
                player1.move(textObj,win, points,Game,1)
                winner=(1,0)                                # this is just for stats. 
            if checkForTie(Game):
                endOfGame=True
                winner=(0,0)                                # this is just for stats. 
                player2.move(textObj,win, points,Game,2)    # This is only needed for the QPlayer, so that she can update Qvalues after end of game
                player1.move(textObj,win, points,Game,1)
            first=player2
        else:
            if display:
                whoesTurn.setText("player's 2 move ....")
                try:
                    whoesTurn.undraw()    
                    whoesTurn.draw(win)
                except GraphicsError:
                    pass

            move=player2.move(textObj,win, points,Game,2)
            Game[move]=2                                    
            if display:
                textObj[move].setText(player2.getSymbol())  #set the symbol of the player in the correct text object
                textObj[move].draw(win)                     #draw new game configuration on canvas
            if checkForWin(Game,2):
                if display:
                    drawWinLine(textObj, win)
                endOfGame=True
                winner=(0,1)                                # this is just for stats.
                player1.move(textObj,win, points,Game,1)    # This is only needed for the QPlayer, so that she can update Qvalues after end of game
                player2.move(textObj,win, points,Game,2)
            if checkForTie(Game):
                endOfGame=True
                winner=(0,0)                                # this is just for stats. 
                player1.move(textObj,win, points,Game,1)    # This is only needed for the QPlayer, so that she can update Qvalues after end of game
                player2.move(textObj,win, points,Game,2)
            first=player1
        if display: time.sleep(sleepTime)
        
    if display==True:
        win.close()                                         #when the game has finished, the window should be closed
        return winner
    else:
        return winner

####################################################
if __name__=='__main__':
    pl1=playerHuman('O')
    main(pl1,None,True)


#Checking how  players play against themselves and learning through playing:

def plus(tuple1, tuple2):
    return (tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])

def play(pl1, pl2, numSim):
    statWins=(0,0)
    counter=1
    for i in range(numSim):
        if i>=counter*10:
            print counter*10, ' games played...'
            counter+=1
        statWins=plus(statWins,main(pl1,pl2,False, random.choice([1,2]), 0.0))
    print pl1.getSymbol()+' wins: ' + str(statWins[0]) + ' times'
    print pl2.getSymbol()+' wins: ' + str(statWins[1]) + ' times'
    return None


#play(playerRandom('X'),playerQTable2('0'),1000)





