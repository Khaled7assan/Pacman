import pygame as pg

from pacman.data_core import Colors, PathManager
from pacman.misc import CELL_SIZE, HIGH_CALORIE_SEEDS
from pacman.objects import DrawableObject


class SeedContainer(DrawableObject):
    def __init__(self, game, seed_data, energizer_data, x=0, y=20) -> None:
        super().__init__()
        self.game = game
        self.__ram_img = pg.image.load(PathManager.get_image_path("ram"))
        self.__x = x
        self.__y = y
        self.__seeds = seed_data
        self.__energizers = energizer_data
        self.__color = {-1: Colors.WHITE, 1: Colors.BLACK}
        self.__index_color = 1
        self.__seeds_on_field = 0
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    self.__seeds_on_field += 1
        self.__max_seeds = self.__seeds_on_field

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __draw_seeds(self, screen) -> None:
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col]:
                    if self.game.skins.current.name == "chrome":
                        screen.blit(
                            self.__ram_img,
                            (
                                self.x + col * CELL_SIZE + CELL_SIZE // 2 - 6,
                                self.y + row * CELL_SIZE + CELL_SIZE // 2 - 6,
                            ),
                        )
                    else:
                        pg.draw.circle(
                            screen,
                            Colors.WHITE,
                            (
                                self.x + col * CELL_SIZE + CELL_SIZE // 2,
                                self.y + row * CELL_SIZE + CELL_SIZE // 2,
                            ),
                            1,
                        )

    def __draw_energizers(self, screen) -> None:
        if pg.time.get_ticks() - self.game.animate_timer > self.game.time_out:
            self.game.animate_timer = pg.time.get_ticks()
            self.__index_color *= -1
        for energizer in self.__energizers:
            pg.draw.circle(
                screen,
                self.__color[self.__index_color],
                (
                    self.x + energizer[0] * CELL_SIZE + CELL_SIZE // 2,
                    self.y + energizer[1] * CELL_SIZE + CELL_SIZE // 2,
                ),
                4,
            )

    def process_draw(self, screen: pg.Surface) -> None:
        self.__draw_seeds(screen)
        self.__draw_energizers(screen)

    def process_collision(self, object) -> int:
        for row in range(len(self.__seeds)):
            for col in range(len(self.__seeds[row])):
                if self.__seeds[row][col] and row * CELL_SIZE + 18 == object.rect.y:
                    if col * CELL_SIZE - 2 == object.rect.x:
                        self.__seeds[row][col] = None
                        if not self.game.sounds.seed.is_busy():
                            self.game.sounds.seed.play()
                        self.game.score.eat_seed()
                        self.__seeds_on_field -= 1
                        return 1
        for energizer in self.__energizers:
            if energizer[1] * CELL_SIZE + 18 == object.rect.y:
                if energizer[0] * CELL_SIZE - 2 == object.rect.x:
                    self.__energizers.remove(energizer)
                    self.game.score.eat_energizer()
                    return 2

    def is_field_empty(self) -> bool:
        return self.__seeds_on_field == (self.__max_seeds - 10 if HIGH_CALORIE_SEEDS else 0)
