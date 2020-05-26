from src.model.DiceEnum import DiceEnum


class Dice:
    def __init__(self, type_dice: DiceEnum, dot: int):
        if is_valid_dot_dice(dot):
            raise Exception('Out of valid dot range : (' + str(dot) + ')')

        self.type_dice = type_dice
        self.dot = dot

def is_valid_dot_dice(dot: int):
    """Return a boolean if if valid dot range"""
    return 0 < dot <= 7
