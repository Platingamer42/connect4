import math
import random
from GameWrapper import Functions

class AI(Functions):
    difficulty = 10
    
    def get_next_move(self, board):
        if random.randint(0, 10) > self.difficulty:
            return random.randint(0, self.COLUMN_COUNT-1)
        else:
            col, _ = self.getBest(board)
        return col
    
    def getBest(self, board) -> int:
        col, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)
        #if self.check_valid_location(board, col):
        #    row = self.get_next_open_row(board, col)
        #    self.drop_piece(board, row, col, self.AI_PIECE)
        return col, minimax_score

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self, board, piece):
        score = 0

        ## Score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT//2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        ## Score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(self.COLUMN_COUNT-3):
                window = row_array[c:c+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(self.ROW_COUNT-3):
                window = col_array[r:r+self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        ## Score posiive sloped diagonal
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score
    
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r

    def minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = self.get_validation_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_win(board, self.AI):
                    return (None, math.inf)
                elif self.check_win(board, self.PLAYER):
                    return (None, -math.inf)
                else: # Game is over, no more valid moves
                    return (None, 0)
            else: # Depth is zero
                return (None, self.score_position(board, self.AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: # Minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board, col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_validation_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.check_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations
    
    def drop_piece(self, board, row, col, piece):
	    board[row][col] = piece

