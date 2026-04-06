from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def ok(message: str = "success", data: Any = None, code: int = 200) -> JSONResponse:
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"code": code, "message": message, "data": data}),
    )


def fail(
    message: str,
    *,
    code: int = 500,
    status_code: int = 500,
    data: Any = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder({"code": code, "message": message, "data": data}),
    )
