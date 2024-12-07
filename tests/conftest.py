import asyncio

import pytest
from autocr_test.utils.config import config, Environment
from autocr_test.utils.red_engine import RedEngine

config.ENV = Environment.TEST

@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope='function')
async def run_around_tests(event_loop):
    await RedEngine().drop_db()
    yield
