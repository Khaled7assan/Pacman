from typing import Tuple, List
import pygame as pg

from pacman.misc import Animator
from pacman.misc.cell_util import CellUtil
from pacman.objects import DrawableObject


class Character(DrawableObject):
    direction = {
        "right": (1, 0, 0),
        "down": (0, 1, 1),
        "left": (-1, 0, 2),
        "up": (0, -1, 3),
        "none": (0, 0, None),
    }

    def __init__(self, game, animator: Animator, start_pos: Tuple[int, int], aura: str = None) -> None:
        super().__init__()
        self.game = game
        self.__aura = pg.image.load(aura) if aura else aura
        self.animator = animator
        self.rect = self.animator.current_image.get_rect()
        self.shift_x, self.shift_y = self.direction["right"][:2]
        self.start_pos = CellUtil.pos_from_cell(start_pos)
        self.move_center(*self.start_pos)
        self.speed = 0
        self.rotate = 0

    def step(self) -> None:
        self.rect.centerx = (self.rect.centerx + self.shift_x * self.speed + self.game.width) % self.game.width
        self.rect.centery = (self.rect.centery + self.shift_y * self.speed + self.game.height) % self.game.height

    def go(self) -> None:
        if self.speed != 0:
            self.animator.start()
        self.speed = 1

    def stop(self) -> None:
        self.animator.stop()
        self.speed = 0

    def set_direction(self, new_direction="none") -> None:
        if new_direction:
            self.shift_x, self.shift_y, rotate = self.direction[new_direction]
            if self.rotate != rotate:
                self.rotate = rotate
                self.animator.rotate = rotate
                if self.animator.is_rotation:
                    self.animator.change_rotation()

    def process_logic(self) -> None:
        self.step()

    def process_draw(self, screen: pg.Surface) -> None:
        for i in range(-1, 2):
            if self.animator.current_aura:
                screen.blit(
                    self.animator.current_aura,
                    (
                        self.rect.centerx - self.__aura.get_rect().width // 2,
                        self.rect.centery - self.__aura.get_rect().height // 2,
                    ),
                )
            elif self.__aura:
                screen.blit(
                    self.__aura,
                    (
                        self.rect.centerx - self.__aura.get_rect().width // 2,
                        self.rect.centery - self.__aura.get_rect().height // 2,
                    ),
                )
            screen.blit(
                self.animator.current_image,
                (self.rect.x + self.game.width * i, self.rect.y),
            )

    def movement_cell(self, cell: Tuple[int, int]) -> list:
        scene = self.game.current_scene
        cell = scene.movements_data[cell[1]][cell[0]]
        return [i == "1" for i in "{0:04b}".format(cell)[::-1]]

    def move_to(self, direction) -> bool:
        return self.movement_cell(self.get_cell())[direction]

    def get_cell(self) -> Tuple[int, int]:
        return CellUtil.get_cell(self.rect)

    def in_rect(self, rect: List[int]) -> bool:
        return rect[0] <= self.get_cell()[0] <= rect[2] and rect[1] <= self.get_cell()[1] <= rect[3]

    @staticmethod
    def two_cells_dis(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> float:
        return CellUtil.two_cells_dis(cell1, cell2)
