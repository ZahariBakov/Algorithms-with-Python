import pygame

from viz.steps import CELL, DONE, PATH

BACKGROUND = (20, 20, 28)
CELL_COLOR = (60, 65, 80)
YELLOW = (240, 210, 60)
BLUE = (80, 150, 240)
GREEN = (70, 200, 100)
TEXT = (235, 235, 240)
DARK_TEXT = (20, 20, 28)


class TableRenderer:
    """Draws a table with the letters of two words on the top and the left."""

    def __init__(self, margin=20):
        self.margin = margin
        self.first = ''
        self.second = ''
        self._font = None
        self._font_size = 0

    def set_words(self, first, second):
        self.first = first
        self.second = second

    def _get_font(self, size):
        if self._font is None or self._font_size != size:
            self._font = pygame.font.Font(None, size)
            self._font_size = size
        return self._font

    def draw(self, surface, step):
        surface.fill(BACKGROUND)
        if step is None or not step.data:
            return

        width, height = surface.get_size()
        table = step.data
        rows = len(table) + 1  # one more for the letters on the top
        cols = len(table[0]) + 1  # one more for the letters on the left

        size = int(min((width - 2 * self.margin) / cols,
                       (height - 2 * self.margin) / rows))
        size = max(size, 4)
        font = self._get_font(max(size * 2 // 3, 8))

        yellow = ()
        blue = ()
        green = ()
        if step.kind == CELL:
            yellow = (step.indices,)
            blue = step.info
        elif step.kind == PATH:
            green = step.info
        elif step.kind == DONE:
            # Show the whole path in the last picture, if there is one.
            green = self._path_of(table)

        left = self.margin
        top = self.margin

        # Letters. Column 0 and row 0 of the grid are for the letters.
        # The first string is on the left, the second one on the top.
        for i, letter in enumerate(self.first):
            self._text(surface, font, letter, left, top + (i + 2) * size, size)
        for j, letter in enumerate(self.second):
            self._text(surface, font, letter, left + (j + 2) * size, top, size)

        for row, cells in enumerate(table):
            for col, value in enumerate(cells):
                if (row, col) in yellow:
                    color = YELLOW
                elif (row, col) in blue:
                    color = BLUE
                elif (row, col) in green:
                    color = GREEN
                else:
                    color = CELL_COLOR
                x = left + (col + 1) * size
                y = top + (row + 1) * size
                pygame.draw.rect(surface, color, (x + 1, y + 1,
                                                  size - 2, size - 2))
                text_color = DARK_TEXT if color != CELL_COLOR else TEXT
                self._text(surface, font, str(value), x, y, size, text_color)

    def _text(self, surface, font, text, x, y, size, color=TEXT):
        image = font.render(text, True, color)
        rect = image.get_rect(center=(x + size // 2, y + size // 2))
        surface.blit(image, rect)

    def _path_of(self, table):
        """The path back, found again from the finished table."""
        row = len(table) - 1
        col = len(table[0]) - 1
        path = [(row, col)]
        while row > 0 and col > 0:
            if self.first[row - 1] == self.second[col - 1]:
                row -= 1
                col -= 1
            elif table[row - 1][col] > table[row][col - 1]:
                row -= 1
            else:
                col -= 1
            path.append((row, col))
        return path
