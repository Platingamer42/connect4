from controller.IOController import IOController
from numpy import flip
from gui.GUI import GUI
from gui.colors import RED

class GUIController(IOController):
    gui = None
    board = None
    logging = False
    
    def init(self, column_count: int, row_count: int, board, logging = False):
        self.logging = logging        
        self.gui = GUI(column_count=column_count, row_count=row_count, board=board)
        self.board = board
        self.display_board(self.board)
        
    def handleInput(self, turn: int) -> int:
        inp = self.gui.get_input(turn=turn)
        return inp
    
    def display_menu(self, stats):
        self.gui.enter_menu(stats)
    
    def display_board(self, board):
        self.gui.draw_board(board)
        if self.logging: 
            print("###########################")
            print(flip(board, 0))
            print("###########################")
        
    def reset(self, stats):
        self.display_menu(stats)
        
    def handle_win(self, turn):
        return self.gui.handle_win(turn, self.board)
        

