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


class playerRandom(player):
    def move(self,textObj,win, points, Game, whichPlayer=1):
        '''
            Implements the move for the random player, who chooses randomly from available empty fields
        '''
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
            Game is the board game that whichPlayer is confronted with and must choos the best possible move
            textObj, win and points are not used. This is only provided, so that the same code can be used to promt a 
            a minimax player to make his move, as well as a human or random player.
            
        '''
        if sum(Game)==0:    # If the board is empty, let the minimax player always choose the middle field. This saves computing time
            move=4
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


    def changePlayer(self,whichPlayer):
        ''' Helper function which only flips the player number '''
        if whichPlayer==1:
            return 2
        else:
            return 1
                                  
            
                            
class playerNeural(player):
    ''' TO DO: IMPLEMENT THE NEURAL NET PLAYER '''
    pass

    

def checkForTie(Game):
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
            if x>=320 and x<=400 and y>=560 and y<=590:player=playerNeural(playerSymbol)
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
        drawCommandButton(Point(320,560), Point(400,590), 'ML2 Player')

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
                winner=(1,0)                                # this is just for stats. 
            if checkForTie(Game):
                endOfGame=True
                winner=(0,0)                                # this is just for stats. 

            first=player2
        else:
            whoesTurn.setText("player's 2 move ....")
            try:
                whoesTurn.undraw()    
                whoesTurn.draw(win)
            except GraphicsError:
                pass

            move=player2.move(textObj,win, points,Game,2)
            Game[move]=2                                    
            if display:
                textObj[move].setText(player2.getSymbol())  #set the symbok of the player in the correct text object
                textObj[move].draw(win)                     #draw new game configuration on canvas
            if checkForWin(Game,2):
                if display:
                    drawWinLine(textObj, win)
                endOfGame=True
                winner=(0,1)                                # this is just for stats.
            if checkForTie(Game):
                endOfGame=True
                winner=(0,0)                                # this is just for stats. 
                
            first=player1
        if display: time.sleep(sleepTime)
    
    if display==True:
        win.close()                                         #when the game has finished, the window should be closed
        return winner
    else:
        return winner

####################################################

pl1=playerHuman('O')
pl2=playerRandom('O')
main(pl1,None,True)



# Checking how the random player plays against itself:
##pl1=playerRandom('X')
##pl2=playerRandom('0')
##
##def plus(tuple1, tuple2):
##    return (tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])
##statWins=(0,0)
##for i in range(1000):
##    statWins=plus(statWins,main(pl1,pl2,False, random.choice([1,2]), 0.0))
##print pl1.getSymbol()+' wins: ' + str(statWins[0]) + ' times'
##print pl2.getSymbol()+' wins: ' + str(statWins[1]) + ' times'


# TO DO:


# 2. Add a text objct indicating who's turn it is!
# 3. Add alpha-beta pruning to the minimax algorithm

# 5. Find another ML player - neural nets player


