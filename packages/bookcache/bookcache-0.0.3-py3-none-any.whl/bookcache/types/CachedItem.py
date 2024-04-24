# Import types
from pydantic import BaseModel
from datetime import datetime
import typing


# Create type
class CachedItem(BaseModel):
    """
    Example usage of `CachedItem`.

    ----

    .. code-block:: python3

    # Import modules
    from datetime import datetime, timedelta

    # Create the time object so it cannot drift
    time = datetime.now()

    # Create a new CachedItem
    CachedItem(
        createdAt = time,
        expireAt = time + timedelta(minutes=15),
        librarianIteration = 0,
        value = "Hello world!!",
    )
    """

    createdAt: datetime
    expireAt: datetime
    librarianIteration: int
    value: typing.Any
