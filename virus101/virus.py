"""Module for defining virus behavior"""
from dataclasses import dataclass
from enum import Enum

from config import VARIABLES, Config



class Mood(Enum):
    """class to catch mood of program"""

    AGGRO = {
        "fg": "red",
        "bold": True,
        "underline": True,
        "overline": True,
        "italic": True,
    }
    ANGRY = {"fg": "red", "bold": True}
    BITTER = {"fg": "yellow", "bold": True}
    NORMAL = {"fg": "bright_green"}
    THINK = {"fg": "cyan"}


@dataclass
class Virus:
    """virus class"""

    config: Config
    started: int = 0
    mood: Mood = Mood.NORMAL
    name: str = "anonym"
    _anger_score: int = 0

    async def create(self) -> None:
        """Set attributes of instance"""
        self.started = int(await self.config.get("started"))
        print(self.started)
        self.name = await self.config.get("name")
        self.anger_score = int(await self.config.get("anger_score"))

    async def set_config(self) -> None:
        """Set configuration instance"""
        for key in VARIABLES:
            await self.config.set(key, str(getattr(self, key)))
        await self.config.create_configfile()

    @property
    def anger_score(self) -> int:
        return self._anger_score

    @anger_score.setter
    def anger_score(self, value: int) -> None:
        self._anger_score = value
        if self._anger_score >= 5:
            self.mood = Mood.AGGRO
        elif self._anger_score >= 3:
            self.mood = Mood.ANGRY
        elif self._anger_score >= 1:
            self.mood = Mood.BITTER

async def create_virus(config) -> Virus:
    """Function to create a virus instance from outside"""
    virus = Virus(config)
    await virus.create()
    return virus
