from functools import wraps

from werkzeug.exceptions import NotAcceptable

from accuhitutils.utils.error_code import CommonErrorCode
from accuhitutils.utils.payload import ResponsePayloadBuilder


def accept_headers(*allowed_header, **params):
    """
    e.g @accept_headers("X-CHATBOT", "X-ACCOUNT", req=request, error_code="999999991", app_context=app_context)
    ...
    Parameters
    ----------
    allowed_header: str
        限制的header keys
    params:
        req: request (必填)
        error_code, app_context: 可自定義的錯誤(CommonRuntimeException)，沒有自定義的錯誤則回傳NotAcceptable
    """

    def decorator(fn):
        @wraps(fn)
        def accept(*args, **kwargs):
            req = params.get("req")
            if not req:
                raise ValueError("params \"req\" was required")
            vail_list = list(filter(lambda ah: req.headers.get(ah) is not None, allowed_header))
            allowed_set = set(allowed_header)
            headers_set = set(vail_list)
            check = allowed_set - headers_set
            if not check:
                return fn(*args, **kwargs)
            supported_types = ', '.join(allowed_header)
            description = '{}\nSupported entities are: {} or value is Empty.'.format(
                NotAcceptable.description, supported_types)
            app_context = params.get("app_context")
            error_code = params.get("error_code")
            if app_context and error_code:
                response_payload = ResponsePayloadBuilder()
                return response_payload.build(CommonErrorCode.UNKNOWN_ERROR, str(error_code))
            raise NotAcceptable(description)

        return accept

    return decorator
