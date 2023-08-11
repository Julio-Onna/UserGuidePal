import aiohttp


class BaseClient:
    def __init__(self):
        self._session = None

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
