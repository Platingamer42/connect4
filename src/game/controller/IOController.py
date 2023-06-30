from abc import ABC, abstractmethod

class IOController(ABC):
    def handleInput(self, turn: int) -> int:
        pass
    
    def reset(self):
        pass
    
    @abstractmethod
    def handle_win(self, turn) -> int:
        return 1
    
    @abstractmethod
    def display_board(self, board):
        pass