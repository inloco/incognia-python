import datetime as dt
from typing import Optional, List

from .datetime_util import total_milliseconds_since_epoch, has_timezone
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
                            account_id: Optional[str] = None,
                            request_token: Optional[str] = None) -> dict:
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
                'account_id': account_id,
                'request_token': request_token
            }
            data = encode(body)
            return self.__request.post(Endpoints.SIGNUPS, headers=headers, data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_feedback(self,
                          event: str,
                          timestamp: dt.datetime = None,
                          external_id: Optional[str] = None,
                          login_id: Optional[str] = None,
                          payment_id: Optional[str] = None,
                          signup_id: Optional[str] = None,
                          account_id: Optional[str] = None,
                          installation_id: Optional[str] = None,
                          session_token: Optional[str] = None,
                          request_token: Optional[str] = None,
                          occurred_at: dt.datetime = None,
                          expires_at: dt.datetime = None) -> None:
        if not event:
            raise IncogniaError('event is required.')
        if timestamp is not None and not has_timezone(timestamp):
            raise IncogniaError('timestamp must have timezone')
        if occurred_at is not None and not has_timezone(occurred_at):
            raise IncogniaError('occurred_at must have timezone')
        if expires_at is not None and not has_timezone(expires_at):
            raise IncogniaError('expires_at must have timezone')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            body = {
                'event': event,
                'external_id': external_id,
                'login_id': login_id,
                'payment_id': payment_id,
                'signup_id': signup_id,
                'account_id': account_id,
                'installation_id': installation_id,
                'session_token': session_token,
                'request_token': request_token
            }
            if timestamp is not None:
                body['timestamp'] = total_milliseconds_since_epoch(timestamp)
            if occurred_at is not None:
                body['occurred_at'] = occurred_at.isoformat()
            if expires_at is not None:
                body['expires_at'] = expires_at.isoformat()
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
                         evaluate: Optional[bool] = None,
                         policy_id: Optional[str] = None,
                         request_token: Optional[str] = None) -> dict:
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
                'payment_methods': payment_methods,
                'policy_id': policy_id,
                'request_token': request_token
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
                       evaluate: Optional[bool] = None,
                       policy_id: Optional[str] = None,
                       request_token: Optional[str] = None) -> dict:
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
                'external_id': external_id,
                'policy_id': policy_id,
                'request_token': request_token
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_web_login(self,
                           session_token: str,
                           account_id: str,
                           external_id: Optional[str] = None,
                           evaluate: Optional[bool] = None,
                           policy_id: Optional[str] = None,
                           request_token: Optional[str] = None) -> dict:
        if not session_token:
            raise IncogniaError('session_token is required.')
        if not account_id:
            raise IncogniaError('account_id is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            params = None if evaluate is None else {'eval': evaluate}
            body = {
                'type': 'login',
                'session_token': session_token,
                'account_id': account_id,
                'external_id': external_id,
                'policy_id': policy_id,
                'request_token': request_token
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None
