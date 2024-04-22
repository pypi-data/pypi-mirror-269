import asyncio
import traceback

from typing import Any, Union, Optional, Callable, Awaitable
from dataclasses import dataclass, field


@dataclass
class _Request:
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    completed: asyncio.Event = field(default_factory=asyncio.Event)
    check: Optional[Callable[..., bool]] = field(default=None)
    result: Union[Any, tuple[Any]] = field(default=None)


class Requeue:
    """
    An asynchronous queue for requesting data
    """

    def __init__(self) -> None:
        self._requests: list[_Request] = []
        self._lock = asyncio.Lock()

    async def wait_for(self,
        check: Optional[Callable[..., bool]] = None,
        timeout: Optional[float] = None,
    ) -> Union[Any, tuple[Any]]:
        """
        Make a request for data and wait for it.
        
        Optionally, apply a check to only permit data matching certain criteria.
        `check` should return a boolean of whether it is a match or not.
        """

        request = _Request(check=check)

        async with self._lock:
            self._requests.append(request)

        try:
            await asyncio.wait_for(request.completed.wait(), timeout=timeout)
            
            async with request.lock:
                result = request.result

            if len(result) == 1:
                return result[0]
            return result

        finally:
            # In case the request is still found in the list,
            # signal to `complete` that the request has expired.
            request.completed.set()

            async with self._lock:
                self._requests.remove(request)

    async def complete(self, *contents: Any) -> Awaitable[bool]:
        """
        Look for a matching request and complete it.
        Returns whether a request was completed.
        """

        async with self._lock:
            requests = self._requests[:]

        for request in requests:
            # Skip timed out requests.
            if request.completed.is_set():
                continue

            try:
                if request.check is not None and not request.check(*contents):
                    continue
            except Exception:
                # Ignore any exception raised with the calling of the check.
                # If the check or data is faulty, that should not affect
                # or interrupt the completion of other requests.
                traceback.print_exc()
                continue

            async with request.lock:
                request.result = contents

            # Signal that the request has been completed.
            request.completed.set()

            return True
        return False
