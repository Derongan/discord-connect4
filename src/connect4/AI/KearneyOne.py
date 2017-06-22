from connect4.BitBoard import Board
import numpy as np
import cProfile


class Score:
    BEST = 10000
    WORST = -BEST
    IMPOSSIBLE = -BEST - 1


class KearneyOneAI():
    def __init__(self):
        pass

    @staticmethod
    def get_move(board, strength=6):
        for i in range(7):
            if board.can_move(i):
                old_move = i

        for i in range(strength):
            score, move = KearneyOneAI.nega_max_ab(strength + 1, board)

            if score == Score.WORST:
                return old_move

            old_move = move
        return move

    @staticmethod
    def nega_max_ab(depth, board: Board, a=Score.WORST, b=Score.BEST):
        """
        Finds the best move
        :param depth:
        :param board:
        :param a:
        :param b:
        :return: A tuple where the first element is the score and the second is the (best) move with that score
        """
        move = 3
        best = Score.WORST

        if depth == 0:
            player = board.get_turn()

            # We are evaluating from the viewpoint of player "0"
            if player == 0:
                return KearneyOneAI.evaluate(board), move
            else:
                return -KearneyOneAI.evaluate(board), move

        # Other player has already won
        if board.is_win():
            return Score.WORST, move

        for i in range(7):
            if board.can_move(i):
                board.make_move(i)
                score = -KearneyOneAI.nega_max_ab(depth - 1, board, -b, -a)[0]
                board.undo_move()
            else:
                score = Score.IMPOSSIBLE

            if score > best:
                best = score
                move = i

            a = max(a, score)

            if a >= b:
                break

        return best, move

    @staticmethod
    def evaluate(board: Board):
        return KearneyOneAI.bitvaluate(board)

    @staticmethod
    def bitvaluate(board: Board):
        b1 = board.bitboard[0]
        b2 = board.bitboard[1]

        ret = 0

        for wingrp in KearneyOneAI.WIN_GROUPS:
            b1_res = b1 & wingrp
            b2_res = b2 & wingrp

            if not b1_res:
                ret -= b2_res
            if not b2_res:
                ret += b1_res

        return ret



    WIN_GROUPS = np.array([
        15,
        1920,
        245760,
        31457280,
        4026531840,
        515396075520,
        65970697666560,
        30,
        3840,
        491520,
        62914560,
        8053063680,
        1030792151040,
        131941395333120,
        60,
        7680,
        983040,
        125829120,
        16106127360,
        2061584302080,
        263882790666240,
        2113665, 270549120,
        34630287360,
        4432676782080,
        4227330,
        541098240,
        69260574720,
        8865353564160,
        8454660,
        1082196480,
        138521149440,
        17730707128320,
        16909320,
        2164392960,
        277042298880,
        35461414256640,
        33818640,
        4328785920,
        554084597760,
        70922828513280,
        67637280,
        8657571840,
        1108169195520,
        141845657026560,
        16843009,
        2155905152,
        275955859456,
        35322350010368,
        33686018,
        4311810304,
        551911718912,
        70644700020736,
        67372036,
        8623620608,
        1103823437824,
        141289400041472,
        2130440,
        272696320,
        34905128960,
        4467856506880,
        4260880,
        545392640,
        69810257920,
        8935713013760,
        8521760,
        1090785280,
        139620515840,
        17871426027520
    ], dtype="int64")


def test():
    ai = KearneyOneAI()
    b = Board()
    b.make_move(3)
    b.make_move(0)
    b.make_move(3)
    b.make_move(0)
    b.make_move(3)
    print(ai.get_move(b))


if __name__ == "__main__":
    test()
    # cProfile.run('test()')
