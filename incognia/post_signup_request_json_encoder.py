import json
from typing import Any


class PostSignupRequestJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        def remove_keys_with_none_values(d: dict) -> dict:
            return {k: v for (k, v) in d.items() if v is not None}

        if isinstance(o, dict):
            return remove_keys_with_none_values(o)
        if hasattr(o, '__dict__'):
            return remove_keys_with_none_values(o.__dict__)
        return json.JSONEncoder.default(self, o)
