import pygame

from viz.steps import COMPARE, DONE, SWAP, WRITE

BACKGROUND = (20, 20, 28)
NORMAL = (120, 130, 150)
YELLOW = (240, 210, 60)
RED = (220, 60, 60)
GREEN = (70, 200, 100)
ORANGE = (240, 140, 50)

KIND_COLORS = {COMPARE: YELLOW, SWAP: RED, WRITE: ORANGE, DONE: GREEN}


class BarsRenderer:
    """Draws a list of numbers as vertical bars."""

    def __init__(self, margin=20):
        self.margin = margin

    def draw(self, surface, step):
        surface.fill(BACKGROUND)
        if step is None or not step.data:
            return

        width, height = surface.get_size()
        data = step.data
        count = len(data)
        biggest = max(max(data), 1)

        area_width = width - 2 * self.margin
        area_height = height - 2 * self.margin
        slot = area_width / count
        bar_width = max(int(slot) - 1, 1)

        highlight = KIND_COLORS.get(step.kind, NORMAL)

        for i, value in enumerate(data):
            bar_height = max(int(area_height * value / biggest), 1)
            x = int(self.margin + i * slot)
            y = height - self.margin - bar_height
            color = highlight if i in step.indices else NORMAL
            pygame.draw.rect(surface, color, (x, y, bar_width, bar_height))
