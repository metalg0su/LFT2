import json
from typing import Union

from lft.serialization import Serializable


class _JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            print(f"origin byte : {o}")
            return "0x" + o.hex()
        elif isinstance(o, str):
            return "0r" + o
        elif isinstance(o, Serializable):
            return o.serialize()
        else:
            return super().encode(o)


class Serializer:
    def __init__(self):
        self._encoder = _JSONEncoder

    def serialize(self, serializable: Union[Serializable, dict, list]):
        return json.dumps(serializable, cls=self._encoder)

    def deserialize(self, serialized: str):
        return json.loads(serialized, object_hook=object_hook)


def object_hook(s):
    if isinstance(s, str):
        if s[:2] == "0x":
            return bytes.fromhex(s[2:])
        elif s[:2] == "0r":
            return s[2:]
    elif isinstance(s, dict):
        if "!type" in s and "!data" in s:
            return Serializable.deserialize(s)
        else:
            return s
    else:
        return s
