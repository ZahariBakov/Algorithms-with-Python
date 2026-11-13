import random

import pygame

from viz.algorithms.sorting import bubble_sort, insertion_sort, selection_sort
from viz.renderers.bars import BarsRenderer
from viz.steps import Step

WINDOW_SIZE = (900, 500)
ITEM_COUNT = 40
FPS = 60

ALGORITHMS = {
    pygame.K_1: ('Bubble sort', bubble_sort),
    pygame.K_2: ('Selection sort', selection_sort),
    pygame.K_3: ('Insertion sort', insertion_sort),
}

# Steps per second. Up goes to the next value, Down to the previous one.
SPEEDS = [2, 5, 10, 20, 40, 80, 160, 320, 640]


def new_data():
    return random.sample(range(1, ITEM_COUNT + 1), ITEM_COUNT)


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    renderer = BarsRenderer()

    data = new_data()
    name, algorithm = ALGORITHMS[pygame.K_1]
    steps = algorithm(data)
    current = Step('idle', (), list(data))

    paused = False
    speed_index = 4
    time_since_step = 0.0
    running = True

    def restart(key=None):
        nonlocal name, algorithm, steps, current, time_since_step
        if key is not None:
            name, algorithm = ALGORITHMS[key]
        steps = algorithm(data)
        current = Step('idle', (), list(data))
        time_since_step = 0.0

    while running:
        # Events are handled on every frame, even when paused.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_UP:
                    speed_index = min(speed_index + 1, len(SPEEDS) - 1)
                elif event.key == pygame.K_DOWN:
                    speed_index = max(speed_index - 1, 0)
                elif event.key in ALGORITHMS:
                    restart(event.key)
                elif event.key == pygame.K_r:
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

        renderer.draw(screen, current)
        state = 'paused' if paused else f'{SPEEDS[speed_index]} steps/s'
        pygame.display.set_caption(f'{name} - {state}')
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
