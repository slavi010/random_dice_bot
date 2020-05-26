from src.model.DiceEnum import DiceEnum, DiceColorEnum


class Dice:
    def __init__(self, type_dice: DiceColorEnum, dot: int):
        if not is_valid_dot_dice(dot):
            raise Exception('Out of valid dot range : (' + str(dot) + ')')

        self.type_dice = type_dice
        self.dot = dot

    def __str__(self):
        return self.type_dice.name + " " + str(self.dot)


def is_valid_dot_dice(dot: int):
    """Return a boolean if if valid dot range"""
    return 0 < dot <= 7
