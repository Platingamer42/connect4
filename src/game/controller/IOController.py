from abc import ABC, abstractmethod
class IOController:
    def init(self):
        pass
    
    def handleInput(self, turn: int) -> int:
        pass
    
    @abstractmethod
    def handleWin(self, turn):
        pass
    
    @abstractmethod
    def displayBoard(self, board):
        pass