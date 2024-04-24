# -*- coding: utf-8 -*-
from datetime import datetime

from starlette.responses import JSONResponse

from accuhitutils.utils.error_code import ErrorCode
from accuhitutils.utils.payload import ResponsePayloadBuilder


class CommonRuntimeException(Exception):
    """定義共用的RuntimeException"""

    @property
    def code(self):
        return self.args[0]

    @property
    def params(self):
        return self.args[1:] if len(self.args) > 1 else ()


class ApplicationException(Exception):
    """
    定義應用程式的ApplicationException
    service層:
         if not account:
            raise ApplicationException(ApplicationErrorCode.CREDENTIALS_ERROR)

    controller層:
        try:
            res_data = ...
            return payload.build(CommonErrorCode.SUCCESS, res_data)
        except ApplicationException as ex:
            return ex.build_status()
    """

    def __init__(self, errorCode: ErrorCode, statusCode=200):
        self.payload = ResponsePayloadBuilder()
        self.errorCode = errorCode
        self.timestamp = datetime.now()
        self.statusCode = statusCode

    def build(self):
        return self.payload.build(errorCode=self.errorCode)

    def build_status(self):
        return JSONResponse(
            status_code=self.statusCode,
            content=self.payload.build(errorCode=self.errorCode)
        )
