from pynput.mouse import Listener

from src.model.Plateau import Plateau

from ahk import AHK

if __name__ == '__main__':
    ahk = AHK()
    plateau = Plateau(ahk)
    plateau.scan()