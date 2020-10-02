import os
import asyncio

from .text import findtext
from .vid import findvid, findvid_gnu
from .project import detect_lang

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())  # type: ignore
