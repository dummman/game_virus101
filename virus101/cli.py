"""Console script for virus101."""
import asyncio
import os
import sys

import click
from communication import create_comms
from startup import startup

os.environ["TK_SILENCE_DEPRECATION"] = "1"


@click.command()
def main() -> int:
    """Console script for virus101."""
    asyncio.run(chain())
    return 0


async def chain() -> None:
    """chaining function for asyncio"""
    result  = await asyncio.gather(create_comms(), startup())
    comms = result[0]
    await comms.talkthrough()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
