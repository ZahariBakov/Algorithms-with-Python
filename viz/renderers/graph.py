import pygame

from viz.steps import DONE, FOUND, VISIT

BACKGROUND = (20, 20, 28)
EDGE = (90, 95, 110)
NODE = (60, 65, 80)
YELLOW = (240, 210, 60)
BLUE = (80, 150, 240)
GREEN = (70, 200, 100)
TEXT = (235, 235, 240)
DARK_TEXT = (20, 20, 28)
SIDE_WIDTH = 200


class GraphRenderer:
    """Draws a graph: lines for edges, circles for nodes, the queue as text."""

    def __init__(self, margin=40):
        self.margin = margin
        self.graph = {}
        self.positions = {}
        self._font = None

    def set_graph(self, graph, positions):
        self.graph = graph
        self.positions = positions

    def _get_font(self):
        if self._font is None:
            self._font = pygame.font.Font(None, 28)
        return self._font

    def _point(self, node, area):
        x, y = self.positions[node]
        left, top, width, height = area
        return int(left + x * width), int(top + y * height)

    def draw(self, surface, step):
        surface.fill(BACKGROUND)
        if step is None or not self.graph:
            return
        font = self._get_font()
        width, height = surface.get_size()
        area = (self.margin, self.margin,
                width - SIDE_WIDTH - 2 * self.margin, height - 2 * self.margin)

        visited = step.data
        queue = step.info if step.kind in (VISIT, FOUND) else []
        # The current node is the last visited one, also while its
        # neighbors are put in the queue.
        current = visited[-1] if step.kind in (VISIT, FOUND) else None

        for node, neighbors in self.graph.items():
            for other in neighbors:
                if node < other:
                    pygame.draw.line(surface, EDGE, self._point(node, area),
                                     self._point(other, area), 2)

        for node in self.graph:
            if node == current:
                color = YELLOW
            elif node in queue:
                color = BLUE
            elif node in visited:
                color = GREEN
            else:
                color = NODE
            center = self._point(node, area)
            pygame.draw.circle(surface, color, center, 20)
            image = font.render(str(node), True,
                                TEXT if color == NODE else DARK_TEXT)
            surface.blit(image, image.get_rect(center=center))

        # The queue and the order, as text at the side.
        x = width - SIDE_WIDTH + 10
        lines = ['Queue:', ' '.join(str(n) for n in queue) or '-', '',
                 'Order:', ' '.join(str(n) for n in visited) or '-']
        if step.kind == DONE:
            lines[0] = 'Queue: (empty)'
        for i, line in enumerate(lines):
            surface.blit(font.render(line, True, TEXT),
                         (x, self.margin + i * 28))
