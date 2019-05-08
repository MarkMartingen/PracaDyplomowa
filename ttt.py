from graphics import *
import random
import copy
import numpy as np
import sys
import neural as nn

# USED CONSTANTS:
BOARD_SIZE = 9
MIN_MINIMAX_VALUE = -1000
MAX_MINIMAX_VALUE = 1000
MATCHES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
# MATCHES represents board configurations that result in a win E.g. (0,1,2)


class QTable(object):
    def __init__(self, file_name, q_table={}):
        global q_file
        self.file_name = file_name
        self.q_table = q_table
        try:
            q_file = open(file_name)
            lines = q_file.read().splitlines()
            for line in lines:
                numbers = map(float, line.split(","))
                key = tuple(map(int, numbers[:BOARD_SIZE]))
                value = numbers[-1]
                q_table[key] = value
        except IOError:
            pass
        q_file.close()

    def save_to_file(self):
        """
            Saves QTable dictionary into the file fileName
            the keys are tuples of length 9, representing board states and the values a are  Qvalues
            represented by floats
        """
        f = open(self.file_name, 'w')
        f.truncate(0)  # I think open(..., 'w') implies truncate
        for el in self.q_table.keys():
            if self.q_table.keys().index(el) != len(self.q_table.keys()) - 1:
                f.write(','.join(map(str, el)) + ',' + str(self.q_table[el]) + '\n')
            else:
                f.write(','.join(map(str, el)) + ',' + str(self.q_table[el]))
        f.close()



class Player(object):
    def __init__(self, symbol):
        self._symbol = symbol

    @property
    def symbol(self):
        return self._symbol

    def changePlayer(self, whichPlayer):
        """ Helper function which only flips the player number """
        return 2 if whichPlayer == 1 else 1


class playerRandom(Player):
    def move(self, Game,  ** keyword_parameters):
        """
            Implements the move for the random player, who chooses randomly from available empty fields
        """
        if checkForTie(Game) or checkForWin(Game, 1) or checkForWin(Game, 2):
            return None
        emptyField = []
        for index in range(BOARD_SIZE):
            if Game[index] == 0:
                emptyField.append(index)

        move = random.choice(emptyField)
        return move


class playerHuman(Player):
    def move(self, Game,  ** keyword_parameters):
        # Arguments also should be explained in the docstring
        """
            Implements the move of the human player based on where has she clicked on the canvas
            The human player should always be player number one, therefore the default value
        """
        points = keyword_parameters['points']
        win = keyword_parameters['win']
        textObj = keyword_parameters['textObj']

        if checkForTie(Game) or checkForWin(Game, 1) or checkForWin(Game, 2):
            return None

        while True:  # the loop is needed to wait for the human player to make her move
            mouseCoords = win.checkMouse()
            try:
                x = mouseCoords.getX()
                y = mouseCoords.getY()
                move = 0
                for p in points:
                    mytuple = aroundPoint(p, 75)
                    if mytuple[0] <= x < mytuple[1] and mytuple[2] <= y < mytuple[3]:
                        if textObj[move].getText() == '':
                            return move
                    move += 1
            except AttributeError:
                pass


class playerMinimax(Player):
    def move(self, Game, ** keyword_parameters):
        """
            Game is the board game that whichPlayer is confronted with and must choose the best possible move
            textObj, win and points are not used. This is only provided, so that the same code can be used to promt a
            a minimax player to make his move, as well as a human or random player.

        """
        whichPlayer = keyword_parameters['whichPlayer']
        if sum(Game) == 0:  # If the board is empty, let the minimax player always choose the middle field.
            # This saves computing time
            return 4
        if checkForTie(Game) or checkForWin(Game, 1) or checkForWin(Game, 2):
            return None
         # otherwise use the minimax function to choose the best move

        value = MIN_MINIMAX_VALUE
        for el in range(BOARD_SIZE):
            if Game[el] == 0:
                newGame = copy.deepcopy(Game)
                newGame[el] = whichPlayer
                nextPlayer = self.changePlayer(whichPlayer)
                # This approach is quite ineffective, because it traverses all permutations
                # I propose to create a lookup tree and update it as necessary
                newValue = self.minimax(newGame, False, whichPlayer, nextPlayer, MIN_MINIMAX_VALUE, MAX_MINIMAX_VALUE)
                if newValue >= value:
                    value = newValue
                    move = el
        return move

    def minimax(self, Game, maximizing, whichPlayer, nextPlayer, alpha, beta):
        """
            assumes that whichPlayer has just maded a move which results in a borad configuration given  by Game.
            The next move belongs to the opponent, that is the nextPlayer and she will strive to minimize whichPlayer's total score.
            The maximizing is boolean, and should be True if it is whichPlayer's move and False if nextPlayer's move
            As a result this function will return the final score that whichPlayer will obtain after this move, at the
            end of the game, given off course that the opponent plays according to the minimax ideas
        """
        # check if this is the end of the game and if so return simple score 1 - winning, -1 - loosing, 0 - tie
        if checkForTie(Game):  # This means that we are at terminal node and nobody won, so the score is zero
            return 0
        if checkForWin(Game, whichPlayer):
            return 1  # if whichPlayer wins, then the score is 1
        if checkForWin(Game, self.changePlayer(whichPlayer)):
            return -1  # if the opponent wins, returns -1

        if maximizing:
            value = MIN_MINIMAX_VALUE
            for el in range(BOARD_SIZE):
                if Game[el] == 0:
                    newGame = copy.deepcopy(Game)
                    newGame[el] = nextPlayer
                    value = max(value,
                                self.minimax(newGame, False, whichPlayer, self.changePlayer(nextPlayer), alpha, beta))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = MAX_MINIMAX_VALUE
            for el in range(9):
                if Game[el] == 0:
                    newGame = copy.deepcopy(Game)
                    newGame[el] = nextPlayer
                    value = min(value,
                                self.minimax(newGame, True, whichPlayer, self.changePlayer(nextPlayer), alpha, beta))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value


class playerQTable(Player):
    def move(self, Game, ** keyword_parameters):

        whichPlayer =  keyword_parameters['whichPlayer']
        QTable = QVT.q_table

        # get all possible moves with the corresponding Q vale from the dictionary, if it is not the end of the game.
        possibleMoves = []
        if not (checkForTie(Game) or checkForWin(Game, 1) or checkForWin(Game, 2)):
            for index in range(9):
                if Game[index] == 0:
                    newGame = copy.deepcopy(Game)
                    newGame[index] = whichPlayer
                    try:
                        possibleMoves.append((index, QTable[tuple(newGame)]))
                    except KeyError:
                        possibleMoves.append((index, 0.0))

        # pick the move from possibleMoves with highest Q value. If the state is terminal - end of game -
        # then assign zero to Qvalue
        if possibleMoves == []:
            maxMove = (0, 0)
        else:
            maxMove = sorted(possibleMoves, key=lambda x: x[1], reverse=True)[0]

            # Special case when the board is empty, start with the middle position
            if sum(Game) == 0:
                maxMove = 4, 1
            # action is the chosen action by player. It is represented as a new state of the game
            action = copy.deepcopy(Game)
            action[maxMove[0]] = whichPlayer
            action = tuple(action)

        # Check if this is the first move in a game. If no, then update the Qvalue of the previous move/action
        if sum(Game) <= 2:
            global actionHistory  # This will be a container for states/actions.
            actionHistory = []
        else:
            # what is the reward of the previous action? A win renders a reward of +1, a loss -1 and a tie is 0.75
            # Other wise reward is zero. A tie is basically something good in tic-tac-toe.
            # The best players will always tie when playing against each other.
            if checkForWin(Game, whichPlayer):
                Reward = 1
            elif checkForWin(Game, self.changePlayer(whichPlayer)):
                Reward = -1
            elif checkForTie(Game):
                Reward = 0.75
            else:
                Reward = 0

            # Update the Qvalue according to Belleman equations.
            discountRate = 0.7
            learning_rate = 0.1
            try:
                QTable[actionHistory[-1]] = QTable[actionHistory[-1]] + learning_rate * (
                        Reward + discountRate * maxMove[1] - QTable[actionHistory[-1]])
            except KeyError:  # When previous action had no Q-value assigned, we tale learning rate equal zero
                QTable[actionHistory[-1]] = Reward + discountRate * maxMove[1]

        # Has the game ended? If not yet, we need to  append our move/acion into actionHistory
        # and return it and wait for the response of our opponent/system

        if checkForTie(Game) or checkForWin(Game, 1) or checkForWin(Game, 2):
            del actionHistory
            return None
        else:
            actionHistory.append(action)
            return maxMove[0]


class playerNeural(Player):
    def move(self, Game, ** keyword_parameters):
        # get all possible moves into one list, and get all possible
        # corresponding states into a dictionary. The state will be the
        # key and the score of winning will be the value
        whichPlayer = keyword_parameters['whichPlayer']
        possibleMoves = []
        possibleStates = {}
        if not (checkForTie(Game) or checkForWin(Game, 1) or checkForWin(Game, 2)):
            for index in range(BOARD_SIZE):
                if Game[index] == 0:
                    possibleMoves.append(index)
                    newGame = copy.deepcopy(Game)
                    newGame[index] = whichPlayer
                    possibleStates[tuple(newGame)] = 0

            # ask the network which out of the possible states returns the highest
            # score of winning:
            for state in possibleStates.keys():
                possibleStates[state] = QNet.predict(np.array(state).reshape(BOARD_SIZE, 1))
            # choose the move with the highest q-vaue or pick one randomly with probability epsilon

            epsilon = 0.07
            if random.random() <= epsilon:
                maxState = random.choice(possibleStates.items())[0]
            else:
                maxState = max(possibleStates.items(), key=lambda x: x[1][0, 0])[0]

            # find the corresponding move (integer from 0 to 9):
            for i in range(len(Game)):
                if Game[i] != maxState[i]:
                    maxMove = i

        else:  # the game has ended, hence we do not need a maxMove.
            maxMove = None

        # if this the first move in the game of whichPlayer,
        # then we should do two things:
        # 1. create a list actionHistory, where following moves will be logged
        # 2. return the move corresponding to center position 4 is whichPlayer
        # makes the first move on an empty board
        try:
            actionHistory
        except NameError:
            global actionHistory
            actionHistory = []

        if sum(Game) == 0:  # if the AI agent makes the first move he will simply opt fot the middle of the board
            return 4

        if len(actionHistory) >= 1:
            # Before returning the maxMove, we want to give feedback to
            # the network (reinforcement learning) so that it can
            # improve weights:
            if checkForWin(Game, whichPlayer):
                Reward = 100
                maxMove_qvalue = 0
            elif checkForWin(Game, self.changePlayer(whichPlayer)):
                Reward = 0.5
                maxMove_qvalue = 0
            elif checkForTie(Game):
                Reward = 75
                maxMove_qvalue = 0
            else:
                Reward = 1
                maxMove_qvalue = possibleStates[maxState]
            # Set hyperparameters
            discountRate = 1.0
            learning_rate = 0.01

            # Train the network - based on one observation.
            # The target value (label) of the previous action by Belleman equations:

            Qtarget = QNet.predict(np.array(actionHistory[-1]).reshape(BOARD_SIZE, 1)) + learning_rate * (
                Reward + discountRate * maxMove_qvalue -
                QNet.predict(np.array(actionHistory[-1]).reshape(BOARD_SIZE, 1)))

            # Pass to the network, so that it adjusts weights
            QNet.train_model(np.array(actionHistory[-1]), Qtarget)

        # We will finally return the maxMove, but prior to that update
        # actionHistory with the state that will follow ater maxMove
        if maxMove != None:
            actionHistory.append(maxState)
        else:  # this means, that the game has ended, se we delete actionHistory
            del actionHistory
        return maxMove


def checkForTie(Game):
    """
        Takes in a Game board and returns True if is a tie and False otherwise
    """
    if checkForWin(Game, 1) or checkForWin(Game, 2):
        return False
    return True if reduce(lambda x, y: x * y, Game) else False


def checkForWin(Game, whichPlayer):
    """
        whichPlayer is 1 or 2, depending on what should be checked: winning by player 1 or 2 respectively
        returns True or False
    """
    for el in MATCHES:
        if Game[el[0]] == Game[el[1]] and Game[el[1]] == Game[el[2]] and Game[el[0]] == whichPlayer:
            return True
    return False


def drawWinLine(t, window):
    """
        This function takes draws the winning line in case one of the players actually wins the game
        t is a list of textObjects corresponding to the fields on the game board.
        windows is the canvas windows
        The function goes through all three-in-line textObjects and if all have the same text, a line will be drawn
    """
    for el in MATCHES:
        if not (not (t[el[0]].getText() == t[el[1]].getText()) or not (
                t[el[1]].getText() == t[el[2]].getText()) or not (t[el[0]].getText() != "")):
            p1 = t[el[0]].getAnchor()
            p2 = t[el[2]].getAnchor()
            if el in [(0, 1, 2), (3, 4, 5), (6, 7, 8)]:
                Line(Point(p1.getX() - 20, p1.getY()), Point(p2.getX() + 20, p2.getY())).draw(window)
            elif el in [(0, 3, 6), (1, 4, 7), (2, 5, 8)]:
                Line(Point(p1.getX(), p1.getY() - 20), Point(p2.getX(), p2.getY() + 20)).draw(window)
            elif el == (0, 4, 8):
                Line(Point(p1.getX() - 20, p1.getY() - 20), Point(p2.getX() + 20, p2.getY() + 20)).draw(window)
            else:
                Line(Point(p1.getX() + 20, p1.getY() - 20), Point(p2.getX() - 20, p2.getY() + 20)).draw(window)
            return True


def drawCommandButton(p1, p2, text):
    """
        Function draws command buttons based on a rectangle given by points p1 and p2.
        Then it adds text to the comand button. Reutrns None.
    """
    global win
    cmd1 = Rectangle(p1, p2)
    cmd1Text = Text(Point(0.5 * (p2.getX() + p1.getX()), 0.5 * (p2.getY() + p1.getY())), text)
    cmd1.setFill('blue')
    cmd1.setOutline('black')
    cmd1Text.setTextColor('white')
    cmd1.draw(win)
    cmd1Text.draw(win)


def checkForPlayer(win, player1):
    """
        Reutrns the second player (first one is human in this case) depending on whcich button has the user clicked
    """
    plr = None

    if player1.symbol == 'X':
        playerSymbol = 'O'
    else:
        playerSymbol = 'X'

    while plr is None:
        try:
            mouseCoords = win.checkMouse()
            x = mouseCoords.getX()
            y = mouseCoords.getY()
            if 10 <= x <= 90 and 560 <= y <= 590:
                plr = playerHuman(playerSymbol)
            if 100 <= x <= 180 and 560 <= y <= 590:
                plr = playerRandom(playerSymbol)
            if 190 <= x <= 270 and 560 <= y <= 590:
                plr = playerMinimax(playerSymbol)
            if 280 <= x <= 360 and 560 <= y <= 590:
                plr = playerQTable(playerSymbol)
            if 370 <= x <= 450 and 560 <= y <= 590:
                plr = playerNeural(playerSymbol)
        except AttributeError:
            pass
    return plr


def aroundPoint(t, extension):
    """
        take as point represented by a tuple t
        takes an extension - float or int
        creates a tuple representing a frame around the point.
        Will be used to detect if human user has clicked around this point.
    """
    return t[0] - extension, t[0] + extension, t[1] - extension, t[1] + extension


def main(player1, player2, display, first=random.choice([1, 2]), sleepTime=0.2, QTab=None, QN=None):
    """
        main function which governs the process of playing the game.
        Takes player1 and player2, display- which if True will display the canvas, first - 1 or 2 depending
        on who will play first player1 or player2, and sleepTime, so that the computer doesn't make too sudden moves
        The function returns  returns winner=(#wins player1, #wins player2) for statistics
        If player2=None, then display should be True
        The symbol for Player1 should be 'X' or 'O'. Otherwise player1 will be coerced to 'X' and player2 to 'O'
    """
    global QVT  # Q Value Table Object
    if QTab is None:
        QVT = QTable('QTable.txt')
    else:
        QVT = QTab

    global QNet
    if QN is None:
        QNet = nn.QNetwork()
    else:
        QNet = QN
    global win
    # setting the canvas and drawing lines
    if display:
        winWidth = 600
        winHeight = 600
        win = GraphWin("TIC-TAC-TOE", winWidth, winHeight)
        LHT = Line(Point(50, 200), Point(550, 200))
        LHT.draw(win)
        LHB = Line(Point(50, 400), Point(550, 400))
        LHB.draw(win)
        LVL = Line(Point(200, 50), Point(200, 550))
        LVL.draw(win)
        LVR = Line(Point(400, 50), Point(400, 550))
        LVR.draw(win)

        whoesTurn = Text(Point(525, 575), "Pick your opponent...")  # will indicate which player is about to make a move
        whoesTurn.draw(win)
        # draw command buttons which enable game mode
        drawCommandButton(Point(10, 560), Point(90, 590), 'Human Player')
        drawCommandButton(Point(100, 560), Point(180, 590), 'Random Player')
        drawCommandButton(Point(190, 560), Point(270, 590), 'Minimax Player')
        drawCommandButton(Point(280, 560), Point(360, 590), 'QTable Player')
        drawCommandButton(Point(370, 560), Point(450, 590), 'Neural Player')

        # Since we are in display mode, the human user may choose his opponent type. Unless player2 was specified before
        if player2 is None:
            player2 = checkForPlayer(win, player1)

        # preparing points and text objects around those points
        points = [(125, 125), (300, 125), (475, 125), (125, 300), (300, 300), (475, 300),
                  (125, 475), (300, 475), (475, 475)]
        textObj = []  # these are holders for the symbols in the 9 fields of the board game
        for p in points:  # initialize textObj with empty string before the start of the game
            textObj.append(Text(Point(p[0], p[1]), ""))
            textObj[len(textObj) - 1].setSize(36)
    else:  # just dummy objects, so that the arguments are passed to functions when display is False
        textObj = []
        points = []
        win = []

    # here starts the game
    if first == 1:
        first = player1
    else:
        first = player2

    Game = [0] * 9  # initializing empty game board 0-empty, 1-player1, 2-player2

    endOfGame = False

    while not endOfGame:

        if first == player1:
            if display:
                whoesTurn.setText("player's 1 move ....")
                try:
                    whoesTurn.undraw()
                    whoesTurn.draw(win)
                except GraphicsError:
                    pass
            move = player1.move(Game, textObj=textObj, win=win, points=points, whichPlayer=1)
            Game[move] = 1
            if display:
                textObj[move].setText(player1.symbol)  # set the symbol of the player in the correct text object
                textObj[move].draw(win)  # draw new game configuration on canvas
            if checkForWin(Game, 1):
                if display:
                    drawWinLine(textObj, win)
                endOfGame = True
                player2.move(Game, textObj=textObj, win=win, points=points, whichPlayer=2)
                player1.move(Game, textObj=textObj, win=win, points=points, whichPlayer=1)
                # This is only needed for the QPlayer, so that she can update Qvalues after end of game
                winner = (1, 0)  # this is just for stats.
            if checkForTie(Game):
                endOfGame = True
                winner = (0, 0)  # this is just for stats.
                player2.move(Game, textObj=textObj, win=win, points=points, whichPlayer=2)
                player1.move(Game, textObj=textObj, win=win, points=points, whichPlayer=1)
                # This is only needed for the QPlayer, so that she can update Qvalues after end of game
            first = player2
        else:
            if display:
                whoesTurn.setText("player's 2 move ....")
                try:
                    whoesTurn.undraw()
                    whoesTurn.draw(win)
                except GraphicsError:
                    pass
            move = player2.move(Game, textObj=textObj, win=win, points=points, whichPlayer=2)
            Game[move] = 2
            if display:
                textObj[move].setText(player2.symbol)  # set the symbol of the player in the correct text object
                textObj[move].draw(win)  # draw new game configuration on canvas
            if checkForWin(Game, 2):
                if display:
                    drawWinLine(textObj, win)
                endOfGame = True
                winner = (0, 1)  # this is just for stats.
                player1.move(Game, textObj=textObj, win=win, points=points, whichPlayer=1)
                player2.move(Game, textObj=textObj, win=win, points=points, whichPlayer=2)
                # This is only needed for the QPlayer, so that she can update Qvalues after end of game
            if checkForTie(Game):
                endOfGame = True
                winner = (0, 0)  # this is just for stats.
                player1.move(Game, textObj=textObj, win=win, points=points, whichPlayer=1)
                player2.move(Game, textObj=textObj, win=win, points=points, whichPlayer=2)
                # This is only needed for the QPlayer, so that she can update Qvalues after end of game
            first = player1
        if display:
            time.sleep(sleepTime)

    if display:
        win.close()  # when the game has finished, the window should be closed
    return winner


# Checking how players play against themselves and learning through playing:
def plus(tuple1, tuple2):
    return tuple1[0] + tuple2[0], tuple1[1] + tuple2[1]


def play(pl1, pl2, numSim):
    """
        pl2 and pl2 - players that will play against each other
        numSim - number of games played
        play returns None, but it prints out stats - number of wins and ties for each player
    """
    statWins = (0, 0)
    counter = 1
    global QVT, QNet
    QVT = QTable('QTable.txt')
    QNet = nn.QNetwork()
    for i in range(numSim):
        if i >= counter * 10:
            print counter * 10, ' games played...'
            counter += 1
        statWins = plus(statWins, main(pl1, pl2, False, random.choice([1, 2]), 0.0, QVT, QNet))
    print pl1.symbol + ' wins: ' + str(statWins[0]) + ' times. Prcnt: ', float(statWins[0]) / numSim

    print pl2.symbol + ' wins: ' + str(statWins[1]) + ' times. Prcnt: ', float(statWins[1]) / numSim

    print ' there were ', numSim - statWins[0] - statWins[1], ' ties. Prcnt: ', \
        float(numSim - statWins[0] - statWins[1]) / numSim
    return None


####################################################
if __name__ == '__main__':
    if sys.argv[1] == 'play':
        pl1 = playerHuman('O')
        main(pl1, None, True)

    if sys.argv[1] == 'train':
        play(playerRandom('X'), playerNeural('0'), 500)
        QNet.save()
        #QVT.save_to_file()

