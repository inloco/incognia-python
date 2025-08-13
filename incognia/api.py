import datetime as dt
from typing import Optional, List

from .datetime_util import has_timezone, datetime_valid
from .endpoints import Endpoints
from .exceptions import IncogniaHTTPError, IncogniaError
from .json_util import encode
from .models import (
    Coordinates,
    StructuredAddress,
    TransactionAddress,
    PaymentValue,
    PaymentMethod,
    Location,
    Coupon,
    PersonID,
)
from .singleton import Singleton
from .token_manager import TokenManager
from .base_request import BaseRequest, JSON_CONTENT_HEADER


class IncogniaAPI(metaclass=Singleton):
    def __init__(self, client_id: str, client_secret: str):
        self.__token_manager = TokenManager(client_id, client_secret)
        self.__request = BaseRequest()

    def __get_authorization_header(self) -> dict:
        access_token, token_type = self.__token_manager.get()
        return {'Authorization': f'{token_type} {access_token}'}

    def register_new_signup(self,
                            request_token: Optional[str],
                            address_line: Optional[str] = None,
                            structured_address: Optional[StructuredAddress] = None,
                            address_coordinates: Optional[Coordinates] = None,
                            external_id: Optional[str] = None,
                            policy_id: Optional[str] = None,
                            account_id: Optional[str] = None,
                            device_os: Optional[str] = None,
                            app_version: Optional[str] = None,
                            person_id: Optional[PersonID] = None,
                            custom_properties: Optional[dict] = None) -> dict:
        if not request_token:
            raise IncogniaError('request_token is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            body = {
                'request_token': request_token,
                'address_line': address_line,
                'structured_address': structured_address,
                'address_coordinates': address_coordinates,
                'external_id': external_id,
                'policy_id': policy_id,
                'account_id': account_id,
                'device_os': device_os.lower() if device_os is not None else None,
                'app_version': app_version,
                'person_id': person_id,
                'custom_properties': custom_properties
            }
            data = encode(body)
            return self.__request.post(Endpoints.SIGNUPS, headers=headers, data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_new_web_signup(self,
                                request_token: Optional[str],
                                policy_id: Optional[str] = None,
                                account_id: Optional[str] = None,
                                custom_properties: Optional[dict] = None,
                                person_id: Optional[PersonID] = None) -> dict:
        if not request_token:
            raise IncogniaError('request_token is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            body = {
                'request_token': request_token,
                'policy_id': policy_id,
                'account_id': account_id,
                'custom_properties': custom_properties,
                'person_id': person_id,
            }
            data = encode(body)
            return self.__request.post(Endpoints.SIGNUPS, headers=headers, data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_feedback(self,
                          event: str,
                          external_id: Optional[str] = None,
                          login_id: Optional[str] = None,
                          payment_id: Optional[str] = None,
                          signup_id: Optional[str] = None,
                          account_id: Optional[str] = None,
                          installation_id: Optional[str] = None,
                          request_token: Optional[str] = None,
                          occurred_at: dt.datetime = None,
                          expires_at: dt.datetime = None,
                          person_id: Optional[PersonID] = None) -> None:
        if not event:
            raise IncogniaError('event is required.')
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
                'request_token': request_token,
                'person_id': person_id,
            }
            if occurred_at is not None:
                body['occurred_at'] = occurred_at.isoformat()
            if expires_at is not None:
                body['expires_at'] = expires_at.isoformat()
            data = encode(body)
            return self.__request.post(Endpoints.FEEDBACKS, headers=headers, data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_payment(self,
                         request_token: str,
                         account_id: str,
                         external_id: Optional[str] = None,
                         location: Optional[Location] = None,
                         addresses: Optional[List[TransactionAddress]] = None,
                         payment_value: Optional[PaymentValue] = None,
                         payment_methods: Optional[List[PaymentMethod]] = None,
                         evaluate: Optional[bool] = None,
                         policy_id: Optional[str] = None,
                         custom_properties: Optional[dict] = None,
                         coupon: Optional[Coupon] = None,
                         device_os: Optional[str] = None,
                         app_version: Optional[str] = None,
                         store_id: Optional[str] = None,
                         person_id: Optional[PersonID] = None) -> dict:
        if not request_token:
            raise IncogniaError('request_token is required.')
        if not account_id:
            raise IncogniaError('account_id is required.')
        if location is not None:
            if location['latitude'] is None:
                raise IncogniaError('location argument requires "latitude" field')
            if location['longitude'] is None:
                raise IncogniaError('location argument requires "longitude" field')
            if (
                location['collected_at'] is not None
                and not datetime_valid(location['collected_at'])
            ):
                raise IncogniaError('location["collected_at"] must conform to ISO-8601 format')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            params = None if evaluate is None else {'eval': evaluate}
            body = {
                'type': 'payment',
                'request_token': request_token,
                'account_id': account_id,
                'external_id': external_id,
                'location': location,
                'addresses': addresses,
                'payment_value': payment_value,
                'payment_methods': payment_methods,
                'policy_id': policy_id,
                'custom_properties': custom_properties,
                'coupon': coupon,
                'device_os': device_os.lower() if device_os is not None else None,
                'app_version': app_version,
                'store_id': store_id,
                'person_id': person_id,
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_login(self,
                       request_token: str,
                       account_id: str,
                       location: Optional[Location] = None,
                       external_id: Optional[str] = None,
                       evaluate: Optional[bool] = None,
                       policy_id: Optional[str] = None,
                       device_os: Optional[str] = None,
                       app_version: Optional[str] = None,
                       person_id: Optional[PersonID] = None) -> dict:
        if not request_token:
            raise IncogniaError('request_token is required.')
        if not account_id:
            raise IncogniaError('account_id is required.')
        if location is not None:
            if location['latitude'] is None:
                raise IncogniaError('location argument requires "latitude" field')
            if location['longitude'] is None:
                raise IncogniaError('location argument requires "longitude" field')
            if (
                location['collected_at'] is not None
                and not datetime_valid(location['collected_at'])
            ):
                raise IncogniaError('location["collected_at"] must conform to ISO-8601 format')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            params = None if evaluate is None else {'eval': evaluate}
            body = {
                'type': 'login',
                'request_token': request_token,
                'account_id': account_id,
                'location': location,
                'external_id': external_id,
                'policy_id': policy_id,
                'device_os': device_os.lower() if device_os is not None else None,
                'app_version': app_version,
                'person_id': person_id,
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None

    def register_web_login(self,
                           request_token: str,
                           account_id: str,
                           external_id: Optional[str] = None,
                           evaluate: Optional[bool] = None,
                           policy_id: Optional[str] = None,
                           custom_properties: Optional[dict] = None,
                           person_id: Optional[PersonID] = None) -> dict:
        if not request_token:
            raise IncogniaError('request_token is required.')
        if not account_id:
            raise IncogniaError('account_id is required.')

        try:
            headers = self.__get_authorization_header()
            headers.update(JSON_CONTENT_HEADER)
            params = None if evaluate is None else {'eval': evaluate}
            body = {
                'type': 'login',
                'request_token': request_token,
                'account_id': account_id,
                'external_id': external_id,
                'policy_id': policy_id,
                'custom_properties': custom_properties,
                'person_id': person_id,
            }
            data = encode(body)
            return self.__request.post(Endpoints.TRANSACTIONS, headers=headers, params=params,
                                       data=data)

        except IncogniaHTTPError as e:
            raise IncogniaHTTPError(e) from None
