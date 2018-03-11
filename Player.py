
import copy, random,Game


class Player(object):
    ''' class holding only the name of the player. Playing logic will be
    implemented in subsequent subclasses'''
    def __init__(self, name):
        self.Name=name
    def setName(self,name):
        self.Name=name
    def getName(self): return self.Name

    def score(self, game):
        ''' heuristic function returning the score for Player, for any given board,
        given that the player is about to move '''
        score=0
    
        '''if player is to win in this move score: 10^board size'''

        '''check rows'''
        
        for i in range(game.getSize()):
            counter=0
            for j in range(game.getSize()):
                if str(game.getBoardPosition(i,j))!=self.Name and str(game.getBoardPosition(i,j))!='-':
                    counter=0
                    break
                elif str(game.getBoardPosition(i,j))==self.Name:
                    counter+=1
            if counter>0:
                score+=10**counter
                #print "row ",score,counter

        ''' check columns '''
        
        for i in range(game.getSize()):
            counter=0
            for j in range(game.getSize()):
                if str(game.getBoardPosition(j,i))!=self.Name and str(game.getBoardPosition(j,i))!='-':
                    counter=0
                    break
                elif str(game.getBoardPosition(j,i))==self.Name:
                    counter+=1
            if counter>0:
                score+=10**counter
                #print "col ",score,counter

        ''' check the two diagonals'''
        size=game.getSize()-1

        counter=0
        for i in range(game.getSize()):
            if str(game.getBoardPosition(i,i))!=self.Name and str(game.getBoardPosition(i,i))!='-':
                counter=0
                break
            elif str(game.getBoardPosition(i,i))==self.Name:
                counter+=1
        if  counter>0 :
            score+=10**counter
            #print "diag1 ",score,counter

        counter=0
        for i in range(game.getSize()):
            if str(game.getBoardPosition(i,size-i))!=self.Name and str(game.getBoardPosition(i,size-i))!='-':
                counter=0
                break
            if str(game.getBoardPosition(i,size-i))==self.Name:
                counter+=1                                     
        if counter>0:
            score+=10**counter
            #print "diag2 ", score,counter
        return score
        

    def __str__(self):
        return str(self.getName())

class Player_human(Player):
    def chooseMove(self,G):
        stop=False
        while not stop:
            print "Player "+str(self)+ " please make a move"
            try:
                x=int(raw_input('give the x position 1,2,3... '))
                y=int(raw_input('give the y position 1,2,3... '))
                stop=True
                return (x-1,y-1)
            except ValueError:
                print "Please make a valid move!"


class Player_random(Player):
    def chooseMove(self,G):
        empty_slots=[]
        for i in range(G.getSize()):
            for j in range(G.getSize()):
                if G.getBoardPosition(i,j)=='-':
                    empty_slots.append((i,j))
        return random.choice(empty_slots)


class Player_minimax(Player):

    def chooseMove(self,G):
        moves={}
        for i in range(G.getSize()):
                for j in range(G.getSize()):
                    if str(G.getBoardPosition(i,j))=='-':
                        moves[(i,j)]=-1
        
        for move in moves.keys():
            board=copy.deepcopy(G.getBoard())
            board[move[0]][move[1]]=self
            newG=Game.Game(G.getSize())
            newG.newBoard(board)

            moves[move]=self.minimax(newG,False)
        
        best=-1
        key=random.choice(moves.keys())
        for move in moves.keys():
            if moves[move]>best:
                best=moves[move]
                key=move

        return key
        
    def minimax(self, G, maximizingPlayer):
        ''' create a copy of the game '''
        size=G.getSize()
        copyG=Game.Game(size)
        other=Player('other')
        board=copy.deepcopy(G.getBoard())
        copyG.newBoard(board)

        
        for i in range(copyG.getSize()):
            for j in range(copyG.getSize()):
                if str(copyG.getBoardPosition(i,j))!=str(self) and copyG.getBoardPosition(i,j)!='-':
                    copyG.setBoard(i,j,other)
        
        ''' check if it is the last move and if so return the value of this leaf'''

        if copyG.checkTie()==True:
            return 0
        if copyG.check()!=False:
            if copyG.check()[1]==str(self):
                return 1
            else:
                return -1
        
        if maximizingPlayer:
            bestValue=-1000
            for i in range(copyG.getSize()):
                for j in range(copyG.getSize()):
                    if copyG.getBoardPosition(i,j)=='-':
                        newBoard=copy.deepcopy(copyG.getBoard())
                        newBoard[i][j]=self
                        newG=Game.Game(copyG.getSize())
                        newG.newBoard(newBoard)
                        v=self.minimax(newG, False)
                        bestValue=max(bestValue, v)
            return bestValue
        else:
            bestValue=1000
            for i in range(copyG.getSize()):
                for j in range(copyG.getSize()):
                    if copyG.getBoardPosition(i,j)=='-':
                        newBoard=copy.deepcopy(copyG.getBoard())
                        newBoard[i][j]=other
                        newG=Game.Game(copyG.getSize())
                        newG.newBoard(newBoard)
                        v=self.minimax(newG, True)
                        bestValue=min(bestValue, v)
            return bestValue



class Player_minimax_fast(Player):

    def chooseMove(self,G):
        moves={}
        for i in range(G.getSize()):
                for j in range(G.getSize()):
                    if str(G.getBoardPosition(i,j))=='-':
                        moves[(i,j)]=-1
        
        for move in moves.keys():
            board=copy.deepcopy(G.getBoard())
            board[move[0]][move[1]]=self
            newG=Game.Game(G.getSize())
            newG.newBoard(board)

            moves[move]=self.minimax(newG,-100,100,False)
        
        best=-1
        key=random.choice(moves.keys())
        for move in moves.keys():
            if moves[move]>best:
                best=moves[move]
                key=move
        return key
        
    def minimax(self, G, alfa, beta, maximizingPlayer):
        ''' create a copy of the game '''
        size=G.getSize()
        copyG=Game.Game(size)
        other=Player('other')
        board=copy.deepcopy(G.getBoard())
        copyG.newBoard(board)

        
        for i in range(copyG.getSize()):
            for j in range(copyG.getSize()):
                if str(copyG.getBoardPosition(i,j))!=str(self) and copyG.getBoardPosition(i,j)!='-':
                    copyG.setBoard(i,j,other)
        
        ''' check if it is the last move and if so return the value of this leaf'''

        if copyG.checkTie()==True:
            return 0
        if copyG.check()!=False:
            if copyG.check()[1]==str(self):
                return 1
            else:
                return -1
        
        if maximizingPlayer:
            bestValue=-1000
            
            for i in range(copyG.getSize()):
                for j in range(copyG.getSize()):
                    if copyG.getBoardPosition(i,j)=='-':
                        newBoard=copy.deepcopy(copyG.getBoard())
                        newBoard[i][j]=self
                        newG=Game.Game(copyG.getSize())
                        newG.newBoard(newBoard)
                        v=self.minimax(newG,alfa, beta, False)
                        bestValue=max(bestValue, v)
                        alfa=max(alfa,bestValue)
                        if beta<=alfa:
                            break
            return bestValue
        else:
            bestValue=1000
            for i in range(copyG.getSize()):
                for j in range(copyG.getSize()):
                    if copyG.getBoardPosition(i,j)=='-':
                        newBoard=copy.deepcopy(copyG.getBoard())
                        newBoard[i][j]=other
                        newG=Game.Game(copyG.getSize())
                        newG.newBoard(newBoard)
                        v=self.minimax(newG,alfa, beta, True)
                        bestValue=min(bestValue, v)
                        beta=min(beta,bestValue)
                        if beta<=alfa:
                            break
            return bestValue




