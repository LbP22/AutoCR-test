from fastapi import APIRouter


class ApiRouterHelper:
    def __init__(self, path: str, tags: list):
        self.prefix = '/api'
        self.path = path
        self.tags = tags

        self._routers: dict[int, APIRouter] = {}

    def version(self, version: int) -> APIRouter:
        router = self._routers.get(version, None)
        if not router:
            router = APIRouter(prefix=f'{self.prefix}/v{version}/{self.path}', tags=self.tags)
            self._routers[version] = router

        return router

    @property
    def versions_list(self) -> list:
        return self._routers.values()