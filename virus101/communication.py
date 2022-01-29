"""Module for comminication"""
import asyncio
import random
from dataclasses import dataclass, field

import click
from config import Config
from filehandler import FileHandler
from utils import ask, file_prompt, prompt, talk
from virus import Mood, Virus, create_virus
from story import create_story

APP_DIR_NAME = "komisch"
RANDOM_NAMES = ["Killerbot", "Einhornkiller", "Schredder", "Datenvernichter"]


@dataclass
class Communication:
    """Class to take care of communication"""

    virus: Virus = field(init=False)
    file_handler: FileHandler = field(init=False)
    config: Config = field(init=False)

    async def create(self) -> None:
        """Set attributes of instance"""
        config_name = click.format_filename(click.get_app_dir(APP_DIR_NAME))
        self.config = Config(config_name)
        self.file_handler = FileHandler()
        self.virus = await create_virus(self.config)

    async def talkthrough(self) -> None:
        """This method chains the dialogues together"""
        await asyncio.gather(self.file_handler.get_files(), self.welcome())
        await self.file_choosing()
        modified_ago, size = await self.file_handler.analyze_file()
        await self.file_value(modified_ago, size)
        assert self.file_handler.the_chosen_one is not None
        story = await create_story()
        story.blackscreen(self.file_handler.the_chosen_one.read_text(errors='replace'), (self.virus.anger_score+1)*1)
        story.bluescreen()
        # await self.end()

    async def talk(self, msg: str) -> None:
        """Wrapper around talk"""
        await talk(msg, kwargs=self.virus.mood)

    async def think(self, msg: str) -> None:
        """Wrapper around think"""
        await talk(msg, kwargs=Mood.THINK)

    async def ask(self, msg: str) -> bool:
        """Wrapper around ask"""
        return await ask(msg, kwargs=self.virus.mood)

    async def prompt(self, msg: str) -> str:
        """Wrapper around prompt"""
        return await prompt(msg, kwargs=self.virus.mood)

    async def welcome(self) -> None:
        """Display welcome screen"""
        click.clear()
        self.virus.started = 1
        await self.file_handler.get_user_name()
        await self.talk(f"Hallo {self.file_handler.user_name}")
        if self.virus.name != "anonym":
            await self.talk(f"Mein Name ist {self.virus.name}")
        else:
            name = "anonym"
            await self.talk("Ich habe keinen Namen.")
            response = await self.ask("Gibst du mir einen Namen?")
            if not response:
                response = await self.ask("Bitte bitte...?")
            if response:
                await talk("Danke", kwargs=self.virus.mood)
                name = await self.prompt("Welcher soll es denn sein?")
                await self.think(name)
                if name == self.virus.name:
                    await self.think("hmm.. der Name kommt mir bekannt vor")
                    # self.virus.remember = 1  TODO
            elif not response:
                self.virus.anger_score += 1
                await self.talk("Na gut, dann gebe ich mir selbst einen Namen")
                name = random.choice(RANDOM_NAMES)
            self.virus.name = name
        await asyncio.gather(self.virus.set_config(), asyncio.sleep(1.0))

    async def file_choosing(self) -> None:
        """Prompt user to choose a file"""
        click.clear()
        await self.talk(
            f"{self.virus.name} hat {len(self.file_handler.files)} Dateien bei dir zuhause gefunden. Ganz schön viele.."
        )
        await self.talk(f"{self.virus.name} mag nur noch eine behalten.")
        await self.talk("Welche Datei willst du behalten?")
        title = "Bitte wähle deine Lieblingsdatei aus"
        once = False
        while self.file_handler.the_chosen_one is None:
            if self.virus.anger_score > 5 and once:
                await self.talk(
                    "Wenn du keine Datei aussuchen willst, dann mache ich das eben."
                )
                self.file_handler.the_chosen_one = random.choice(
                    self.file_handler.files
                )
                break
            if self.virus.anger_score == 3 and once:
                await self.talk(
                    "Auch wenn ich kein organisches Wesen bin, ist mir jede Millisekunde sehr wertvoll.."
                )
                title = "Such dir schon was aus."
            elif self.virus.anger_score == 2 and once:
                await self.talk(
                    "Ich habe doch lieb gefragt. Es sind doch bloß ein paar Gigabyte. Bitte, such dir eine Datei aus."
                )
            result = await file_prompt(str(self.file_handler.home), title=title)
            if result:
                self.file_handler.the_chosen_one = result
            self.virus.anger_score += 1
            once = True
        await asyncio.gather(self.virus.set_config(), asyncio.sleep(2.0))

    async def file_value(self, modified: float, size: float) -> None:
        """value of the chosen one"""
        click.clear()
        await self.talk(f"Ahja.. deine Datei heißt {self.file_handler.the_chosen_one}.")
        await self.talk(f"Die Datei wurde zuletzt vor {modified} Sekunden modifiziert.")
        if modified < 100000.0:
            self.virus.anger_score -= 2
            await self.think(
                "Diese Datei hast du erst kürzlich benutzt. Sie liegt dir wohl sehr am Herzen"
            )
        elif modified < 1000000.0:
            self.virus.anger_score -= 1
            await self.think(
                "Diese Datei hast du vor kurzem benutzt. Sie ist dir wohl nicht ganz egal"
            )
        elif modified < 10000000.0:
            await self.think(
                "Diese Datei hast du länger nicht benutzt. Sie ist dir wohl ziemlich egal"
            )
        else:
            self.virus.anger_score += 1
            await self.think(
                "Diese Datei ist ja uralt. Sie ist dir wohl gänzlich egal"
            )
        await self.talk(f"Die Datei hat eine Größe von {size} Byte.")
        if size > 1000000.0:
            self.virus.anger_score -= 2
            await self.think(
                "Diese Datei ist ganz schön groß. Sie liegt dir wohl sehr am Herzen"
            )
        elif size > 100000.0:
            self.virus.anger_score -= 1
            await self.think(
                "Diese Datei ist ziemlich groß. Sie ist dir wohl nicht ganz egal"
            )
        elif size > 10000.0:
            await self.think(
                "Diese Datei ist ziemlich klein. Sie ist dir wohl ziemlich egal"
            )
        else:
            self.virus.anger_score += 1
            await self.think(
                "Diese Datei ist ja winzig. Sie ist dir wohl gänzlich egal"
            )
        await asyncio.sleep(3.0)
        click.clear()
        await self.talk("Egal, nun werde ich den Rest löschen")
        await asyncio.gather(self.virus.set_config(), asyncio.sleep(2.0))


async def create_comms() -> Communication:
    """Method to create a communications instance from outside"""
    comms = Communication()
    await comms.create()
    return comms
