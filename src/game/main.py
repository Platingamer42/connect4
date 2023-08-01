import numpy as np
from controller.CLIController import CLICOntroller
from controller.GUIController import GUIController
import Ai
from GameWrapper import Functions
import json
import os
from random import randint

class Main(Functions):
    board = None
    GAME_OVER = False
    turn = 0 #the player who acts (always 0 or 1 for player 1 or 2)
    useGUI = True
    useAI = True
    ROW_COUNT, COLUMN_COUNT = 6, 7 #in case we want to make it dynamic, we use some global vars.
    controller = None

    logging = False #Set to true => Print the board. See GUIController.
    stats = {}
        
    def __init__(self) -> None:   
        #path = os.getcwd() 
        if self.useGUI:
            self.controller = GUIController()
        else:
            self.controller = CLICOntroller()
        self.ai = Ai.AI()
        
        self.create_board()
        while self.loop():
            self.restart_game()
        
        #game closes -> save file
        self.save_stats_to_file()
        
        
    #simply creates an empty matrix for the gamefield
    def create_board(self):
        gameBoard = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))
        self.board = gameBoard
            
    def display_board(self):
        # print(np.flip(self.board, 0))
        self.controller.display_board(board=self.board)
    
    #saves locally
    def save_winner(self):
        self.stats["times_played"] += 1
        if self.turn == 0:
            self.stats["wins"]["player_one"] += 1
        else:
            self.stats["wins"]["player_two"] += 1
        
    #saves the stats to file
    def save_stats_to_file(self):
        with  open(r'src\game\data\stats.json', 'w') as json_file:
            json.dump(self.stats, json_file)
    def load_stats_from_file(self):
        with open(r'src\game\data\stats.json', 'r') as f:
            self.stats = json.load(f)
            
    def restart_game(self):
        self.GAME_OVER = False
        self.create_board() #resets the board
        self.set_starting_player()
        self.controller.reset(self.stats)

    
    def set_starting_player(self):
        """Randomly picks the starting player by choosing 0 or 1
        """
        self.turn = randint(0, 1)
    
    #starts the game_loop
    def loop(self) -> int:
        self.set_starting_player()
        self.load_stats_from_file()

        
        if self.useGUI:
            self.controller.init(self.COLUMN_COUNT, self.ROW_COUNT, self.board, logging=self.logging)
            self.controller.display_menu(self.stats)
        
        while not self.GAME_OVER:
            if self.useAI and self.turn == 1:
                selection = self.ai.get_next_move(self.board.copy())
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
                self.GAME_OVER = True
                self.save_winner()
                if self.controller.handle_win(self.turn):
                    return 1
            #TURN OVER
            self.turn = 1 if self.turn == 0 else 0
        return 0
        

if __name__ == "__main__":
    game = Main()
    