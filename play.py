
import random,time, copy
from Game import Game
from Player import Player, Player_human, Player_random, Player_minimax, Player_minimax_fast

##G=Game()
p1=Player_human('X')
p2=Player_minimax_fast('Y')
##G.move(1,1,p1)
##print G


def play(player1, player2):
    game=Game()
    print game
    p=1

    stop_game=False

    while not stop_game:
        if p==1:
            plr=player1
        else:
            plr=player2
        #if plr==player2: print plr.score(game)
        xy=plr.chooseMove(game)
        
        
        while game.move(xy[0],xy[1],plr)==None:
            print "Please make a valid move"
            print game
            xy=plr.chooseMove(game)
            

        if  game.check()!=False:
            print game
            print game.check()[1] + ' wins the game!'
            stop_game=True
        elif game.checkTie()==True:
            print game
            print " it's a tie!"
            stop_game=True
        else:
            print game
            time.sleep(0.5)

        p=p*(-1)
        
    return game.getBoard()   

play(p1,p2)
