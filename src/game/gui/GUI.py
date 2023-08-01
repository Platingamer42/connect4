import pygame, sys, math
from gui.GameBoard import GameBoard
import gui.colors as colors
from typing import Self, List
from abc import ABC, abstractmethod
#import pygame_gui
from gui.UI_Elements import UI_Element, Button, Label

class GUI:  
    version = 0.8 #TODO auslagern?
    SQUARESIZE = 100
    COLUMN_COUNT = 0
    ROW_COUNT = 0
    RADIUS = int(SQUARESIZE/2 - 5)

    
    screen = None
    #font = None
    IN_MENU = False
    fonts = {}
    fps_clock = None
    
    ui_elements:List[UI_Element] = []
    fps = 60
    
    game_board = None
        
    def __init__(self, column_count: int, row_count: int, board): 
        pygame.init()
       
        self.COLUMN_COUNT = column_count
        self.ROW_COUNT = row_count
        #define width and height of board
        self.width = column_count * self.SQUARESIZE #700
        self.height = (row_count+1) * self.SQUARESIZE #600
        
        size = (self.width, self.height)
                
        self.screen = pygame.display.set_mode(size)
        
        ##set name:
        pygame.display.set_caption("Connect4 " + str(self.version))
        
        #INIT THE GAMEBOARD
        self.game_board = GameBoard(column_count=self.COLUMN_COUNT, row_count=self.ROW_COUNT)
        
        pygame.display.update()
        
        
        self.fonts = { 
            "font40": pygame.font.SysFont('Arial', 40),
            "font14": pygame.font.SysFont('Arial', 14)
        }
        self.fps_clock = pygame.time.Clock()
        #manager = pygame_gui.UIManager((800, 600))



    def handle_win(self, turn, board) -> int:
        label = Label(40, 10, width=400, height=100, font=self.fonts["font40"], labelText="Player {} wins!!".format(turn+1))
        self.ui_elements.append(label)
        self.process_elements()
        #self.draw_board(board=board) #TODO not sure if still needed.
        pygame.time.wait(3000) 
        return 1 #return code. Todo: Add exit functionality?
    
            
    
    def get_input(self, turn) -> int:
        pygame.event.clear()
        self.fps_clock.tick(self.fps)
        
        for event in pygame.event.get():
            #print(self.fps_clock.get_fps())
            if event.type == pygame.QUIT:
                sys.exit()
    
            #moves the floating piece with the mouse. TODO: Own object?
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, colors.BLACK, (0,0, self.width, self.SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(self.screen, colors.BLUE, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                else: 
                    pygame.draw.circle(self.screen, colors.YELLOW, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
            pygame.display.update()
    
            #clears the screen where the piece was floating earlier (whole row with heiht of SQUARESIZE gets painted black)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, colors.BLACK, (0,0, self.width, self.SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/self.SQUARESIZE))

                    return col
    
                # # Ask for Player 2 Input
                else:               
                    posx = event.pos[0]
                    col = int(math.floor(posx/self.SQUARESIZE))
                    return col
        return -1
    
    def draw_board(self, board):
        self.screen.fill(colors.BLACK) #TODO: Bad pratice since this leads to unneccessary reloads
        self.game_board.draw_board(board=board)
        self.screen.blit(self.game_board.board_surface, (0, 0))
        pygame.display.update()
            
    
    ### function to draw the menu:
    def draw_menu(self, stats):
        self.screen.fill(colors.BLACK)
        pygame.display.flip()

        button1 = Button(30, 140, 400, 100, fonts=self.fonts, buttonText='START',onclickFunction=self.start_pressed).with_colors("#AABBCC", "#A3DE33", "#001100")
        button2 = Button(30, 270, 400, 100, fonts=self.fonts, buttonText='2-Player', onclickFunction=self.start_pressed, onePress=True)
        
        #LABELS:                
        label = Label(x=540, y=140, width=100, height=30, font=self.fonts["font14"], labelText="STATISTIK")
        label2 = Label(x=540, y=170, width=100, height=30, font=self.fonts["font14"], labelText="times played: {}".format(stats["times_played"]))
        label3 = Label(x=540, y=200, width=100, height=30, font=self.fonts["font14"], labelText="P1 won: {}".format(stats["wins"]["player_one"]))        
        label4 = Label(x=540, y=230, width=100, height=30, font=self.fonts["font14"], labelText="P2 won: {}".format(stats["wins"]["player_two"]))        

        self.ui_elements.extend((button1, button2, label, label2, label3, label4))
        
        
        self.process_elements()
                    
    def display_elements(self):
        """updates every element in ui_elements if it's toUpdate value is true
        """
        for element in self.ui_elements:
            if element.toUpdate:
                self.screen.blit(element.elementSurface, element.elementRect)
                pygame.display.update(element.elementRect)
                element.toUpdate = False
                
    def process_elements(self):
        for element in self.ui_elements:
            element.process()
        self.display_elements()


    def enter_menu(self, stats):
        self.IN_MENU = True
        self.draw_menu(stats)

        while self.IN_MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.process_elements()
            self.fps_clock.tick(self.fps)
        
    def exit_menu(self):
        self.IN_MENU = False
        self.screen.fill(colors.BLACK)
        self.ui_elements.clear()
        
        #TEST?
        self.screen.blit(self.game_board.board_surface, (0, 0))
        pygame.display.update()
        
        #pygame.display.update()
        
    def start_pressed(self) -> bool:
        self.exit_menu()
        return True
    
