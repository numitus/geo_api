from pydantic_settings import BaseSettings


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Application settings.

    The parameter value can be changed by using an environment variable with the same
    name as parameter name (e.g. `CORS_ALLOW_METHODS=db`).
    """

    class Config:  # pylint: disable=too-few-public-methods,missing-class-docstring
        env_prefix = ""

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_db: str = "geo_api"
    celery_broker_url: str = "amqp://localhost:5672//"
    geocode_api: str


settings = Settings()
