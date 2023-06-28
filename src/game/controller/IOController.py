from abc import ABC, abstractmethod
class IOController:
    def init(self):
        pass
    
    def handleInput(self, turn: int) -> int:
        pass
    
    @abstractmethod
    def handle_win(self, turn):
        pass
    
    @abstractmethod
    def display_board(self, board):
        pass