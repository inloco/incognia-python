import base64
import datetime as dt
import json
from typing import Final, Optional, NamedTuple

import requests

from .endpoints import Endpoints
from .exceptions import IncogniaHTTPError


class TokenValues(NamedTuple):
    access_token: str
    token_type: str


class TokenManager:
    TOKEN_REFRESH_BEFORE_SECONDS: Final[int] = 10

    def __init__(self, client_id: str, client_secret: str, endpoints: Endpoints):
        self.__client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__endpoints: Endpoints = endpoints
        self.__token_values: Optional[TokenValues] = None
        self.__expiration_time: Optional[dt.datetime] = None

    def __refresh_token(self) -> None:
        client_id, client_secret = self.__client_id, self.__client_secret
        client_id_and_secret_encoded = base64.urlsafe_b64encode(
            f'{client_id}:{client_secret}'.encode('ascii')).decode('utf-8')
        headers = {'Authorization': f'Basic {client_id_and_secret_encoded}'}

        try:
            response = requests.post(url=self.__endpoints.token, headers=headers,
                                     auth=(client_id, client_secret))
            response.raise_for_status()

            parsed_response = json.loads(response.content.decode('utf-8'))
            token_values = TokenValues(parsed_response['access_token'],
                                       parsed_response['token_type'])
            expiration_time = dt.datetime.now() + dt.timedelta(
                seconds=int(parsed_response['expires_in']))

            self.__token_values, self.__expiration_time = token_values, expiration_time

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e) from None

    def __is_expired(self) -> bool:
        return (self.__expiration_time - dt.datetime.now()).total_seconds() <= \
               self.TOKEN_REFRESH_BEFORE_SECONDS

    def get(self) -> TokenValues:
        if not self.__expiration_time or self.__is_expired():
            self.__refresh_token()
        return self.__token_values
