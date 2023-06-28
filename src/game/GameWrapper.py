from abc import ABC, abstractmethod
import numpy as np
from scipy.signal import convolve2d


class Functions:
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    PLAYER = 0
    AI = 1

    EMPTY = 0
    PLAYER_PIECE = 1
    AI_PIECE = 2

    WINDOW_LENGTH = 4
    
    def next_free_row(self, board, col):
        for r in range(len(board)):
            if board[r][col] == 0:
                return r 
    
    def drop_piece(self, board, row, col, turn):
        board[row][col] = turn
        
    #if this condition is true we will let the use drop piece here.
    #if not true that means the col is not vacant
    def check_valid_location(self, board, col):
        return board[self.ROW_COUNT-1][col] == 0
    
    def check_win(self, board, turn):
        horizontal_kernel = np.array([[ 1, 1, 1, 1]])
        vertical_kernel = np.transpose(horizontal_kernel)
        diag1_kernel = np.eye(4, dtype=np.uint8)
        diag2_kernel = np.fliplr(diag1_kernel)
        detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]  
        
        boardCopy = board.copy()
                
        #transpose board so that all "PLAYER"-Pieces are 1 and everything else 0:
        if turn == 1: #player 2
            for row in boardCopy:
                row[row == 1] = 0
                row[row == 2] = 1
        else: #player 1
            for row in boardCopy:
                row[row == 2] = 0
                
        #print(np.flip(boardCopy, 0))
                
        for kernel in detection_kernels:
            if (convolve2d(boardCopy == 1, kernel, mode="valid") == 4).any():
                return True
        return False
    
    def get_validation_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.check_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations
    
    def is_terminal_node(self, board):
        return self.check_win(board=board, turn=self.AI)  or self.check_win(board=board, turn=self.PLAYER) or len(self.get_validation_locations(board)) == 0
