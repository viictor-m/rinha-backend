"""Módulo de rotas da API."""

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.clientes.acoes import fazer_transacao
from src.clientes.esquemas import CorpoTransacao


rotas = APIRouter()


@rotas.post("/{id}/transacoes")
def transacionar(id: int, corpo: CorpoTransacao) -> JSONResponse:
    """
    Realiza a transação pedida ao ID de entrada.

    Transação só realmente será realizada se houver saldo suficiente disponível para
    tal. Caso contrário, esta não será completa.

    Parameters
    ----------
    id : int
        ID do usuário para transacionar.
    corpo : CorpoTransacao
        Informações da transação.

    Returns
    -------
    JSONResponse
        Reposta contendo limite e saldo atualizado do usuário.
    """
    novos_valores = fazer_transacao(id, corpo)
    return JSONResponse(content=jsonable_encoder(novos_valores))
