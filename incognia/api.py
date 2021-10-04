import json
from typing import Optional

import requests

from .endpoints import Endpoints
from .exceptions import IncogniaHTTPError, IncogniaError
from .models import Coordinates, StructuredAddress
from .token_manager import TokenManager


class IncogniaAPI:
    def __init__(self, access_token: str, token_type: str):
        self.__token_manager = TokenManager(access_token, token_type)

    def register_new_signup(self,
                            installation_id: str,
                            address_line: Optional[str] = None,
                            structured_address: Optional[StructuredAddress] = None,
                            coordinates: Optional[Coordinates] = None) -> dict:
        try:
            assert installation_id, 'installation_id is required.'

            access_token, token_type = self.__token_manager.get()
            headers = {
                'Content-type': 'application/json',
                'Authorization': f'{token_type} {access_token}'
            }
            body = {
                'installation_id': installation_id,
                'address_line': address_line,
                'structured_address': structured_address,
                'coordinates': coordinates
            }
            data = json.dumps({k: v for (k, v) in body.items() if v is not None})
            response = requests.post(Endpoints.SIGNUPS, headers=headers, data=data)
            response.raise_for_status()

            return json.loads(response.content.decode('utf-8'))

        except AssertionError as e:
            raise IncogniaError(e)

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e)

    def get_latest_signup_assessment(self, signup_id: str) -> dict:
        try:
            assert signup_id, 'id is required.'

            access_token, token_type = self.__token_manager.get()
            headers = {
                'Authorization': f'{token_type} {access_token}',
            }
            response = requests.get(f'{Endpoints.SIGNUPS}/{signup_id}', headers=headers)
            response.raise_for_status()

            return json.loads(response.content.decode('utf-8'))
        except AssertionError as e:
            raise IncogniaError(e)
