"""Handlers globais para gestão de erros da API."""

from fastapi import Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from src.main import app


@app.exception_handler(RequestValidationError)
async def erro_requisicao_incompleta(request: Request, exc: ValidationError):
    """Processa exceções de validação Pydantic."""
    erros = exc.errors()[0]
    if erros["type"] == "missing":
        motivo_erro = "não foi informado"
    else:
        motivo_erro = "não pode ser processado. O tipo de dado informado está correto?"

    parametro = erros["loc"][1]

    return JSONResponse(
        content={"msg": f"o parâmetro '{parametro}' {motivo_erro}."},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
