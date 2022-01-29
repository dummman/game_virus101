"""Module to handle the configuration"""
import configparser
from pathlib import Path

SECTION = "DEFAULT"
VARIABLES = {
    "started": "0",
    "name": "anonym",
    "anger_score": "0",
}


class Config:
    """Configuration class"""

    filename: Path

    def __init__(self, filename: str) -> None:
        self.filename = Path(filename).resolve()
        self.parser = configparser.ConfigParser(defaults=VARIABLES)
        if self.filename.exists() and self.filename.stat().st_size != 0.0:
            self.parser.read(self.filename)

    async def create_configfile(self) -> None:
        """Method to create the configuration file"""
        with self.filename.open("w+") as _file:
            self.parser.write(_file)

    async def get(self, var: str) -> str:
        return self.parser[SECTION][var]

    async def set(self, name: str, value: str) -> None:
        self.parser.set(SECTION, name, value)
