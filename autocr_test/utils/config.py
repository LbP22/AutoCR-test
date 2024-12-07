import enum

from pydantic_settings import BaseSettings


class Environment(str, enum.Enum):
    MAIN = 'main'
    DEV = 'dev'
    TEST = 'testing'
    LOCAL = 'local'


class Config(BaseSettings):
    ENV: Environment = Environment.LOCAL
    PYTHONPATH: str = '.' # Only for local

    REDIS_URL: str = 'redis://localhost:6379'
    REPO_CACHE_TTL: int = 60 * 60 * 24  # day

    REPO_SIZE_LIMIT: int = 1000000

    GITHUB_TOKEN: str
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = 'gpt-4-turbo'

    class Config:
        env_file = ".env"

config = Config()
