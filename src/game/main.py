import numpy as np
from controller.CLIController import CLICOntroller
from controller.GUIController import GUIController
from scipy.signal import convolve2d


class Game:
    board = None
    gameOver = False
    turn = 0 #the player who acts (always 0 or 1 for player 1 or 2)
    useGUI = True
    ROW_COUNT, COLUMN_COUNT = 6, 7 #in case we want to make it dynamic, we use some global vars.
    
    if useGUI:
        controller = GUIController()
    else:
        controller = CLICOntroller()
        
    #simply creates an empty matrix for the gamefield
    def create_board(self):
        gameBoard = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        print(gameBoard)
        self.board = gameBoard
        
        return gameBoard
    
    #if this condition is true we will let the use drop piece here.
    #if not true that means the col is not vacant
    def checkValidPosition(self, col):   
        return self.board[5][col]==0
    
    def displayBoard(self):
        # print(np.flip(self.board, 0))
        self.controller.displayBoard(board=self.board)
        
    def dropPiece(self, row, col):
        self.board[row][col] = self.turn + 1 
        
    def nextFreeRow(self, col):
        for r in range(len(self.board)):
            if self.board[r][col] == 0:
                return r 
    
    def checkWin(self):
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]  
        
        boardCopy = self.board.copy()
        
        #transpose board so that all "PLAYER"-Pieces are 1 and everything else 0:
        if self.turn == 1:
            for row in boardCopy:
                row[row == 1] = 0
                row[row == 2] = 1
        else:
            for row in boardCopy:
                row[row == 2] = 0
                
        #print(np.flip(boardCopy, 0))
                
        for kernel in detection_kernels:
            if (convolve2d(boardCopy == 1, kernel, mode="valid") == 4).any():
                return True
        return False
    
    def loop(self):
        if self.useGUI:
            self.controller.init(self.COLUMN_COUNT, self.ROW_COUNT, self.board)
        
        while not self.gameOver:
            #GET SELECTION from the input handler
            selection = self.controller.handleInput(turn=self.turn)
            #GUI returns -1 if there was no input
            if selection == -1:
                continue
            if self.checkValidPosition(selection):
                row = self.nextFreeRow(selection)
                self.dropPiece(row, selection)
            else: 
                continue
            
            #print the board first before checking the win
            self.displayBoard()
            if self.checkWin():
                self.controller.handleWin(self.turn)
                self.gameOver = True 
            
            #TURN OVER
            self.turn = 1 if self.turn == 0 else 0

if __name__ == "__main__":
    game = Game()
    game.create_board()
    game.loop()