# -*- coding: utf-8 -*-

import time
import Reversi
from random import randint
from playerInterface import *

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "Random Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1,-1)
        #moves = [m for m in self._board.legal_moves()]
        #move = moves[randint(0,len(moves)-1)]
        move=self.bestMove()
        self._board.push(move)
        print("I am playing ", move)
        (c,x,y) = move
        assert(c==self._mycolor)
        print("My current board :")
        print(self._board)
        return (x,y) 

    def playOpponentMove(self, x,y):
        assert(self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x,y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    def evaluate(self):
        print("My color : ",self._mycolor)
        
        eval=0

        #Si on trouve un chemin où on a gagné on le choisit
        if(self._board.is_game_over()):
            if ((self._mycolor is self._board._WHITE) and ((self._board._nbWHITE - self._board._nbBLACK)>0)):
                return 1000
            elif((self._board._nbBLACK - self._board._nbWHITE) > 0):
                return 1000

        #Il faut prendre les coins
        color=self._mycolor
        if(self._board._board[0][0]==color or (self._board._nextPlayer==color and self._board.is_valid_move(color,0,0))):
            eval+=400
        if(self._board._board[9][9]==color or (self._board._nextPlayer==color and self._board.is_valid_move(color,9,9))):
            eval+=400
        if(self._board._board[0][9]==color or (self._board._nextPlayer==color and self._board.is_valid_move(color,0,9))):
            eval+=400
        if(self._board._board[9][0]==color or (self._board._nextPlayer==color and self._board.is_valid_move(color,9,0))):
            eval+=400

        #Il ne faut pas donner les coins
        adversaire=self._board._WHITE

        if(self._mycolor is self._board._WHITE):
            adversaire=self._board._BLACK

        print("Adversaire : ",adversaire)

        if(self._board._board[0][1]==color and self._board.is_valid_move(adversaire,0,0)):
            eval+=200
        if(self._board._board[1][0]==color and self._board.is_valid_move(adversaire,0,0)):
            eval+=200
        if(self._board._board[1][1]==color and self._board._board[0][0]==self._board._EMPTY):
            eval-=200

        if(self._board._board[0][8]==color and self._board.is_valid_move(adversaire,0,9)):
            eval+=200
        if(self._board._board[1][9]==color and self._board.is_valid_move(adversaire,0,9)):
            eval+=200
        if(self._board._board[1][8]==color and self._board._board[0][9]==self._board._EMPTY):
            eval-=200

        if(self._board._board[8][1]==color and self._board.is_valid_move(adversaire,9,0)):
            eval+=200
        if(self._board._board[8][0]==color and self._board.is_valid_move(adversaire,9,0)):
            eval+=200
        if(self._board._board[9][1]==color and self._board._board[9][0]==self._board._EMPTY):
            eval-=200

        if(self._board._board[8][8]==color and self._board.is_valid_move(adversaire,9,9)):
            eval+=200
        if(self._board._board[8][9]==color and self._board.is_valid_move(adversaire,9,9)):
            eval+=200
        if(self._board._board[9][8]==color and self._board._board[9][9]==self._board._EMPTY):
            eval-=200

        #Edges valued
        for i in range(self._board._boardsize):
            if(self._board._board[i][0]==color):
                eval+=20
            if(self._board._board[i][9]==color):
                eval+=20
            if(self._board._board[0][i]==color):
                eval+=20
            if(self._board._board[9][i]==color):
                eval+=20

        #Having more pieces than opponent is values, especially late game
        if(self._board._nbWHITE+self._board._nbBLACK>78):
            if(self._mycolor is self._board._BLACK):
                eval+=20*(self._board._nbBLACK-self._board._nbWHITE)
            else:
                eval+=20*(self._board._nbWHITE-self._board._nbBLACK)

        #Minimize their moves mid to late game
        if(self._board._nbWHITE+self._board._nbBLACK>47):

            if(self._mycolor is self._board._WHITE):
                self._board._nextPlayer=self._board._BLACK
                moves=self._board.legal_moves()
                if(len(moves)==0):
                    eval+=200
                elif(len(moves)<3):
                    eval+=100
                else:
                    eval-=len(moves)*25
                self._board._nextPlayer=self._board._WHITE

            else:
                self._board._nextPlayer=self._board._WHITE
                moves=self._board.legal_moves()
                if(len(moves)==0):
                    eval+=200
                elif(len(moves)<3):
                    eval+=100
                else:
                    eval-=len(moves)*25     
                self._board._nextPlayer=self._board._BLACK
        
        return eval

    def heuristique(self):
        '''if self._mycolor is self._board._WHITE:
            return self._board._nbWHITE - self._board._nbBLACK
        return self._board._nbBLACK - self._board._nbWHITE'''
        return self.evaluate()

    def minimax(self,depth,maximizingPlayer):
        if(depth==0):
            return self.heuristique()

        if maximizingPlayer:
            value=-float('infinity')
            for m in self._board.legal_moves():
                self._board.push(m)
                value=max(value,self.minimax(depth-1,False))
                self._board.pop()
            return value
        else:
            value=float('infinity')
            for m in self._board.legal_moves():
                self._board.push(m)
                value=min(value,self.minimax(depth-1,True))
                self._board.pop()
            return value

    def bestMove(self):
        debut=time.time()
        maxpoints=-float('infinity')
        for i in range(1,2):
            for m in self._board.legal_moves():
                self._board.push(m)
                points=self.minimax(i-1,False)
                self._board.pop()
                print("Move : ",m," Profondeur : ",i," Points : ",points," Maxpoints : ",maxpoints)

                if points>=maxpoints:
                    maxpoints=points
                    mx=m[1]
                    my=m[2]

        time.sleep(1800)



        return [self._board._nextPlayer,mx,my]











