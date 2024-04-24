# -*- coding: utf-8 -*-
import datetime
import json
import logging
import time
from datetime import datetime

from bson import ObjectId

from accuhitutils.utils.datetime import DEFAULT_DATETIME_PATTERN
from accuhitutils.utils.error_code import ErrorCode

logger = logging.getLogger(__name__)


def obj_to_json(obj):
    """物件轉json"""
    return json.JSONDecoder().decode(JSONEncoder().encode(obj.__dict__))


class JSONEncoder(json.JSONEncoder):
    """json轉字串"""

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj.strftime(DEFAULT_DATETIME_PATTERN))
        return json.JSONEncoder.default(self, obj)


class ResponsePayloadBuilder(object):

    def __init__(self):
        """初始化"""
        self.start_time = time.time()  # 初始時間

    def build(self, errorCode: ErrorCode, data=None, paging=None):
        """
        payload = ResponsePayloadBuilder()
        try:
            res_data = ...
            return payload.build(CommonErrorCode.SUCCESS, res_data)
        except Exception as e:
            return payload.build(CommonErrorCode.UNKNOWN_ERROR, str(e))
        """
        end_time = time.time()
        cost_time = end_time - self.start_time  # 計算時間差
        payload = {
            "code": errorCode.code,
            "message": errorCode.message,
            "costTime": cost_time
        }
        if errorCode.code[2:4] == "99":
            return payload

        payload["data"] = data

        if paging:
            payload["paging"] = paging

        return payload
