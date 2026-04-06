
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from utils.exception import generic_exception_handler, http_exception_handler, intergrity_error_handler, sqlalchemy_exception_handler


def register_exception(app):
    """
    注册异常处理
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(IntegrityError, intergrity_error_handler)
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
