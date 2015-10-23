from random import randint


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


b = Board('C:\\Users\\Anne\\PycharmProjects\\CSPGames\\Resources\\Sevastopol.txt')
playerBlue = Player("blue")
playerGreen = Player("green")

