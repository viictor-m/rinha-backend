"""Módulo de rotas da API."""

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.clientes.acoes import fazer_transacao
from src.clientes.acoes import gerar_extrato
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


@rotas.get("/{id}/extrato")
def extrato(id: int) -> JSONResponse:
    """
    Gera extrato do cliente.

    Parameters
    ----------
    id : int
        ID do cliente.

    Returns
    -------
    JSONResponse
        Resposta com valores de limite, saldo e últimas 10 transações.
    """
    valores = gerar_extrato(id)
    return JSONResponse(content=jsonable_encoder(valores))
