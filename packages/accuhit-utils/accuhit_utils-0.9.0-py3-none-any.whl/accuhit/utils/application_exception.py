from datetime import datetime

from starlette.responses import JSONResponse

from accuhit.utils.error_code import ErrorCode
from accuhit.utils.payload import ResponsePayloadBuilder


class ApplicationException(Exception):
    def __init__(self, errorCode: ErrorCode, statusCode=200):
        self.payload = ResponsePayloadBuilder()
        self.errorCode = errorCode
        self.timestamp = datetime.now()
        self.statusCode = statusCode

    def _init_ex(self, errorCode: str, ex: Exception):
        self.errorCode = errorCode
        self.exception = ex

    def build(self):
        return self.payload.build(errorCode=self.errorCode)

    def build_status(self):
        return JSONResponse(
            status_code=self.statusCode,
            content=self.payload.build(errorCode=self.errorCode)
        )
