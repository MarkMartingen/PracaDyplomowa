
from Player import *

class Game(object):
    def __init__(self,Size=3):
        self.Size=Size
        board=[]
        empty_player=Player('-')
        for i in range(Size):
            board.append(['-'])
            for j in range(Size-1,):
                board[i].append('-')
        self.Board=board

    def newBoard(self,board):
        self.Board=board

    def getSize(self): return self.Size
    def getBoard(self): return self.Board
    def setBoard(self,n,m,Player):
        try:
            assert n in range(self.getSize()) and m in range(self.getSize())
            self.Board[n][m]=Player
        except AssertionError:
            print "Invalid move"
    
    def getBoardPosition(self,n,m):
        assert n<=self.getSize() and m<=self.getSize()
        return self.getBoard()[n][m]

    def move(self,n,m,Player):
        if self.getBoardPosition(n,m)!='-':
            return None
        try:
            self.setBoard(n,m,Player)
            return True
        except:
            print 'Invalid move'
            return None

        
    def check(self):
        ''' Checks if one of the players won the game. If so,  returns a list with 
            first argument binef True or False, and the second argument is the name
            of the player that won. If no player one, False is returned'''
        size=self.getSize()
        checklist=[0]*(2*size+2)

        for i in range(size):
            for j in range(size-1):
                if str(self.getBoardPosition(i,j))==str(self.getBoardPosition(i,j+1)) and str(self.getBoardPosition(i,j))!='-':
                    checklist[i]+=1
                if str(self.getBoardPosition(j,i))==str(self.getBoardPosition(j+1,i)) and str(self.getBoardPosition(j,i))!='-':
                    checklist[i+size]+=1
                                
        for i in range(size-1):
            if str(self.getBoardPosition(i,i))==str(self.getBoardPosition(i+1,i+1)) and str(self.getBoardPosition(i,i))!='-':
                checklist[2*size]+=1
            if str(self.getBoardPosition(i,size-i-1))==str(self.getBoardPosition(i+1,size-i-2)) and str(self.getBoardPosition(i,size-i-1))!='-':
                checklist[2*size+1]+=1

        for k in range(len(checklist)):
            if checklist[k]==size-1:
                if k<size:
                    return [True, str(self.getBoardPosition(k,0))]
                elif k<2*size:
                    return [True, str(self.getBoardPosition(0,k-size))]
                elif k==2*size:
                    return [True,str(self.getBoardPosition(0,0))]
                else:
                    return [True,str(self.getBoardPosition(0,size-1))]
                            
        return False

    def checkTie(self):
        empty_slots=False
        for i in range(self.getSize()):
            if '-' in self.getBoard()[i]:
                empty_slots=True
        if self.check()==False and empty_slots==False:
            return True
        else:
            return False
        
    def lastMove(self):
        ''' returnt TRUE if there is only one move to go, and FALSE otherwise'''
        last=0
        for i in range(self.getSize()):
            for j in range(self.getSize()):
                if self.getBoardPosition(i,j)=='-': last+=1
        if last==1:
            return True
        else:
            return False
                
        
    def __str__(self):
        line=''
        for i in range(self.getSize()):
            #line=line+'------\n'
            for j in range(self.getSize()):
                line=line + ' ' + str(self.getBoardPosition(i,j)) +' '
            line=line+'\n'
        return line
        

