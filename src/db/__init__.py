from motor.motor_asyncio import AsyncIOMotorClient

from src import config
from src.logit import log


cliente = AsyncIOMotorClient(config.db.mongodb_uri)
banco = cliente[config.db.banco]

try:
    cliente.admin.command("ping")
except Exception as e:
    log.critical("Erro ao estabelecer conexão com o banco de dados.")
    log.exception(e)
else:
    log.info("Conexão com o banco de dados estabelecida!")
