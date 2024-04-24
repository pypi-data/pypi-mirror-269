# -*- coding: utf-8 -*-
import datetime
import json
import logging
import time
from datetime import datetime

from bson import ObjectId

from accuhit.utils.datetime import DEFAULT_DATETIME_PATTERN
from accuhit.utils.error_code import ErrorCode

logger = logging.getLogger(__name__)


def obj_to_json(obj):
    return json.JSONDecoder().decode(JSONEncoder().encode(obj.__dict__))


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj.strftime(DEFAULT_DATETIME_PATTERN))
        return json.JSONEncoder.default(self, obj)


class ResponsePayloadBuilder(object):

    def __init__(self):
        """
        初始化
        """
        self.start_time = time.time()  # 初始時間

    def build(self, errorCode: ErrorCode, data=None, paging=None):
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
            payload["paging"] = {
                "pageNo": paging.page_no,
                "totalPages": paging.total_page
            }

        return payload
