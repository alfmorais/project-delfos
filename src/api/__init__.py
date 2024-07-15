from fastapi import FastAPI

from src.api.views import data_routers
from src.infrastructure.server.settings import settings


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            title=settings.PROJECT_TITLE,
            version=settings.PROJECT_VERSION,
        )
        self._include_routers()

    def _include_routers(self) -> None:
        self.include_router(data_routers)


app = App()
