import numpy as np
import copy

ONE = np.int64(1)

# Most functions Modified from https://github.com/denkspuren/BitboardC4/blob/master/BitboardDesign.md
class Board:
    def __init__(self):
        self.bitboard = np.zeros(2, dtype="int64")  # Two bitboards one for each player
        self.height = np.array([0, 7, 14, 21, 28, 35, 42], dtype="int64")  # Speed things up by saving height
        self.moves = np.zeros(7 * 6, dtype="int32")  # remember the order of moves so we can undo them

        self.counter = np.int64(0)  # Stores both whos turn it is and the current position in history

    def get_turn(self):
        return self.counter & 1

    def get_at(self, x, y):
        return ((self.bitboard[0] >> (7 * x + y)) & 1) - ((self.bitboard[1] >> (7 * x + y)) & 1)

    def make_move(self, col):
        # move = np.left_shift(1, self.height[col])
        move = 1 << self.height[col]
        self.height[col] += 1
        self.bitboard[self.counter & 1] ^= move
        self.moves[self.counter] = col
        self.counter += 1

    def undo_move(self):
        col = self.moves[self.counter - 1]
        self.counter -= 1
        move = 1 << (self.height[col] - 1)
        self.height[col] -= 1
        self.bitboard[self.counter & 1] ^= move

    def is_win(self):
        b = self.bitboard[(self.counter + 1) & 1]

        y = b & (b >> 6)
        if y & (y >> 2 * 6) != 0:  # Diag
            return True

        y = b & (b >> 7)  # Horiz
        if y & (y >> 2 * 7) != 0:
            return True

        y = b & (b >> 8)  # Diag 2
        if y & (y >> 2 * 8) != 0:
            return True

        y = b & (b >> 1)
        if y & (y >> 2) != 0:  # Vert
            return True

        return False

    def can_move(self, col):
        return self.height[col] < col * 7 + 6

    def is_full(self):
        return self.counter >= 42

    def __str__(self):
        res = ""
        for i in range(6):
            for j in range(7):
                v = self.get_at(j, 5 - i)
                if v > 0:
                    res += "X "
                elif v < 0:
                    res += "O "
                else:
                    res += "_ "
            res += "\n"

        return res

    def __copy__(self):
        b2 = Board()

        b2.height = np.copy(self.height)
        b2.moves = np.copy(self.moves)
        b2.bitboard = np.copy(self.bitboard)
        b2.counter = np.copy(self.counter)

        return b2


if __name__ == "__main__":
    x = Board()
    x.make_move(0)

    print(x)

    z = copy.copy(x)

    print(z)