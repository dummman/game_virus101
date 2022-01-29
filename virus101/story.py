import os
from time import sleep

from gui import Color, create_gui


class Story:
    async def create(self) -> None:
        self.gui = await create_gui()

    def blackscreen(self, msg: str, timer: float = 3.0) -> None:
        font = self.gui.set_font("Comic Sans MS", 15)
        try:
            self.gui.blit_text(msg, (0, 0), font, Color.WHITE.value)
            # text = font.render(f'Hier ist deine beliebte Datei...\n\n\n{msg}', True, white, black)
        except ValueError:
            text = font.render(
                "Leider habe ich auch deine Lieblingsdatei verloren.. upps",
                True,
                Color.WHITE.value,
                Color.BLACK.value,
            )
            textRect = text.get_rect()
            self.gui.screen.blit(text, textRect)
        # pygame.display.flip()
        self.gui.update()
        sleep(timer)

    def bluescreen(self, timer: float = 3.0) -> None:
        self.gui.set_bg(os.path.join(self.gui.asset_dir, "BSoD-10.jpg"), timer=timer)


async def create_story() -> Story:
    story = Story()
    await story.create()
    return story
