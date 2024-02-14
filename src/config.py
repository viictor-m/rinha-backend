from pydantic_settings import BaseSettings


class DB(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017/admin"
    banco: str = "rinha"


db = DB()
