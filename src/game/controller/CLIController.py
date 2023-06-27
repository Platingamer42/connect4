from controller.IOController import IOController
from numpy import flip

class CLICOntroller(IOController):
    def handleInput(self, turn: int):
        super().handleInput(turn=turn)
        inp = -1 #so that the loop runs once
        
        while inp > 6 or inp < 0:
            inp = input("Spieler {}: ".format(turn))
            if not inp.isdigit():
                print("Please insert a number from 0 to 6")
                inp = -1
            else:
                inp = int(inp)              
        return inp
    
    def displayBoard(self, board):
        print(flip(board, 0))
    
    def handleWin(self, turn):
        print("Spieler {} gewinnt!".format(self.turn + 1))

