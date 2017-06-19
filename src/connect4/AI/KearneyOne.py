from connect4.BitBoard import Board


class KearneyOneAI():
    def __init__(self):
        pass

    @staticmethod
    def get_move(board):
        return KearneyOneAI.nega_max(5, board)[1]

    @staticmethod
    def nega_max(depth, board: Board):
        best = float("-inf")
        move = 3

        if board.is_win():  # Someone won
            return float("-inf"), 0
        if board.is_full():  # No moves left to make
            return 0, 0

        if depth == 0:  # Done searching
            return 0, 0

        for i in range(7):
            if board.can_move(i):
                board.make_move(i)
                score = -KearneyOneAI.nega_max(depth - 1, board)[0]
                board.undo_move()
            else:
                score = float("-inf")

            if best < score:
                best = score
                move = i

        return best, move
