import datetime as dt
from typing import Optional, List

from .datetime_util import total_milliseconds_since_epoch
from .endpoints import Endpoints
from .exceptions import IncogniaHTTPError, IncogniaError
from .json_util import encode
from .models import Coordinates, StructuredAddress, TransactionAddress, PaymentValue, PaymentMethod
from .token_manager import TokenManager
from .base_request import BaseRequest, JSON_CONTENT_HEADER


class IncogniaAPI:
    def __init__(self, client_id: str, client_secret: str):
        self.__token_manager = TokenManager(client_id, client_secret)
        self.__request = BaseRequest()

    def __get_authorization_header(self) -> dict:
        access_token, token_type = self.__token_manager.get()
        return {'Authorization': f'{token_type} {access_token}'}

    def register_new_signup(self,
                            installation_id: str,
                            address_line: Optional[str] = None,
                            structured_address: Optional[StructuredAddress] = None,
                            address_coordinates: Optional[Coordinates] = None,
                            external_id: Optional[str] = None,
                            policy_id: Optional[str] = None,
                            account_id: Optional[str] = None) -> dict:
        if not installation_id:
            raise IncogniaError('installation_id is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            body = {
                'installation_id': installation_id,
                'address_line': address_line,
                'structured_address': structured_address,
                'address_coordinates': address_coordinates,
                'external_id': external_id,
                'policy_id': policy_id,
                'account_id': account_id
            }
            data = encode(body)
            return self.__request.post(Endpoints.SIGNUPS, headers=headers, data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def get_signup_assessment(self, signup_id: str) -> dict:
        if not signup_id:
            raise IncogniaError('signup_id is required.')

        try:
            headers = self.__get_authorization_header()
            return self.__request.get(f'{Endpoints.SIGNUPS}/{signup_id}', headers=headers)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_feedback(self,
                          event: str,
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
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
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
            data = encode(body)
            return self.__request.post(Endpoints.FEEDBACKS, headers=headers, data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_payment(self,
                         installation_id: str,
                         account_id: str,
                         external_id: Optional[str] = None,
                         addresses: Optional[List[TransactionAddress]] = None,
                         payment_value: Optional[PaymentValue] = None,
                         payment_methods: Optional[List[PaymentMethod]] = None,
                         evaluate: Optional[bool] = None) -> dict:
        if not installation_id:
            raise IncogniaError('installation_id is required.')
        if not account_id:
            raise IncogniaError('account_id is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            params = None if evaluate is None else {'eval': evaluate}
            body = {
                'type': 'payment',
                'installation_id': installation_id,
                'account_id': account_id,
                'external_id': external_id,
                'addresses': addresses,
                'payment_value': payment_value,
                'payment_methods': payment_methods
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_login(self,
                       installation_id: str,
                       account_id: str,
                       external_id: Optional[str] = None,
                       evaluate: Optional[bool] = None) -> dict:
        if not installation_id:
            raise IncogniaError('installation_id is required.')
        if not account_id:
            raise IncogniaError('account_id is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            params = None if evaluate is None else {'eval': evaluate}
            body = {
                'type': 'login',
                'installation_id': installation_id,
                'account_id': account_id,
                'external_id': external_id
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None
