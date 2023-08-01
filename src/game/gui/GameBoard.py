import gui.colors as colors
import pygame

class GameBoard:        
    #define our screen size
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)
    width, height = (0, 0) 
    board_surface = None
    dropped_pieces = [] #Circles that are already dropped
    cells = [] #the (rect-circle)-pairs for every cell
    
    def __init__(self, column_count: int, row_count: int):
        self.width = column_count * self.SQUARESIZE #700
        self.height = (row_count+1) * self.SQUARESIZE #600
        self.COLUMN_COUNT = column_count
        self.ROW_COUNT = row_count
        self.init_board()

        
    def init_board(self):
        self.board_surface = pygame.Surface((self.width, self.height))
        self.cells = self.generate_empty_fields()
    
    def generate_empty_fields(self) -> list:
        """_summary_
        Returns:
            list: containing the cells as (cell, circle)
        """
        cells = []
        
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                #red cell:
                cell =  pygame.draw.rect(surface=self.board_surface, color=colors.RED, rect=(c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                
                #black circle in red cell:
                circle = pygame.draw.circle(surface=self.board_surface, color=colors.BLACK, center=(int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), radius=self.RADIUS)
                
                cells.append((cell, circle))
                
        return cells        
        

    def draw_board(self, board):  
        """function to draw the board

        Args:
            board (_type_): the gameboard to be drawn onto the board surface
        """
        self.dropped_pieces = self.fill_board(board=board)
        
        
    def fill_board(self, board) -> list:
        """similar to generate_empty_fields, loads the board into an
        list containing the pieces that are dropped

        Args:
            board (_type_): _description_

        Returns:
            list: containing pygame-Circles
        """
        
        pieces = []
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):      
                if board[r][c] == 1:
                    #print blue circle 
                    pieces.append(pygame.draw.circle(self.board_surface, colors.BLUE, \
                        (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS))
                elif board[r][c] == 2: 
                    #print yellow circle
                    pieces.append(pygame.draw.circle(self.board_surface, colors.YELLOW, \
                        (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS))       
        return pieces