from random import randint
from copy import deepcopy
from collections import defaultdict


class GameBoard:
    boardSize=6
    tempBoard=[[1,4,5],
               [2,3,6],
               [9,8,7]]

    tempBoard2=[[1,2],
                [3,4]]

    tempBoard2State=[[0,0],
                     [0,0]]
    minMoves=[]
    maxMoves=[]


def evaluate(currentValue, node, expansionType):
    return (currentValue, node, expansionType)

def isLeaf(node):
    return 1


def getChildren(visitedStates, gameInstance,isMax):
    #run paradrop
    children={'para':[], 'blitz':[]}

    for r in range(0,gameInstance.boardSize):
        for c in range(0, gameInstance.boardSize):
            if visitedStates[r][c] == 0:
                children['para'].append((r,c))


    #run blitz

    result=blitzNodes(visitedStates,isMax,gameInstance)

    for key, value in result.items():
        #print(key)
        #print(value)
        children['blitz'].append((key, value))
        #(      piece, [(blitzMove, [flipNode1, flipNode2, ...]),
        #               (blitzMove2, [flipNode1, flipNode2, ...])      ]    )
    return children

def fowardNodeValue(child, gameInstance, nodeType):
    if nodeType=='para':
        return gameInstance.tempBoard2[child[0]][child[1]]
    if nodeType=='blitz':
        blitzMove=child[0]
        #print(child)
        sum=gameInstance.tempBoard2[blitzMove[0]][blitzMove[1]]
        for elem in child[1]:
            sum=sum+gameInstance.tempBoard2[elem[0]][elem[1]]
        return sum


global counter
counter=0
def minimax(gameInstance, node, depth, isMax, visitedStates, totalUtil, maxMin, moveList, expansionType, root):
    #print(maxMin)

    global counter

    visit=deepcopy(visitedStates)
   # print(visit)
    if isMax==False and visit[node[0]][node[1]]==0:
        visit[node[0]][node[1]]='a'
        if expansionType == 'blitz':
            for elem in flippedNodesFromBlitz(visit,node,'a'):
                visit[elem[0]][elem[1]]='a'
    elif isMax==True and visit[node[0]][node[1]]==0:
        visit[node[0]][node[1]]='b'
        if expansionType == 'blitz':
            for elem in flippedNodesFromBlitz(visit,node,'b'):
                visit[elem[0]][elem[1]]='b'

    #print(isMax)
    #print(visit)
    children=getChildren(visit, gameInstance,isMax)

    #print('blitz children',children['blitz'])
    #print(' children',children)
    if len(children['para'])==0 and len(children['blitz'])==0 or depth==0:
        # print('...')
        # print(maxMin)
        # print('...')
        counter=counter +1
        #print(evaluate(maxMin, node, expansionType))
        return evaluate(maxMin, node, expansionType)
    if isMax==True:
        v=(-1000, node, expansionType)
        vp=0
        retNode=node
        #print('max turn')
        for child in children['para']:
            tempPar=maxMin+fowardNodeValue(child, gameInstance, 'para')
            #print(tempPar)
            res= minimax(gameInstance, child,
                                                                depth-1,
                                                                False,
                                                                visit,
                                                                totalUtil,
                                                                tempPar, moveList, 'para',root)
            vp=res

            #print(vp)
            if vp[0] > v[0]:
                if v[1] == root:

                    v=(vp[0], v[1], v[2])
                    moveList[0]=vp[1]
                    moveList[1]=vp[2]
                    #print('move',moveList)
                else:
                    #print('kkk', v[1])
                    v=(vp[0], v[1], v[2])
        for piece in children['blitz']:
            #print(children['blitz'])
            piece2=piece[1]
            for child in piece2:
                tempPar=maxMin+fowardNodeValue(child, gameInstance, 'blitz')
                #print(tempPar)
                res= minimax(gameInstance, child[0],
                            depth-1,
                            False,
                                                                    visit,
                                                                    totalUtil,
                                                                   tempPar, moveList, 'blitz',root)
                #print(vp)
                vp=res

                if vp[0] > v[0]:
                    if v[1] == root:

                        v=(vp[0], v[1], v[2])
                        moveList[0]=vp[1]
                        moveList[1]=vp[2]
                        #print('move',moveList)
                    else:
                        #print('kkk2', v[1])
                        v=(vp[0], v[1], v[2])


        return v
    if isMax==False:
        v=(1000, node, expansionType)
        vp=0
        retNode=node
        #print('min turn')
        for child in children['para']:
            tempPar=maxMin-fowardNodeValue(child, gameInstance, 'para')
            #print(tempPar)
            res= minimax(gameInstance, child,
                        depth-1,
                        True,
                                                                visit,
                                                                totalUtil,
                                                               tempPar, moveList, 'para',root)
            #print(vp)
            vp=res
            #print(vp)

            if vp[0] < v[0]:
                if v[1] == root:

                    v=(vp[0], v[1], v[2])
                    moveList[0]=vp[1]
                    moveList[1]=vp[2]
                    #print('move',moveList)
                else:
                    #print('kkk2', v[1])
                    v=(vp[0], v[1], v[2])

        for piece in children['blitz']:
            #print(children['blitz'])
            piece2=piece[1]
            for child in piece2:
                tempPar=maxMin-fowardNodeValue(child, gameInstance, 'blitz')
                #print(tempPar)
                res= minimax(gameInstance, child[0],
                            depth-1,
                            True,
                                                                    visit,
                                                                    totalUtil,
                                                                   tempPar, moveList, 'blitz',root)
                #print(vp)
                vp=res

                if vp[0] < v[0]:
                    if v[1] == root:

                        v=(vp[0], v[1], v[2])
                        moveList[0]=vp[1]
                        moveList[1]=vp[2]
                        #print('move',moveList)
                    else:
                        #print('kkk2', v[1])
                        v=(vp[0], v[1], v[2])



        #print(v)
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
                board[i][j] = int(board[i][j])
                j+=1
            i+=1

        self.board = board
        self.isFull = False



#playerBlue = Player("blue")
#playerGreen = Player("green")

def zeroInList(gameInstance):
    for item in gameInstance.tempBoard2State:
        if 0 in item:
            return True
    return False


def firstMove(gameInstance, depth):
    playerMove=[(-1,-1), 'ERROR']
    visitReplace=deepcopy(gameInstance.tempBoard2State)
    total=-1000
    first=[(-1,-1)]
    for r in range(0,len(gameInstance.tempBoard2State)):
        for c in range(0, len(gameInstance.tempBoard2State[r])):
            gameInstance.tempBoard2State[r][c]='a'
            result=minimax(gameInstance, (r,c), depth, True, list(gameInstance.tempBoard2State),0,gameInstance.tempBoard2[r][c], playerMove, 'para',(r,c))
            if total < result[0]:
                total=result[0]
                first[0]=playerMove[0]
            gameInstance.tempBoard2State=deepcopy(visitReplace)


    gameInstance.tempBoard2State=deepcopy(visitReplace)
    print('lllllllllllllllllllllllllllllll',first[0])
    return first[0]

    # x=0
    # node=(-1,-1)
    # for r in range(0,len(gameInstance.tempBoard2)):
    #     for c in range(0, len(gameInstance.tempBoard2[r])):
    #         if x < gameInstance.tempBoard2[r][c]:
    #             x= gameInstance.tempBoard2[r][c]
    #             node=(r,c)
    # print('first move:')
    # print(node)
    # return node



def ageOfBlitz():
    depth=3
    gameInstance=GameBoard()
    b = Board('Resources\Sevastopol.txt')

    # tempBoard2=[[1,4],
    #             [3,2]]
    # b.board=deepcopy(tempBoard2)

    gameInstance.tempBoard2=b.board
    gameInstance.boardSize=len(gameInstance.tempBoard2)
    initializeState=[]
    for elem in range(0,gameInstance.boardSize):
        initializeState.append([])
        for elem2 in range(0, gameInstance.boardSize):
            initializeState[elem].append(0)
    gameInstance.tempBoard2State=deepcopy(initializeState)
    printBoard(initializeState)
    print('------------')
    printBoard(gameInstance.tempBoard2)
    print('------------')




    playerMove=[(-1,-1), 'ERROR']
    playerTurn=False

    #determine first move
    node=firstMove(gameInstance, depth)
    #node=(1,0)
    #update gameState
    gameInstance.tempBoard2State[node[0]][node[1]]='a'
    #while(moves are possible)
    while(zeroInList(gameInstance)):
        if playerTurn == True:
            print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
            result=minimax(gameInstance, node, depth, True, list(gameInstance.tempBoard2State),0,gameInstance.tempBoard2[node[0]][node[1]], playerMove, 'para',node)
            node=playerMove[0]
            print('RESULT A')
            print(result)
            gameInstance.tempBoard2State[node[0]][node[1]]='a'
            if playerMove[1] == 'blitz':
                for elem in flippedNodesFromBlitz(gameInstance.tempBoard2State,node,'a'):
                    gameInstance.tempBoard2State[elem[0]][elem[1]]='a'
            playerTurn=False
            printBoard(gameInstance.tempBoard2State)
            #print(result)
        if playerTurn == False:
            print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
            result=minimax(gameInstance, node, depth, False, list(gameInstance.tempBoard2State),0,gameInstance.tempBoard2[node[0]][node[1]], playerMove, 'para',node)
            node=playerMove[0]
            print('RESULT B')
            print(result)
            gameInstance.tempBoard2State[node[0]][node[1]]='b'
            if playerMove[1] == 'blitz':
                for elem in flippedNodesFromBlitz(gameInstance.tempBoard2State,node,'b'):
                    gameInstance.tempBoard2State[elem[0]][elem[1]]='b'
            printBoard(gameInstance.tempBoard2State)
            playerTurn=True
            #print(result)
        #update gameState
    #printboard
    print('------------')
    printBoard(gameInstance.tempBoard2State)
    return 1

def printBoard(board):
    for elem in board:
        print(elem)
# print('----')
# moveList=[(-1,-1)]
# result=minimax((0,0), 5, False, list(GameBoard.tempBoard2State),0,GameBoard.tempBoard2[0][0], moveList)
# print('----')
# print(result)
# print(moveList)
# print(counter)

import timeit




def flippedNodesFromBlitz(boardState, node, player):
    if player=='b': opponent='a'
    else: opponent='b'

    flips=[]
    def positive(one, two):
        if one>=0 and two>=0: return True
        return False

    try:
        if boardState[node[0]-1][node[1]] == opponent and positive(node[0]-1, node[1]):
            flips.append((node[0]-1, node[1]))
    except:
        pass
        #print('up not possible')
    #down
    try:
        if boardState[node[0]+1][node[1]] == opponent and positive(node[0]+1, node[1]):
            flips.append((node[0]+1, node[1]))
    except:
        pass
        #print('down not possible')
    #left
    try:
        if boardState[node[0]][node[1]-1] == opponent and positive(node[0], node[1]-1):
            flips.append((node[0], node[1]-1))
    except:
        pass
        #print('left not possible')
    #right
    try:
        if boardState[node[0]][node[1]+1] == opponent and positive(node[0], node[1]+1):
            flips.append((node[0], node[1]+1))
    except:
        pass
        #print('right not possible')
    return flips


def nextBlitzMoves(boardState, node):
    moves=[]
    #up
    def positive(one, two):
        if one>=0 and two>=0: return True
        return False

    try:
        if boardState[node[0]-1][node[1]] == 0 and positive(node[0]-1, node[1]):
            moves.append((node[0]-1, node[1]))
    except:
        pass
        #print('up not possible')
    #down
    try:
        if boardState[node[0]+1][node[1]] == 0 and positive(node[0]+1, node[1]):
            moves.append((node[0]+1, node[1]))
    except:
        pass
        #print('down not possible')
    #left
    try:
        if boardState[node[0]][node[1]-1] == 0 and positive(node[0], node[1]-1):
            moves.append((node[0], node[1]-1))
    except:
        pass
        #print('left not possible')
    #right
    try:
        if boardState[node[0]][node[1]+1] == 0 and positive(node[0], node[1]+1):
            moves.append((node[0], node[1]+1))
    except:
        pass
        #print('right not possible')
    return moves



def blitzNodes(boardState, isMax,gameInstance):
    if isMax==True: player='a'
    else: player='b'

    blitzStructure=defaultdict(list)
    #printBoard(boardState)
    for r in range(0,gameInstance.boardSize):
        for c in range(0, gameInstance.boardSize):
            # print(r,c, boardState[r][c])
            if boardState[r][c] == player:

                moves=nextBlitzMoves(boardState,(r,c))
                # print(moves)
                if moves:
                    for move in moves:
                        flips=flippedNodesFromBlitz(boardState,move,player)
                        blitzStructure[(r,c)].append(
                            (move, flips)
                        )


    return blitzStructure


def tester():
    a='a'
    b='b'
    tempBoard=[[1,4,5],
               [2,3,6],
               [9,8,7]]

    tempBoardState=[[b,0,b],
                    [0,a,0],
                    [0,0,0]]

    tempBoard2=[[1,4],
                [2,3]]

    tempBoard2State=[[0,a],
                     [b,0]]
    gameInstance=GameBoard()
    gameInstance.boardSize=3
    gameInstance.tempBoard2=deepcopy(tempBoard)
    gameInstance.tempBoard2State=deepcopy(tempBoardState)

    result=blitzNodes(tempBoardState,True,gameInstance)

    print(result)

    val=fowardNodeValue(
        ((1,1),((0,1), [(0,2), (0,0)]))
        , gameInstance, 'blitz')

    print(val)


# tester()

start = timeit.default_timer()
ageOfBlitz()
stop = timeit.default_timer()
print(start-stop)