"""Módulo com as ações lógicas realizadas nos endpoints."""

from fastapi import status
from fastapi.exceptions import HTTPException

from src.clientes.esquemas import CorpoTransacao
from src.clientes.esquemas import Extrato
from src.clientes.esquemas import RegistroTransacao
from src.clientes.esquemas import Transacao
from src.db import banco


async def fazer_transacao(id: int, corpo: CorpoTransacao) -> Transacao:
    """
    Registra as transações de crédito/débito no banco de dados.

    Parameters
    ----------
    id : int
        ID do usuário.
    corpo : CorpoTransacao
        Objeto contendo informações da transação a ser realizada.

    Returns
    -------
    Transacao
        Saldo e limite pós transação realizada.
    """
    dados_usuario = await banco.clientes.find_one(
        {"id": id}, {"_id": 0, "saldo": 1, "limite": 1}
    )

    if not dados_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )

    modelo_usuario = Transacao(**dados_usuario)

    if corpo.tipo == "c":
        modelo_usuario.saldo += corpo.valor
    elif corpo.tipo == "d":
        modelo_usuario.saldo -= corpo.valor
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Tipo de transação informada não reconhecida.",
        )

    registro_transacao = RegistroTransacao(**corpo.model_dump())
    await banco.clientes.update_one(
        {"id": id},
        {
            "$set": {"saldo": modelo_usuario.saldo},
            "$push": {
                "ultimas_transacoes": {
                    "$each": [registro_transacao.model_dump()],
                    "$sort": {"registrada_em": -1},
                    "$slice": 10,
                }
            },
        },
        upsert=True,
    )
    return modelo_usuario


async def gerar_extrato(id: int) -> dict:
    """
    Gera o extrato de um cliente.

    Parameters
    ----------
    id : int
        ID do cliente.

    Returns
    -------
    Extrato
        Extrato com limite, saldo e últimas transações.
    """
    dados = await banco.clientes.find_one({"id": id}, {"_id": 0, "id": 0})
    if not dados:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )
    extrato = Extrato(**dados)
    return extrato.resposta
