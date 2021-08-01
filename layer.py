from enum import IntEnum, auto

class Layer(IntEnum):
    CREATURE = auto()
    OBSTACLE = auto()
    BASE = auto()
    UI = auto()

if __name__ == '__main__':
    print(Layer.BASE >= Layer.OBSTACLE)