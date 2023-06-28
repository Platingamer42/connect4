from controller.IOController import IOController
from numpy import flip
from gui.GUI import GUI
from gui.colors import RED

class GUIController(IOController):
    gui = None
    board = None
    def init(self, column_count: int, row_count: int, board):
        super().init()
        self.gui = GUI(column_count=column_count, row_count=row_count, board=board)
        self.board = board
        self.display_board(self.board)
        
    def handleInput(self, turn: int) -> int:
        inp = self.gui.get_input(turn=turn)
        return inp
    
    def display_menu(self, board):
        self.gui.draw_menu(board)
    
    def display_board(self, board):
        self.gui.draw_board(board)
        
    def handle_win(self, turn):
        self.gui.handleWin(turn, self.board)

