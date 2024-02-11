from pydantic_settings import BaseSettings


class DB(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017/admin"
    mongodb_api_servidor: str = "1"
    banco: str = "rinha"


db = DB()
