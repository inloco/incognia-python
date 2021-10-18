import json


def encode(d: dict) -> bytes:
    return json.dumps({k: v for (k, v) in d.items() if v is not None},
                      ensure_ascii=False).encode('utf-8')
