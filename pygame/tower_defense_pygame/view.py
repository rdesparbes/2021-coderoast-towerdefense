from typing import NamedTuple, Tuple

import pygame
from pygame.surface import Surface

from tower_defense.interfaces.tower_defense_controller import ITowerDefenseController

SCALE = 20


class Rect(NamedTuple):
    left: int
    top: int
    width: int
    height: int


class PyGameView:
    def __init__(
        self, controller: ITowerDefenseController, timestep: int = 1_000
    ) -> None:
        print("Bot initialized")
        self._controller = controller
        self._timestep = timestep

    def _build_background(self) -> Surface:
        width, height = self._controller.map_shape()
        shape: Tuple[int, int] = width * SCALE, height * SCALE
        background = Surface(shape)
        for (col, row), block in self._controller.iter_blocks():
            rect = Rect(left=SCALE * col, top=SCALE * row, width=SCALE, height=SCALE)
            if block.is_constructible:
                color: Tuple[int, int, int] = 102, 145, 112
            elif block.is_walkable:
                color = 75, 67, 12
            else:
                color = 28, 69, 111
            pygame.draw.rect(background, color, rect)
        return background

    def start(self) -> None:
        pygame.init()
        width, height = self._controller.map_shape()
        shape: Tuple[int, int] = width * SCALE, height * SCALE
        screen: Surface = pygame.display.set_mode(shape)
        background: Surface = self._build_background()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.blit(background, (0, 0))
            for tower in self._controller.iter_towers():
                x, y = tower.get_position()
                center = SCALE * x + SCALE // 2, SCALE * y + SCALE // 2
                pygame.draw.circle(
                    screen, color=(180, 165, 114), center=center, radius=SCALE // 2
                )
            for monster in self._controller.iter_monsters():
                x, y = monster.get_position()
                center = SCALE * x + SCALE // 2, SCALE * y + SCALE // 2
                pygame.draw.circle(
                    screen, color=(255, 0, 0), center=center, radius=SCALE // 2
                )
            for projectile in self._controller.iter_projectiles():
                x, y = projectile.get_position()
                center = SCALE * x + SCALE // 2, SCALE * y + SCALE // 2
                pygame.draw.circle(screen, color=(255, 128, 0), center=center, radius=3)
            pygame.display.flip()
        pygame.quit()
