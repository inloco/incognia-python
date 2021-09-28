import base64
import datetime as dt
import json
from typing import Tuple, Final

import requests

from endpoints import Endpoints
from exceptions import IncogniaException

AUTHORIZATION_HEADER: Final[str] = 'Authorization'
OK_STATUS_CODE: Final[int] = 200
TOKEN_REFRESH_BEFORE_SECONDS: Final[int] = 10


class TokenValues:
    def __init__(self, access_token: str, token_type: str):
        self.access_token, self.token_type = access_token, token_type


class TokenManager:
    @staticmethod
    def __get_new_token(client_id: str, client_secret: str) -> Tuple[TokenValues, dt.datetime]:
        client_id_secret = client_id + ':' + client_secret
        base64url = base64.urlsafe_b64encode(client_id_secret.encode('ascii')).decode('utf-8')
        headers = {AUTHORIZATION_HEADER: 'Basic ' + base64url}

        response = requests.post(url=Endpoints.TOKEN, headers=headers, auth=(client_id, client_secret))

        if response.status_code == OK_STATUS_CODE:
            parsed_response = json.loads(response.content.decode('utf-8'))
            value = TokenValues(parsed_response['access_token'], parsed_response['token_type'])
            expiration_time = dt.datetime.now() + dt.timedelta(seconds=int(parsed_response['expires_in']))
            return value, expiration_time
        else:
            raise IncogniaException('network error: {}'.format(response.status_code))

    def __init__(self, client_id: str, client_secret: str):
        self.__client_id, self.__client_secret = client_id, client_secret
        self.__token_values, self.__expiration_time = self.__get_new_token(client_id, client_secret)

    def __is_expired(self) -> bool:
        return (self.__expiration_time - dt.datetime.now()).total_seconds() <= TOKEN_REFRESH_BEFORE_SECONDS

    def get(self) -> TokenValues:
        if self.__is_expired():
            self.__token_values, self.__expiration_time = self.__get_new_token(self.__client_id, self.__client_secret)
        return self.__token_values
