import asyncio
from typing import Coroutine


async def periodically(function: Coroutine, waitTime: int):
    while True:
        await function()
        await asyncio.sleep(waitTime)
