"""Module for GUI implementation"""
import os
from dataclasses import dataclass
from enum import Enum
from time import sleep

import pygame


class Color(Enum):
    """enum class as wrapper for pygame colors"""

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 128)
    BLACK = (0, 0, 0)


@dataclass
class Gui:
    """Class as wrapper for pygame GUI"""

    width: int = 0
    height: int = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    asset_dir = os.path.abspath(os.path.join(dir_path, "../assets"))

    async def create(self) -> None:
        """method to create an asynchronously instance from outside"""
        pygame.init()

        # self.clock = pygame.time.Clock()
        flags = pygame.FULLSCREEN  # | pygame.OPENGL | pygame.HIDDEN
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        # pygame.display.init()

    #
    @staticmethod
    def update() -> None:
        """method for updating the screen"""
        pygame.display.update()

    @staticmethod
    def end() -> None:
        """method to end pygame"""
        pygame.quit()

    # https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    def blit_text(self, text, pos, font, color=pygame.Color("black")):
        """method to blit text in pygame"""
        words = [
            word.split(" ") for word in text.splitlines()
        ]  # 2D array where each row is a list of words.
        space = font.size(" ")[0]  # The width of a space.
        max_width, max_height = self.screen.get_size()
        word_height = 0.0
        x_pos, y_pos = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x_pos + word_width >= max_width:
                    x_pos = pos[0]  # Reset the x.
                    y_pos += word_height  # Start on new row.
                self.screen.blit(word_surface, (x_pos, y_pos))
                x_pos += word_width + space
            x_pos = pos[0]  # Reset the x.
            y_pos += word_height  # Start on new row.

    def set_bg(self, image: str, timer: float = 3.0) -> None:
        """method to set background"""
        background = pygame.image.load(image)
        self.screen.blit(background, (0, 0))
        # pygame.display.flip()
        self.update()
        sleep(timer)

    @staticmethod
    def set_font(font: str, size: int = 15) -> pygame.font.Font:
        """method to set a system font"""
        return pygame.font.SysFont(font, size)

    @staticmethod
    def run() -> None:
        """method for running the event loop"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        running = False


async def create_gui() -> Gui:
    """Function to create a virus instance from outside"""
    gui = Gui()
    await gui.create()
    return gui
