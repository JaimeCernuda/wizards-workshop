from ursina import *
from .game_manager import GameManager


def main():
    app = Ursina()
    
    game = GameManager()
    game.setup()
    
    app.run()


if __name__ == "__main__":
    main()