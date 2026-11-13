import random

import pygame

from viz.algorithms.sorting import (
    bubble_sort,
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    selection_sort,
)
from viz.algorithms.searching import binary_search
from viz.algorithms.dp import edit_distance, lcs, move_down_right
from viz.algorithms.graphs import SAMPLE_GRAPH, SAMPLE_POSITIONS, bfs, dfs
from viz.renderers.bars import BarsRenderer
from viz.renderers.graph import GraphRenderer
from viz.renderers.table import TableRenderer
from viz.steps import COMPARE, DONE, NOT_FOUND, SWAP, WRITE, Step

WINDOW_SIZE = (900, 500)
ITEM_COUNT = 40
FPS = 60

ALGORITHMS = {
    pygame.K_1: ('Bubble sort', bubble_sort),
    pygame.K_2: ('Selection sort', selection_sort),
    pygame.K_3: ('Insertion sort', insertion_sort),
    pygame.K_4: ('Merge sort', merge_sort),
    pygame.K_5: ('Quick sort', quick_sort),
    pygame.K_6: ('Heap sort', heap_sort),
}

# The number keys on the right of the keyboard (the numpad) have other key codes.
# They choose the same algorithms as the number keys above the letters.
NUMPAD = {
    pygame.K_KP1: pygame.K_1,
    pygame.K_KP2: pygame.K_2,
    pygame.K_KP3: pygame.K_3,
    pygame.K_KP4: pygame.K_4,
    pygame.K_KP5: pygame.K_5,
    pygame.K_KP6: pygame.K_6,
    pygame.K_KP7: pygame.K_7,
    pygame.K_KP8: pygame.K_8,
    pygame.K_KP9: pygame.K_9,
    pygame.K_KP0: pygame.K_0,
}

# Key 7 is binary search. It is not in ALGORITHMS because it needs
# sorted data and a target.
SEARCH_KEY = pygame.K_7
MISSING_CHANCE = 0.3

# Key 8 is the longest common subsequence (LCS), drawn as a table.
LCS_KEY = pygame.K_8
# Key 9 is the edit distance (all costs are 1), also a table with two words.
EDIT_KEY = pygame.K_9
# Key 0 is move down right: the best sum in a small grid of numbers.
GRID_KEY = pygame.K_0
GRID_SIZE = (4, 6)  # rows, columns
TABLE_KEYS = {
    LCS_KEY: ('LCS', lcs),
    EDIT_KEY: ('Edit distance', edit_distance),
}
# Key B is breadth first search (BFS) and key D is depth first search (DFS)
# on a small graph.
GRAPH_KEY = pygame.K_b
DFS_KEY = pygame.K_d
GRAPH_ALGORITHMS = {
    GRAPH_KEY: ('BFS', bfs, 'Queue'),
    DFS_KEY: ('DFS', dfs, 'Stack'),
}
WORDS = [
    'algorithm', 'python', 'computer', 'keyboard', 'monitor', 'program',
    'variable', 'function', 'network', 'pointer', 'compiler', 'database',
    'subsequence', 'sequence', 'iteration', 'recursion',
]

# Steps per second. Up goes to the next value, Down to the previous one.
SPEEDS = [2, 5, 10, 20, 40, 80, 160, 320, 640]


def new_data():
    return random.sample(range(1, ITEM_COUNT + 1), ITEM_COUNT)


def new_target(values):
    """A random value from the list, or sometimes one that is not in it."""
    if random.random() < MISSING_CHANCE:
        return random.choice([0, ITEM_COUNT + 1])
    return random.choice(values)


def new_words():
    """Two different random words."""
    return tuple(random.sample(WORDS, 2))


def new_grid():
    """A small grid of random numbers from 1 to 9."""
    rows, cols = GRID_SIZE
    return [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    bars = BarsRenderer()
    table = TableRenderer()
    graph_view = GraphRenderer()
    graph_view.set_graph(SAMPLE_GRAPH, SAMPLE_POSITIONS)
    graph_mode = False
    graph_key = GRAPH_KEY
    start_node = 0
    renderer = bars
    words = new_words()
    grid = new_grid()
    table_mode = False
    table_key = LCS_KEY

    data = new_data()
    name, algorithm = ALGORITHMS[pygame.K_1]
    steps = algorithm(data)
    current = Step('idle', (), list(data))

    paused = False
    speed_index = 4
    time_since_step = 0.0
    compares = 0
    changes = 0  # swaps and writes
    running = True

    searching = False
    target = None

    def restart(key=None):
        nonlocal name, algorithm, steps, current, time_since_step
        nonlocal compares, changes, searching, target
        nonlocal renderer, table_mode, table_key, graph_mode, graph_key
        if key in GRAPH_ALGORITHMS:
            graph_mode = True
            graph_key = key
            table_mode = False
            searching = False
            name = GRAPH_ALGORITHMS[key][0]
            graph_view.label = GRAPH_ALGORITHMS[key][2]
        elif key is not None:
            graph_mode = False
        if key in GRAPH_ALGORITHMS:
            pass  # already set above
        elif key in TABLE_KEYS or key == GRID_KEY:
            table_mode = True
            searching = False
            table_key = key
            if key == GRID_KEY:
                name = 'Move down right'
            else:
                name = TABLE_KEYS[key][0]
        elif key == SEARCH_KEY:
            table_mode = False
            searching = True
            name = 'Binary search'
        elif key is not None:
            table_mode = False
            searching = False
            name, algorithm = ALGORITHMS[key]
        renderer = bars
        if table_mode:
            renderer = table
        elif graph_mode:
            renderer = graph_view
        if graph_mode:
            steps = GRAPH_ALGORITHMS[graph_key][1](SAMPLE_GRAPH, start_node)
            current = Step('idle', (), [], [])
        elif table_mode:
            if table_key == GRID_KEY:
                table.set_words('', '')
                steps = move_down_right(grid)
            else:
                table.set_words(*words)
                steps = TABLE_KEYS[table_key][1](*words)
            current = Step('idle', (), [])
        elif searching:
            shown = sorted(data)
            target = new_target(shown)
            steps = binary_search(shown, target)
            current = Step('idle', (), shown)
        else:
            steps = algorithm(data)
            current = Step('idle', (), list(data))
        time_since_step = 0.0
        compares = 0
        changes = 0

    while running:
        # Events are handled on every frame, even when paused.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                key = NUMPAD.get(event.key, event.key)
                if key == pygame.K_SPACE:
                    paused = not paused
                elif key == pygame.K_UP:
                    speed_index = min(speed_index + 1, len(SPEEDS) - 1)
                elif key == pygame.K_DOWN:
                    speed_index = max(speed_index - 1, 0)
                elif key in ALGORITHMS or key in (SEARCH_KEY, GRID_KEY, *GRAPH_ALGORITHMS, *TABLE_KEYS):
                    restart(key)
                elif key == pygame.K_r:
                    if graph_mode:
                        start_node = random.choice(list(SAMPLE_GRAPH))
                    elif table_mode:
                        words = new_words()
                        grid = new_grid()
                    else:
                        data = new_data()
                    restart()

        # One step per tick. The tick length depends on the speed.
        time_since_step += clock.get_time() / 1000
        tick = 1 / SPEEDS[speed_index]
        if not paused and time_since_step >= tick:
            time_since_step = 0.0
            next_step = next(steps, None)
            if next_step is not None:
                current = next_step
                if next_step.kind == COMPARE:
                    compares += 1
                elif next_step.kind in (SWAP, WRITE):
                    changes += 1

        renderer.draw(screen, current)
        state = 'paused' if paused else f'{SPEEDS[speed_index]} steps/s'
        if graph_mode:
            if current.kind == DONE:
                result = 'order: ' + ' '.join(str(n) for n in current.info)
            else:
                result = 'searching...'
            caption = f'{name} - {state} - start: {start_node} - {result}'
        elif table_mode:
            if current.kind != DONE:
                result = 'working...'
            elif table_key == LCS_KEY:
                result = f'answer: "{current.info}"'
            else:
                result = f'answer: {current.info}'
            if table_key == GRID_KEY:
                caption = f'{name} - {state} - best sum - {result}'
            else:
                caption = (f'{name} - {state} - "{words[0]}" and '
                           f'"{words[1]}" - {result}')
        elif searching:
            if current.kind == DONE:
                result = f'found at index {current.indices[0]}'
            elif current.kind == NOT_FOUND:
                result = 'not found (-1)'
            else:
                result = 'searching...'
            caption = f'{name} - {state} - target: {target} - {result}'
        else:
            caption = (f'{name} - {state} - compares: {compares}, '
                       f'swaps/writes: {changes}')
        pygame.display.set_caption(caption)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
