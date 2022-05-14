#!/usr/bin/env python3
""" Final Project: Computerized Othello, minimax edition  """
__author__="Joshua Graves"
import sys
import os
import random
import helptxt as h
#Player plays BLACK, player moves first
BLACK = '@'
WHITE = 'o'
EMPTY = '.'
OUTER = '?'
UP = -10
DOWN = 10
LEFT = -1
RIGHT = 1
DIAG_UR = -9
DIAG_DR = 11
DIAG_DL = 9
DIAG_UL = -11
DIRECTIONS = (UP, DOWN, LEFT, RIGHT, DIAG_UR, DIAG_DR, DIAG_DL, DIAG_UL)
PIECES = (BLACK, WHITE, EMPTY, OUTER)
DEPTH = 5
class minimaxBot:
    def __init__(self, player):
        self.SQUARE_WEIGHTS=[0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
                            0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
                            0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
                            0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
                            0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
                            0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
                            0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
                            0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
                            0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
                            0,   0,   0,   0,   0,   0,   0,   0,   0,   0]

        self.MAX_DEPTH = DEPTH
        self.x = None
        self.player = player
    def minimax(self, player, board, depth=0, evaluate=None, moves=None): #Def

        if depth == self.MAX_DEPTH: #Limits searching to avoid spending too much time calculating game states
            #print('DOA')
            return evaluate
        else:
            copy = list(board)
            num = 0
            if not moves:
                moves = self.minimaxLegalMoves(player, copy)
            #print(moves)
            if not moves:
               # print('State 2')
                return evaluate
            for move in range(11, 89):
                #print('State 3')
                if moves[move]:
                    num = move
                    movePiece(move, self.player, copy)
                    if evaluate == None:
                       # print('State 4')
                        evaluate = [num, self.value(player, copy)]
                    else:
                        #print('State 5')
                        oppVal = self.minimax(opponent(player), copy, depth+1)
                        if oppVal:
                            val = self.value(player, copy) - oppVal[1]
                        else:
                            val = self.value(player, copy)
                        if val > evaluate[1]:
                            evaluate = [num, val]
                        elif val == evaluate[1]:
                            r = random.randint(1, 2)
                            if r == 1:
                                evaluate = [num, val]
                    moves[move] = False
        #print('HERE!')
        return self.minimax(player, copy, depth+1, evaluate)
    def minimaxLegalMoves(self, player, board):
        valids = []
        for i in range(len(self.SQUARE_WEIGHTS)):
            if i < 11 or i > 88:
                valids+=[False]
            else:
                if isLegal(i, player, board):
                    valids+=[True]
                else:
                    valids+=[False]
        return valids

    def value(self, player, board):
        val = 0
        for square in range(11, 89):
            if board[square] == player:
                val+=self.SQUARE_WEIGHTS[square]
        return val
    def minimaxStrategy(self, player, board):
        self.x = self.minimax(player, board, 0, None)
        return self.x
    def printStuff(self, player, board):
        self.minimaxStrategy(player, board)
        printBoard(board)
        print(self.x)

############################################################ BOARD STATUS AND CONSTRUCTION #############################################


def defaultBoard(): #Makes the board with the default piece placement
    board = [OUTER] * 100
    for i in range(11, 89):
        if 1 <= (i%10) <= 8:
            board[i] = EMPTY
    board[44] = WHITE
    board[55] = WHITE
    board[45] = BLACK
    board[54] = BLACK
    return board

def printBoard(board):
    for row in range(0, 11):
        if row > 0 and row < 9:
            print(row, end = '  ')
        else:
            print('   ', end='')
        if row < 10:
            for col in range(0, 10):
                print(board[(row*10)+col], end = '  ')
        else:
            print('   1  2  3  4  5  6  7  8')
        print()
def opponent(player):
    if player == WHITE:
        return BLACK
    else:
        return WHITE
####################################################### GAMEPLAY #####################################################################
def findBracket(square, player, board, direction):
    bracket = square+direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket+=direction
    if board[bracket] in (OUTER, EMPTY):
        return None
    else:
        return bracket

def isLegal(move, player, board):
    #Create a list of all directions from the current boardstate using all possible directions
    hasBracket = validDirections(move, player, board)
    #if any of the values in hasbracket are true, and the space on the board is unoccupied, it returns true
    if board[move] == EMPTY and any(hasBracket):
        return True
def validDirections(move, player, board):
    valids = []
    for i in DIRECTIONS:
        if findBracket(move, player, board, i) != None:
            valids+=[True]
    return valids
def isValid(move, board):
    try:
        if board[move] != OUTER:
            return True
    except:
        if type(move) != 'int':
            print('Please input an integer value')
        else:
            print('Out of bounds selection')
        return False
def allLegalMoves(player, board):
    valids = []
    for square in range(11, 89):
        if isLegal(square, player, board):
            valids+=[True]
        else:
            valids+=[False]
    return valids
def anyLegalMoves(player, board):
    if True in allLegalMoves(player, board):
        return True
    return False

def movePiece(move, player, board):
    board[move] = player
    for d in DIRECTIONS:
        flip(move, player, board, d)
    return board

def flip(move, player, board, direction):
    bracket = findBracket(move, player, board, direction)
    if not bracket:
        return board
    square = move + direction
    while square != bracket:
        board[square] = player
        square+=direction

############## DRIVERS #########################
def play(player1, player2):
    board = defaultBoard()
    player = BLACK
    print('BLACK: '+BLACK)
    print('WHITE: '+WHITE)
    #Human to Human Match:
    if player1 == 'human' and player2 == 'human':
        while player:
            printBoard(board)
            move = getMove('human', player, board)
            movePiece(move, player, board)
            player = nextPlayer(board, player)
            os.system('cls' if os.name =='nt' else 'clear')

    #Human To Bot Match:
    elif player1 == 'human' and player2 == 'bot':
        #bot = minimaxBot(player)
        #bot.printStuff(player, board)
        turnPlayer = random.randint(1, 2)
        lastMove = None
        if turnPlayer == 1:
            susukichi = minimaxBot(WHITE)
        else:
            susukichi = minimaxBot(BLACK)
        while player:
            printBoard(board)
            if turnPlayer == 1:
                if lastMove:
                    print('Your opponent\'s last move was WHITE to '+str(lastMove))
                if player == BLACK:
                    move = getMove('human', player, board)
                else:
                    move = susukichi.minimaxStrategy(WHITE, board)[0]
            elif turnPlayer == 2:
                if lastMove:
                    print('Your opponent\'s last move was BLACK to '+str(lastMove))
                if player == BLACK:
                    move = susukichi.minimaxStrategy(BLACK, board)[0]
                else:
                    move = getMove('human', player, board)
            lastMove = move
            movePiece(move, player, board)
            player = nextPlayer(board, player)
            os.system('cls' if os.name == 'nt' else 'clear')
    elif player1 == 'bot' and player2 == 'bot':
        lastMove = []
        kaichi = minimaxBot(BLACK)
        susuki = minimaxBot(WHITE)
        while player:
            printBoard(board)
            if lastMove:
                print(lastMove[0]+', '+str(lastMove[1]))
                lastMove = None
            if player == BLACK:
                move = kaichi.minimaxStrategy(BLACK, board)[0]
                lastMove = ['BLACK', move]
            else:
                move = susuki.minimaxStrategy(WHITE, board)[0]
                lastMove = ['WHITE', move]
            movePiece(move, player, board)
            player = nextPlayer(board, player)
    return board, score(BLACK, board)


def nextPlayer(board, previousPlayer):
    opp = opponent(previousPlayer)
    if anyLegalMoves(opp, board):
        return opp
    elif anyLegalMoves(previousPlayer, board):
        return previousPlayer
    return None


def getMove(strategy, player, board):
    if player == WHITE:
        playerS = 'WHITE'
    else:
        playerS = 'BLACK'
    if strategy == 'human':
        try:
            move = int(input('Please input a number for a tile, '+playerS+'\n>>'))
        except KeyboardInterrupt:
            sys.exit(0)
        except ValueError:
            print('Invalid textual input. Please input a valid integer.')
            return getMove(strategy, player, board)
        if(not isValid(int(move), board) or not isLegal(int(move), player, board)):
            if(not isLegal(move, player, board)):
                print('Illegal Move Selection. Please select a valid move.')
            return getMove(strategy, player, board)
        return move
    else: #Bot movements
        return None #Change later
def score(player, board):
    blackScore = 0
    whiteScore = 0
    for square in range(11, 89):
        if board[square] == BLACK:
            blackScore+=1
        elif board[square] == WHITE:
            whiteScore+=1
    return {'Black':blackScore, 'White':whiteScore}

if __name__ == "__main__":
    try:
        if sys.argv[1] != None:
            x = int(sys.argv[1])
            if x <= 0:
                DEPTH = 1
            else:
                DEPTH = x

    finally:
        while(True):
            os.system('cls' if os.name =='nt' else 'clear')
            ans = input('1: Play Othello against a buddy\n2: Play Othello against a bot.\n3: Watch 2 Bots play Othello against each other.\n4: View the help screen.\n5: Close the game.\n>>')
            if int(ans) == 1:
                res = play('human', 'human')
                printBoard(res[0])
                print()
                print('The final score was: '+str(res[1]['Black']) +' to '+str(res[1]['White']))
                q = input('Would you like to do more? Y/N\n>>')
                if q.upper() == 'N':
                    print('Thanks for playing!')
                    sys.exit(0)
            elif int(ans) == 2:
                res = play('human', 'bot')
                printBoard(res[0])
                print()
                print('The final score was: Black '+str(res[1]['Black']) + ' to White ' +str(res[1]['White']))
                q = input('Would you like to do more? Y/N\n>>')
                if q.upper() == 'N':
                    print('Thanks for playing!')
                    sys.exit(0)
            elif int(ans) == 3:
                res = play('bot', 'bot')
                printBoard(res[0])
                print()
                print('The final score was: Black '+str(res[1]['Black']) + ' to White ' +str(res[1]['White']))
                q = input('Would you like to do more? Y/N\n>>')
                if q.upper() == 'N':
                    print('Thanks for playing!')
                    sys.exit(0)
            elif int(ans) == 4:
                h.printmsg()
            elif int(ans) == 5:
                sys.exit(0)
            else:
                print('Please enter 1, 2, 3, 4, or 5.')
                input('Press enter to continue.')
