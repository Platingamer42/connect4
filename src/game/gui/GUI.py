import pygame, sys, math
from gui.colors import RED, YELLOW, BLACK, BLUE

class GUI:
    #define our screen size
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)
    width, height = 0, 0
    
    COLUMN_COUNT = 0
    ROW_COUNT = 0
    screen = None
    myFont = None
        
    def __init__(self, column_count: int, row_count: int, board):        
        pygame.init()

        self.COLUMN_COUNT = column_count
        self.ROW_COUNT = row_count
        #define width and height of board
        self.width = column_count * self.SQUARESIZE
        self.height = (row_count+1) * self.SQUARESIZE
        
        size = (self.width, self.height)
                
        self.screen = pygame.display.set_mode(size)
        self.myFont = pygame.font.SysFont("monospace", 75)

    def handleWin(self, turn, board):
        label = self.myFont.render("Player {} wins!!".format(turn+1), 1, RED)
        self.screen.blit(label, (40,10))
        self.draw_board(board=board)
        pygame.time.wait(3000)
    
    
    def getInput(self, turn) -> int:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, self.SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(self.screen, BLUE, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                else: 
                    pygame.draw.circle(self.screen, YELLOW, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(self.screen, BLACK, (0,0, self.width, self.SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/self.SQUARESIZE))

                    return col
                    # if is_valid_location(self.board, col):
                    #     row = get_next_open_row(board, col)
                    #     drop_piece(board, row, col, 1)
    
                    #     if winning_move(board, 1):
                    #         label = myfont.render("Player 1 wins!!", 1, RED)
                    #         screen.blit(label, (40,10))
                    #         game_over = True
    
    
                # # Ask for Player 2 Input
                else:               
                    posx = event.pos[0]
                    col = int(math.floor(posx/self.SQUARESIZE))
                    return col
                    # if is_valid_location(board, col):
                    #     row = get_next_open_row(board, col)
                    #     drop_piece(board, row, col, 2)
    
                    #     if winning_move(board, 2):
                    #         label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    #         screen.blit(label, (40,10))
                    #         game_over = True
    
                # print_board(board)
                # draw_board(board)
    
                # turn += 1
                # turn = turn % 2
        return -1
        
    ### function to draw the board
    def draw_board(self, board):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(self.screen, RED, (c*self.SQUARESIZE, r*self.SQUARESIZE+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):      
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, BLUE, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                elif board[r][c] == 2: 
                    pygame.draw.circle(self.screen, YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int(r*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
        pygame.display.update()
 