import numpy as np
from controller.CLIController import CLICOntroller
from controller.GUIController import GUIController
import Ai
from GameWrapper import Functions


class Main(Functions):
    board = None
    GAME_OVER = False
    turn = 0 #the player who acts (always 0 or 1 for player 1 or 2)
    useGUI = True
    useAI = True
    ROW_COUNT, COLUMN_COUNT = 6, 7 #in case we want to make it dynamic, we use some global vars.
    controller = None
        
    def __init__(self) -> None:    
        if self.useGUI:
            self.controller = GUIController()
        else:
            self.controller = CLICOntroller()
        self.ai = Ai.AI()
        
        self.create_board()
        self.loop()
        
        
    #simply creates an empty matrix for the gamefield
    def create_board(self):
        gameBoard = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        print(gameBoard)
        self.board = gameBoard
        
        return gameBoard
    
    def display_board(self):
        # print(np.flip(self.board, 0))
        self.controller.display_board(board=self.board)
    
    def loop(self):
        if self.useGUI:
            self.controller.init(self.COLUMN_COUNT, self.ROW_COUNT, self.board)
            
        #TODO wait for menu input from GUI
        
        while not self.GAME_OVER:
            if self.useAI and self.turn == 1:
                selection, score = self.ai.getBest(self.board.copy())
            else:
                #GET SELECTION from the input handler
                selection = self.controller.handleInput(turn=self.turn)
            
            #GUI returns -1 if there was no input
            if selection == -1:
                continue
            if self.check_valid_location(self.board, selection):
                row = self.next_free_row(self.board, selection)
                self.drop_piece(self.board, row, selection, self.turn+1)
            else: 
                continue
            
            #print the board first before checking the win
            self.display_board()
            if self.is_terminal_node(self.board):
                self.controller.handle_win(self.turn)
                self.GAME_OVER = True 
            
            #TURN OVER
            self.turn = 1 if self.turn == 0 else 0

if __name__ == "__main__":
    game = Main()
    