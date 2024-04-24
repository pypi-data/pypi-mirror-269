# -*- coding: utf-8 -*-
import json
import hashlib


def create_md5(data):
    md5 = hashlib.md5()
    md5.update(data.encode("utf-8"))
    return md5.hexdigest()


def validate_request_checksum(request_data):
    """
    :param checksum:
    :param data:
    :return:
    """
    checksum = request_data.get("checksum")
    if checksum and request_data:
        request_data.pop("checksum")
        result = create_request_checksum(request_data)
        return result.lower() == checksum.lower()
    return False


def create_request_checksum(data):
    """
    create checksum
    :param checksum:
    :param data:
    :return:
    """
    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return create_md5(data_json)
