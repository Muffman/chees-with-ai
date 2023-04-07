import pygame
from pieces import Pawn, Knight, Bishop, Rook, Queen, King

pygame.init()


class Board:
    piece_points = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K':0}

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.sq_size = 64
        self.board = [['' for _ in range(cols)]for _ in range(rows)]

    def draw(self, win):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r+c) % 2 == 0:
                    pygame.draw.rect(
                        win, 'white', (c*self.sq_size, r*self.sq_size, self.sq_size, self.sq_size))
                else:
                    pygame.draw.rect(
                        win, 'gray', (c*self.sq_size, r*self.sq_size, self.sq_size, self.sq_size))

    def place_pieces(self):
        # white pawns
        self.board[6][0] = Pawn(6, 0, 'w')
        self.board[6][1] = Pawn(6, 1, 'w')
        self.board[6][2] = Pawn(6, 2, 'w')
        self.board[6][3] = Pawn(6, 3, 'w')
        self.board[6][4] = Pawn(6, 4, 'w')
        self.board[6][5] = Pawn(6, 5, 'w')
        self.board[6][6] = Pawn(6, 6, 'w')
        self.board[6][7] = Pawn(6, 7, 'w')

        # white Knight
        self.board[7][1] = Knight(7, 1, 'w')
        self.board[7][6] = Knight(7, 6, 'w')

        # white Bishops
        self.board[7][2] = Bishop(7, 2, 'w')
        self.board[7][5] = Bishop(7, 5, 'w')

        # white Rooks
        self.board[7][0] = Rook(7, 0, 'w')
        self.board[7][7] = Rook(7, 7, 'w')

        # white Queen
        self.board[7][3] = Queen(7, 3, 'w')

        # white King
        self.board[7][4] = King(7, 4, 'w')

        # black pawns
        self.board[1][0] = Pawn(1, 0, 'b')
        self.board[1][1] = Pawn(1, 1, 'b')
        self.board[1][2] = Pawn(1, 2, 'b')
        self.board[1][3] = Pawn(1, 3, 'b')
        self.board[1][4] = Pawn(1, 4, 'b')
        self.board[1][5] = Pawn(1, 5, 'b')
        self.board[1][6] = Pawn(1, 6, 'b')
        self.board[1][7] = Pawn(1, 7, 'b')

        # black Knight
        self.board[0][1] = Knight(0, 1, 'b')
        self.board[0][6] = Knight(0, 6, 'b')

        # black Bishops
        self.board[0][2] = Bishop(0, 2, 'b')
        self.board[0][5] = Bishop(0, 5, 'b')

        # black Rooks
        self.board[0][0] = Rook(0, 0, 'b')
        self.board[0][7] = Rook(0, 7, 'b')

        # black Queen
        self.board[0][3] = Queen(0, 3, 'b')

        # black King
        self.board[0][4] = King(0, 4, 'b')

    def draw_pieces(self, win):
        for r, row in enumerate(self.board):
            for c, piece in enumerate(row):
                if piece == '':
                    continue
                piece.draw(win, self.board[r][c].img, self.sq_size)

    def find_king(self, color, board):
        name = color + 'K'
        for r, row in enumerate(board):
            for c, piece in enumerate(row):
                if piece == '':
                    continue
                if piece.name == name:
                    return (r, c)

    def find_all_pieces(self, color, board):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != '' and piece.color == color:
                    pieces.append(piece)
        return pieces

    def find_material_point(self, color):
        points = 0
        pieces = self.find_all_pieces(color)
        for piece in pieces:
            points += self.piece_points[piece.name[1]]

    def evaluate_material(self, color):
        opp_color = 'w' if color == 'b' else 'b'
        return self.find_material_point(color) - self.find_material_point(opp_color)

    def evaluate_space_control(self, color):
        pieces = self.find_all_pieces(color)
        moves = []
        for piece in pieces:
            moves.extend(piece.valid_locations(self.board))
        return len(moves)

    def evaluate_king_safety(self, color):
        score = 0
        row, col = self.find_king(color, self.board)
        all_moves = [(row, col-1),
                     (row, col+1),
                     (row-1, col),
                     (row+1, col),
                     (row+1, col+1),
                     (row-1, col-1),
                     (row+1, col-1),
                     (row-1, col+1)]
        for r, c in all_moves:
            if r not in range(len(self.board)) or c not in range(len(self.board[0])):
                continue
            if self.board[r][c] == '':
                score -= 1
            elif self.board[r][c].color != color:
                score -= 5
            elif self.board[r][c].color == color:
                score += 3
        return score

    def evaluate(self, color):
        material = self.evaluate_material(color)
        space = self.evaluate_space_control(color)
        king_safety = self.evaluate_king_safety(color)

        return material + space + king_safety
