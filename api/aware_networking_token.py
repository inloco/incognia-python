import base64
import datetime as dt
import json
from typing import Tuple
from urllib.parse import urljoin

import requests

from exceptions import IncogniaException

URL = 'https://api.us.incognia.com'
TOKEN_PATH: str = 'api/v1/token'
AUTHORIZATION_HEADER: str = 'Authorization'
OK_STATUS_CODE: int = 200
TOKEN_REFRESH_BEFORE_SECONDS: int = 10


class Value:
    access_token: str
    token_type: str

    def __init__(self, access_token: str, token_type: str):
        self.access_token, self.token_type = access_token, token_type


class AwareNetworkingToken:
    __client_id: str
    __client_secret: str

    __value: Value
    __expiration_time: dt.datetime

    @staticmethod
    def __get_new_token(client_id: str, client_secret: str) -> Tuple[Value, dt.datetime]:
        client_id_secret = client_id + ':' + client_secret
        base64url = base64.urlsafe_b64encode(client_id_secret.encode('ascii')).decode('utf-8')
        headers = {AUTHORIZATION_HEADER: 'Basic ' + base64url}

        response = requests.post(url=urljoin(URL, TOKEN_PATH), headers=headers, auth=(client_id, client_secret))

        if response.status_code == OK_STATUS_CODE:
            parsed_response = json.loads(response.content.decode('utf-8'))
            value = Value(parsed_response['access_token'], parsed_response['token_type'])
            expiration_time = dt.datetime.now() + dt.timedelta(seconds=int(parsed_response['expires_in']))
            return value, expiration_time
        else:
            raise IncogniaException('network error: {}'.format(response.status_code))

    def __init__(self, client_id: str, client_secret: str):
        self.__client_id, self.__client_secret = client_id, client_secret
        self.__value, self.__expiration_time = self.__get_new_token(client_id, client_secret)

    def __is_expired(self) -> bool:
        return (self.__expiration_time - dt.datetime.now()).total_seconds() <= TOKEN_REFRESH_BEFORE_SECONDS

    def get(self) -> Value:
        if self.__is_expired():
            self.__value, self.__expiration_time = self.__get_new_token(self.__client_id, self.__client_secret)
        return self.__value
