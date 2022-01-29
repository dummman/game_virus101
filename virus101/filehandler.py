"""Module for file handling"""
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union
from datetime import datetime
# import click

DEFAULT_USERNAME = 'anonym'

@dataclass
class FileHandler:
    """class for handling files"""
    files: list[Path] = field(default_factory=list)
    home: Path = Path.home()
    user_name: str = DEFAULT_USERNAME
    _the_chosen_one: Optional[Path] = None

    @property
    def the_chosen_one(self) -> Optional[Path]:
        return self._the_chosen_one

    @the_chosen_one.setter
    def the_chosen_one(self, value: Union[Path, str]) -> None:
        self._the_chosen_one = Path(value)
        
    async def get_files(self) -> None:
        """Method to scan all files in the home directory of the user."""
        items = self.home.glob("**/*")
        self.files.extend(items)
        # with click.progressbar(items, item_show_func=lambda x: f"scanning {x}") as pb:
        # with click.progressbar(items, label="scanning filesystem") as p_b:
        #     self.files.extend(p_b)
        #     for child in p_b:
        #         # assert child is not None
        #         p_b.update(1, child)

    async def get_user_name(self) -> None:
        """Method to get the username"""
        user_name = os.environ.get('USERNAME', DEFAULT_USERNAME)
        if user_name == DEFAULT_USERNAME:
            user_name = os.environ.get('USER', DEFAULT_USERNAME)
        self.user_name = user_name.capitalize()

    async def analyze_file(self) -> tuple[float, float]:
        """Analyze file the_chosen_one"""
        assert self.the_chosen_one is not None
        atime = self.the_chosen_one.stat().st_atime
        now = datetime.now().timestamp()
        return now - atime, self.the_chosen_one.stat().st_size
