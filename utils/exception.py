
import traceback

from fastapi import HTTPException, Request, status
from starlette.responses import JSONResponse

from sqlalchemy.exc import IntegrityError, SQLAlchemyError


DEBUG_MODE = True



async def http_exception_handler(request: Request, exc: HTTPException):

    """"
    处理HTTP异常
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )



async def intergrity_error_handler(request: Request, exc: IntegrityError):
    """
    处理数据库完整性异常
    """
    
    error_msg = str(exc.orig)

    # 判断具体的约束值错误
    if "username_UNIQ" in error_msg or "Duplicate entry" in error_msg:
        detail = "用户名已存在"
    elif "foreign key" in error_msg:
        detail = "外键约束异常"
    else:
        detail = "数据库完整性异常"
    

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type" : "integrity_error",
            "error_message" : error_msg,
            "path" : str(request.url)
        }


    return JSONResponse(
        status_code=400,
        content={
            "code": 400,
            "message": detail,
            "data": error_data,
        },
    )




async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    处理SQLAlchemy异常
    """
    error_msg = str(exc.orig)
    detail = "数据库操作失败"

    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type" : type(exc).__name__,
            "error_message" : error_msg,
            "error_detail" : str(exc),
            "error_traceback" : traceback.format_exc(),
            "path" : str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": detail,
            "data": error_data,
        },
    )




async def generic_exception_handler(request: Request, exc: Exception):
    """
    兜底：未单独注册的异常。HTTPException 由 http_exception_handler 处理，一般不会进这里。
    """
    error_msg = str(exc)
    detail = "服务器内部错误"
    error_data = None
    if DEBUG_MODE:
        error_data = {
            "error_type" : type(exc).__name__,
            "error_message" : error_msg,
            "error_detail" : str(exc),
            "error_traceback" : traceback.format_exc(),
            "path" : str(request.url)
        }

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "message": error_msg if DEBUG_MODE else detail,
            "data": error_data,
        },
    )












