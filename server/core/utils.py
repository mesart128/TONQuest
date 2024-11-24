import json
from datetime import datetime
from enum import Enum

from tonsdk.utils import Address


def read_address(cell):
    data = "".join([str(cell.bits.get(x)) for x in range(cell.bits.length)])
    if len(data) < 267:
        return None
    wc = int(data[3:11], 2)
    hashpart = int(data[11 : 11 + 256], 2).to_bytes(32, "big").hex()
    return Address(f"{wc if wc != 255 else -1}:{hashpart}")


def _prepare_message(message):
    def convert_obj(obj):
        if isinstance(obj, dict):
            return {key: convert_obj(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_obj(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return obj

    if isinstance(message, str):
        return message.encode("utf-8")
    else:
        message_with_converted_objects = convert_obj(message)
        return json.dumps(message_with_converted_objects).encode("utf-8")
