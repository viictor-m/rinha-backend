"""Módulo de rotas da API."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.clientes.esquemas import CorpoTransacao


rotas = APIRouter()


@rotas.post("/{id}/transacoes")
def transacionar(id: int, corpo: CorpoTransacao) -> JSONResponse:
    return JSONResponse(content=f"Lógica não implementada. id: {id} | corpo: {corpo}")
