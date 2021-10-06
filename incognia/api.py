import datetime as dt
import json
from typing import Optional, Literal

import requests

from .endpoints import Endpoints
from .exceptions import IncogniaHTTPError, IncogniaError
from .feedback_events import FeedbackEvents, FeedbackEventType  # type: ignore
from .models import Coordinates, StructuredAddress
from .token_manager import TokenManager


class IncogniaAPI:
    def __init__(self, access_token: str, token_type: str, region: Literal['br', 'us'] = 'us'):
        self.__endpoints = Endpoints(region)
        self.__token_manager = TokenManager(access_token, token_type, self.__endpoints)

    def register_new_signup(self,
                            installation_id: str,
                            address_line: Optional[str] = None,
                            structured_address: Optional[StructuredAddress] = None,
                            address_coordinates: Optional[Coordinates] = None) -> dict:
        if not installation_id:
            raise IncogniaError('installation_id is required.')

        try:
            access_token, token_type = self.__token_manager.get()
            headers = {
                'Content-type': 'application/json',
                'Authorization': f'{token_type} {access_token}'
            }
            body = {
                'installation_id': installation_id,
                'address_line': address_line,
                'structured_address': structured_address,
                'address_coordinates': address_coordinates
            }
            data = json.dumps({k: v for (k, v) in body.items() if v is not None},
                              ensure_ascii=False).encode('utf-8')
            response = requests.post(self.__endpoints.signups, headers=headers, data=data)
            response.raise_for_status()

            return json.loads(response.content.decode('utf-8'))

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e) from None

    def get_signup_assessment(self, signup_id: str) -> dict:
        if not signup_id:
            raise IncogniaError('signup_id is required.')

        try:
            access_token, token_type = self.__token_manager.get()
            headers = {
                'Authorization': f'{token_type} {access_token}',
            }
            response = requests.get(f'{self.__endpoints.signups}/{signup_id}', headers=headers)
            response.raise_for_status()

            return json.loads(response.content.decode('utf-8'))

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e) from None

    def send_feedback(self,
                      event: FeedbackEventType,
                      timestamp: dt.datetime,
                      external_id: Optional[str] = None,
                      login_id: Optional[str] = None,
                      payment_id: Optional[str] = None,
                      signup_id: Optional[str] = None,
                      account_id: Optional[str] = None,
                      installation_id: Optional[str] = None) -> None:
        if not event:
            raise IncogniaError('event is required.')
        if not timestamp:
            raise IncogniaError('timestamp is required.')

        try:
            access_token, token_type = self.__token_manager.get()
            headers = {
                'Content-type': 'application/json',
                'Authorization': f'{token_type} {access_token}'
            }

            def total_milliseconds_since_epoch(t: dt.datetime) -> int:
                return int((t - dt.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)

            body = {
                'event': event,
                'timestamp': total_milliseconds_since_epoch(timestamp),
                'external_id': external_id,
                'login_id': login_id,
                'payment_id': payment_id,
                'signup_id': signup_id,
                'account_id': account_id,
                'installation_id': installation_id
            }
            data = json.dumps({k: v for (k, v) in body.items() if v is not None})
            response = requests.post(self.__endpoints.feedbacks, headers=headers, data=data)
            response.raise_for_status()

        except requests.HTTPError as e:
            raise IncogniaHTTPError(e)
