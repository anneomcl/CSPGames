from random import randint
from copy import deepcopy
class GameBoard:
    tempBoard=[[1,4,5],
               [2,3,6],
               [9,8,7]]

    tempBoard2=[[1,4],
                [2,3]]

    tempBoard2State=[[0,0],
                     [0,0]]
    minMoves=[]
    maxMoves=[]


def evaluate(node):
    return GameBoard.tempBoard2[node[0]][node[1]]

def isLeaf(node):
    return 1

def getChildren(node, visitedStates):
    #run paradrop
    children=[]
    for r in range(0,len(GameBoard.tempBoard2State)):
        for c in range(0, len(GameBoard.tempBoard2State[r])):
            if visitedStates[r][c] == 0:
                children.append((r,c))

    #run blitz

    return children

global counter
counter=0
def minimax(node, depth, isMax, visitedStates, totalUtil, maxMin, moveList):
    global counter

    visit=deepcopy(visitedStates)
    visit[node[0]][node[1]]=1


    children=getChildren(node, visit)
    if len(children)==0 or depth==0:
        print('...')
        print(maxMin)
        print('...')
        counter=counter +1;

        return maxMin
    if isMax==True:
        v=-1000
        vp=0
        retNode=node
        print('max turn')
        for child in children:
            tempPar=maxMin+GameBoard.tempBoard2[child[0]][child[1]]
            #print(tempPar)
            res= minimax(child,
                                                                depth-1,
                                                                False,
                                                                visit,
                                                                totalUtil,
                                                                tempPar, moveList)
            vp=res

            print(vp)
            if vp > v:
                v=vp
                retNode=child
        moveList[0]=retNode
        return v
    if isMax==False:
        v=1000
        vp=0
        retNode=node
        print('min turn')
        for child in children:
            tempPar=maxMin-GameBoard.tempBoard2[child[0]][child[1]]
            #print(tempPar)
            res= minimax(child,
                        depth-1,
                        True,
                                                                visit,
                                                                totalUtil,
                                                               tempPar, moveList)
            print(vp)
            vp=res

            if vp < v:
                v=vp
                retNode=child
        moveList=retNode
        return v




def buildGameTree(node, depth, visitedStates):

    visit=deepcopy(visitedStates)
    visit[node[0]][node[1]]=1

    print(visit)
    children=getChildren(node, visit)
    if len(children)==0 or depth==0:
        print(node)
    for child in children:
        buildGameTree(child, depth, visit)
    return 1


class Moves:

    def takeEnemyPiece(self, i, j, board, player, opponent):
        board[i][j].color = player.color
        player.score += board[i][j].value
        opponent.score -= board[i][j].value

    def paraDrop(self, i, j, board, player):
        if(board[i][j].color == "white"):
            board[i][j].color = player.color
            player.score += board[i][j].value
            return True
        else:
            return False

    def deathBlitz(self, i, j, board, player, opponent):
        Moves.paraDrop(i, j, board, player)

        if(i > 0):
            if(board[i - 1][j].color == player.oppColor):
                Moves.takeEnemyPiece(i - 1, j, board, player, opponent)
        if(i < 5):
             if(board[i + 1][j].color == player.oppColor):
                Moves.takeEnemyPiece(i + 1, j, board, player, opponent)
        if(j > 0):
            if(board[i][j - 1].color == player.oppColor):
                Moves.takeEnemyPiece(i, j - 1, board, player, opponent)
        if(j < 5):
            if(board[i][j + 1].color == player.oppColor):
                Moves.takeEnemyPiece(i, j + 1, board, player, opponent)

class Player:

    def __init__(self, color):
        self.color = color

        if(color == "blue"):
            self.isFirst = True
            self.oppColor = "green"
        else:
            self.isFirst = False
            self.oppColor = "blue"

        self.score = 0

    def takeTurn(self, move, i, j, board):
        if(move == "paraDrop"):
            turn = Moves.paraDrop(i, j)

        if(turn != True):
            print("Not a valid move")

class Space:

    def __init__(self, val):
        self.value = val
        self.isOccupied = False
        self.color = "white"

class Board:

    def __init__(self, file):
        boardText = open(file,"r")
        board = []

        i = 0
        line = boardText.read().split('\n')
        while(i < 6):
            board.insert(i, line[i].split('\t'))
            j = 0
            while(j < 6):
                board[i][j] = Space(int(board[i][j]))
                j+=1
            i+=1

        self.board = board
        self.isFull = False


#b = Board('C:\\Users\\Anne\\PycharmProjects\\CSPGames\\Resources\\Sevastopol.txt')
#playerBlue = Player("blue")
#playerGreen = Player("green")

def possibleMove():
    return 1
def ageOfBlitz():
    gameInstance=GameBoard()
    #determine first move
    node=(0,0)
    #update gameState
    gameInstance.tempBoard2State[0][0]='a'
    #while(moves are possible)

        #use minimax to get next move
        #update gameState
    #printboard

    return 1
print('----')
moveList=[(-1,-1)]
result=minimax((0,0), 5, False, list(GameBoard.tempBoard2State),0,GameBoard.tempBoard2[0][0], moveList)
print('----')
print(result)
print(moveList)
print(counter)
