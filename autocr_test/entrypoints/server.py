import asyncio
import inspect
import sqlite3
import time
from contextlib import asynccontextmanager
from types import ModuleType

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from odmantic import Model
import uvicorn

from .. import routes
from ..utils.config import Environment, config
from ..utils.router_helper import ApiRouterHelper

def register_helper_routes():
    route_versions_list = [module for _, module in inspect.getmembers(routes, lambda x: isinstance(x, ModuleType))]
    for version in route_versions_list:
        routes_list = [module for _, module in inspect.getmembers(version, lambda x: isinstance(x, ModuleType))]

        for route_module in routes_list:
            router = getattr(route_module, "router", None)
            if router is None:
                continue
            if isinstance(router, APIRouter):
                app.include_router(router)
            elif isinstance(router, ApiRouterHelper):
                router: ApiRouterHelper
                for version_router in router.versions_list:
                    app.include_router(version_router)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_helper_routes()

def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("autocr_test.entrypoints.server:app", host="0.0.0.0", port=8000, reload=True)
