class ErrorCode:
    """定義ErrorCode父類別"""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message


class CommonErrorCode(ErrorCode):
    """定義共用的ErrorCode"""
    SUCCESS = ErrorCode(code="996600001", message="execute success.")
    ILLEGAL_ERROR = ErrorCode(code="999900001",
                              message="illegal input argument({0[0]}) or input argument({0[0]}) format error.")
    UNKNOWN_ERROR = ErrorCode(code="999999999", message="system is busy now.")
    NETWORK_ERROR = ErrorCode(code="999999995", message="network exception.")
    API_ERROR = ErrorCode(code="999999994", message="API exception.")
    VALIDATION_ERROR = ErrorCode(code="999999993", message="request model validation error.")
