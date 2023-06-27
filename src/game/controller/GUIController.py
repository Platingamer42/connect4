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
        self.displayBoard(self.board)
        
    def handleInput(self, turn: int) -> int:
        inp = self.gui.getInput(turn=turn)
        return inp
    
    def displayBoard(self, board):
        self.gui.draw_board(board)
        
    def handleWin(self, turn):
        self.gui.handleWin(turn, self.board)

