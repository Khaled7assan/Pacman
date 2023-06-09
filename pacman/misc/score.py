from pacman.misc import Points


class Score:
    def __init__(self) -> None:
        self.__score = 0
        self.fear_mode = False
        self.fear_count = 0

    def __str__(self):
        return str(self.__score)

    def __int__(self):
        return self.__score

    @property
    def score(self):
        return self.__score

    def reset(self) -> None:
        self.__score = 0

    def __add__(self, value):
        self.__score = self.__score + value
        return self

    def __iadd__(self, value):
        return self + value

    def eat_seed(self) -> None:
        self + Points.POINT_PER_SEED

    def eat_energizer(self) -> None:
        self + Points.POINT_PER_ENERGIZER

    def eat_fruit(self, bonus) -> None:
        self + bonus

    def activate_fear_mode(self) -> None:
        self.fear_mode = True
        self.fear_count = 0

    def deactivate_fear_mode(self) -> None:
        self.fear_mode = False
        self.fear_count = 0

    def eat_ghost(self) -> None:
        self + (200 * 2**self.fear_count)
        self.fear_count += 1
