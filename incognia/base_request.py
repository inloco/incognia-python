import json
import platform
import sys
from typing import Final, Any, Union, Optional

import requests

from incognia.exceptions import IncogniaHTTPError

_LIBRARY_VERSION: Final[str] = sys.modules['incognia'].__version__
_OS_NAME: Final[str] = platform.system()
_OS_VERSION: Final[str] = platform.release()
_OS_ARCH: Final[str] = platform.architecture()[0]
_LANGUAGE_VERSION: Final[str] = platform.python_version()

USER_AGENT_HEADER: Final[dict] = {
    'User-Agent': f'incognia-python/{_LIBRARY_VERSION}'
                  f' ({_OS_NAME} {_OS_VERSION} {_OS_ARCH})'
                  f' Python/{_LANGUAGE_VERSION}'
}

JSON_CONTENT_HEADER: Final[dict] = {
    'Content-Type': 'application/json'
}


class BaseRequest:
    def __init__(self, timeout: float = 5.0):
        self.__timeout: float = timeout

    def timeout(self) -> float:
        return self.__timeout

    def post(self, url: Union[str, bytes], headers: Any = None, data: Any = None,
             params: Any = None,
             auth: Optional[Any] = None) -> Optional[dict]:
        headers = headers or {}
        headers.update(USER_AGENT_HEADER)

        try:
            response = requests.post(url=url, headers=headers, data=data, params=params,
                                     timeout=self.__timeout,
                                     auth=auth)
            response.raise_for_status()
            if len(response.content) == 0:
                return None
            return json.loads(response.content.decode('utf-8')) or None

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e) from None

    def get(self, url: Union[str, bytes], headers: Any = None, data: Any = None) -> Optional[dict]:
        headers = headers or {}
        headers.update(USER_AGENT_HEADER)

        try:
            response = requests.get(url=url, headers=headers, data=data, timeout=self.__timeout)
            response.raise_for_status()
            return json.loads(response.content.decode('utf-8')) or None

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e) from None
