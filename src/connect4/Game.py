from connect4.BitBoard import Board
from PIL import Image, ImageDraw, ImageFont

from io import BytesIO


font = ImageFont.truetype("arial.ttf", 18)

# Essentially a wrapper for bitboard
class Game:
    def __init__(self):
        self.board = Board()

    def move(self, column):
        if self.board.can_move(column):
            self.board.make_move(column)
            return True
        else:
            return False

    def check_win(self):
        return self.board.is_win()

    def get_turn(self):
        return self.board.get_turn()

    def __repr__(self):
        return self.board.__repr__()

    def __str__(self):
        return self.__repr__()

    def generate_image_board(self, color1="red", color2="black"):
        im = Image.new("RGB", (256, 256), "white")
        draw = ImageDraw.Draw(im)

        diameter = 28
        padding = 6
        margin = 12

        for i in range(7):
            for j in range(6):
                if self.board.get_at(i, 5 - j) == 1:
                    color = color1
                    outline = 'red'
                elif self.board.get_at(i, 5 - j) == -1:
                    color = color2
                    outline = 'black'
                else:
                    color = '#CCC'
                    outline = "#CCC"

                draw.ellipse((margin + (diameter + padding) * i, margin + (diameter + padding) * j,
                              margin + (diameter + padding) * i + diameter,
                              margin + (diameter + padding) * j + diameter), fill=outline,
                             outline=None)
                draw.ellipse((margin + (diameter + padding) * i + 2, margin + (diameter + padding) * j + 2,
                              margin + (diameter + padding) * i + diameter - 2,
                              margin + (diameter + padding) * j + diameter - 2), fill=color,
                             outline=None)

            draw.text((margin + (diameter + padding) * i + 10, 214), str(i), fill="black", font=font)

        return im


if __name__ == "__main__":
    game = Game()

    print(game.board)

    game.move(0)
    game.move(3)
    game.move(1)
    game.move(1)
    game.move(2)
    game.move(2)
    game.move(0)
    game.move(1)
    game.move(0)
    print(game.move(0))

    game.generate_image_board("green").show()

    pass
