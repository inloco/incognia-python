import base64
import datetime as dt
from threading import Lock
from typing import Final, Optional, NamedTuple

from .base_request import BaseRequest
from .endpoints import Endpoints
from .exceptions import IncogniaHTTPError

_TOKEN_REFRESH_BEFORE_SECONDS: Final[int] = 10


class TokenValues(NamedTuple):
    access_token: str
    token_type: str


class TokenManager:
    def __init__(self, client_id: str, client_secret: str):
        self.__client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__token_values: Optional[TokenValues] = None
        self.__expiration_time: Optional[dt.datetime] = None
        self.__request: BaseRequest = BaseRequest()
        self.__mutex: Lock = Lock()

    def __refresh_token(self) -> None:
        client_id, client_secret = self.__client_id, self.__client_secret
        client_id_and_secret_encoded = base64.urlsafe_b64encode(
            f'{client_id}:{client_secret}'.encode('ascii')).decode('utf-8')
        headers = {'Authorization': f'Basic {client_id_and_secret_encoded}'}

        try:
            response = self.__request.post(url=Endpoints.TOKEN, headers=headers,
                                           auth=(client_id, client_secret))
            token_values = TokenValues(response['access_token'], response['token_type'])
            expiration_time = dt.datetime.now() + dt.timedelta(seconds=int(response['expires_in']))

            self.__token_values, self.__expiration_time = token_values, expiration_time

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def __is_expired(self) -> bool:
        return (self.__expiration_time - dt.datetime.now()) \
                   .total_seconds() <= _TOKEN_REFRESH_BEFORE_SECONDS

    def get(self) -> TokenValues:
        self.__mutex.acquire()
        if not self.__expiration_time or self.__is_expired():
            self.__refresh_token()
        token_values = self.__token_values
        self.__mutex.release()
        return token_values
