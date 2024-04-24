"""
MIT License

Copyright (c) 2024-present NotAussie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import required modules
import asyncio
from datetime import datetime, timedelta
from utils.runner import periodically

# Import types/classes
from types.CachedItem import CachedItem
import typing


# Create cache class
class Cache:
    def __init__(self, iterationTiming: float) -> None:

        # Store the timing between iterations
        self._iterationTiming = iterationTiming

        # Create library
        self._library = dict()

        # Create librarian variables
        self._librarianIteration: int = 0
        self._librarianTotalDeletions: int = 0

        # Create task variables
        self._taskLibrarianScan: asyncio.Task = None

    @property
    def totalDeletions(self) -> int:
        """The total deletions by both the librarian and function calls."""
        return self._librarianTotalDeletions

    @property
    def totalIterations(self) -> int:
        """The total iterations of the librarian."""
        return self._librarianIteration

    async def librarianScan(self) -> typing.NoReturn:
        """Runs a scan on the library."""
        # Get the current time and store it
        currentTime = datetime.now()

        # Iterate over the library.
        for key, value in self._library:
            # Check if the item was added in the same iteration
            # if value.librarianIteration == self._librarianIteration:
            # continue
            # ^ ^ ^
            # Going to rethink this feature as it could have issues.

            # Check if the expiry time has passed
            if value.expireAt < currentTime:
                # Pop the item from the library
                self._library.pop(key)

        # Bump the iteration count
        self._librarianIteration += 1

    async def init(self, loop: asyncio.BaseEventLoop) -> typing.NoReturn:
        """Initializes the librarian background functions and initializes other miscellaneous things."""

        # Initialize scanner function
        self._taskLibrarianScan = loop.create_task(
            periodically(self.librarianScan(), self._iterationTiming)
        )

    async def Set(self, key: str, value: typing.Any, ttl: float = None):
        """
        Sets the entered key to a value

        ----

        Arguments:
            `key` (`str`): The identifier for the key.
            `value` (`any`): The value to store.
            `ttl` (`float`, `none`): How many seconds till the key should expire.

        Raises:
            ...
        """

    async def Get(self, key: str) -> typing.Any:
        """
        Fetches the entered key from the cache.

        ----

        Arguments:
            `key` (`str`): The key to look up.

        Returns:
            `any`: The value of the cached object.
        """

        # Attempt to grab the item from cache
        field: CachedItem = self._library.get(key)

        # Return None if key is empty
        if not field:
            return None

        # Return infomation
        return field.value
