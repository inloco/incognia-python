import datetime as dt
from typing import Final
from unittest import TestCase
from unittest.mock import patch, Mock

from incognia.api import IncogniaAPI
from incognia.base_request import BaseRequest
from incognia.endpoints import Endpoints
from incognia.exceptions import IncogniaHTTPError, IncogniaError
from incognia.json_util import encode
from incognia.token_manager import TokenValues, TokenManager


class TestIncogniaAPI(TestCase):
    CLIENT_ID: Final[str] = 'ANY_ID'
    CLIENT_SECRET: Final[str] = 'ANY_SECRET'
    INSTALLATION_ID: Final[str] = 'ANY_INSTALLATION_ID'
    REQUEST_TOKEN: Final[str] = 'ANY_REQUEST_TOKEN'
    INVALID_REQUEST_TOKEN: Final[str] = 'INVALID_REQUEST_TOKEN'
    ACCOUNT_ID: Final[str] = 'ANY_ACCOUNT_ID'
    INVALID_ACCOUNT_ID: Final[str] = 'INVALID_ACCOUNT_ID'
    ADDRESS_LINE: Final[str] = 'ANY_ADDRESS_LINE'
    DEVICE_OS: Final[str] = 'ANY_DEVICE_OS'
    APP_VERSION: Final[str] = 'ANY_APP_VERSION'
    PERSON_ID: Final[dict] = {
        'type': 'cpf',
        'value': '12345678901'
    }
    STRUCTURED_ADDRESS: Final[dict] = {
        'locale': 'ANY_LOCALE',
        'country_name': 'ANY_COUNTRY_NAME',
        'country_code': 'ANY_COUNTRY_CODE',
        'state': 'ANY_STATE',
        'city': 'ANY_CITY',
        'borough': 'ANY_BOROUGH',
        'neighborhood': 'ANY_NEIGHBORHOOD',
        'street': 'ANY_STREET',
        'number': 'ANY_NUMBER',
        'complements': 'ANY_COMPLEMENTS',
        'postal_code': 'ANY_POSTAL_CODE'
    }
    ADDRESS_COORDINATES: Final[dict] = {
        'lat': 1.69,
        'lng': 2.345
    }
    EXTERNAL_ID: Final[str] = 'ANY_EXTERNAL_ID'
    POLICY_ID: Final[str] = 'ANY_POLICY_ID'
    SIGNUP_ID: Final[str] = 'ANY_SIGNUP_ID'
    TOKEN_VALUES: Final[TokenValues] = TokenValues('ACCESS_TOKEN', 'TOKEN_TYPE')
    JSON_RESPONSE: Final[dict] = {
        'id': 'signup_identifier',
        'request_id': 'request_identifier',
        'risk_assessment': 'unknown_risk',
        'evidence': []
    }
    AUTH_HEADER: Final[dict] = {
        'Authorization': f'{TOKEN_VALUES.token_type} {TOKEN_VALUES.access_token}'
    }
    AUTH_AND_JSON_CONTENT_HEADERS: Final[dict] = {
        'Authorization': f'{TOKEN_VALUES.token_type} {TOKEN_VALUES.access_token}',
        'Content-Type': 'application/json'
    }
    REGISTER_SIGNUP_DATA: Final[bytes] = encode({
        'request_token': f'{REQUEST_TOKEN}'
    })
    REGISTER_INVALID_SIGNUP_DATA: Final[bytes] = encode({
        'request_token': f'{INVALID_REQUEST_TOKEN}'
    })
    CUSTOM_PROPERTIES: Final[dict] = {
        'float_field': 6.092,
        'string_field': "the next generation of identity",
    }
    FULL_REGISTER_SIGNUP_DATA: Final[bytes] = encode({
        'request_token': f'{REQUEST_TOKEN}',
        'address_line': f'{ADDRESS_LINE}',
        'structured_address': STRUCTURED_ADDRESS,
        'address_coordinates': ADDRESS_COORDINATES,
        'external_id': f'{EXTERNAL_ID}',
        'policy_id': f'{POLICY_ID}',
        'account_id': f'{ACCOUNT_ID}',
        'device_os': f'{DEVICE_OS.lower()}',
        'app_version': f'{APP_VERSION}',
        'person_id': PERSON_ID,
        'custom_properties': CUSTOM_PROPERTIES
    })
    REGISTER_WEB_SIGNUP_DATA: Final[bytes] = encode({
        'request_token': f'{REQUEST_TOKEN}'
    })
    REGISTER_INVALID_WEB_SIGNUP_DATA: Final[bytes] = encode({
        'request_token': f'{INVALID_REQUEST_TOKEN}'
    })
    FULL_REGISTER_WEB_SIGNUP_DATA: Final[bytes] = encode({
        'request_token': f'{REQUEST_TOKEN}',
        'policy_id': f'{POLICY_ID}',
        'account_id': f'{ACCOUNT_ID}',
        'custom_properties': CUSTOM_PROPERTIES,
        'person_id': PERSON_ID
    })
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400
    VALID_EVENT_FEEDBACK_TYPE: Final[str] = 'valid_event_feedback_type'
    TIMESTAMP: Final[dt.datetime] = dt.datetime.now(dt.timezone.utc)
    TIMESTAMP_WITHOUT_TIMEZONE: Final[dt.datetime] = dt.datetime.now()
    LOGIN_ID: Final[str] = 'ANY_LOGIN_ID'
    PAYMENT_ID: Final[str] = 'ANY_PAYMENT_ID'
    STORE_ID: Final[str] = 'ANY_STORE_ID'
    COUPON: Final[dict] = {
        "type": "percent_off",
        "value": 2.5,
        "max_discount": 50.0,
        "id": "COUPON_ID",
        "name": "COUPON_NAME"
    }
    TRANSACTION_ADDRESS: Final[dict] = {
        "type": "billing",
        "structured_address": STRUCTURED_ADDRESS,
        "address_coordinates": ADDRESS_COORDINATES
    }
    PAYMENT_VALUE: Final[dict] = {
        'value': 12.34,
        'currency': 'BRL'
    }
    CARD_INFO: Final[dict] = {
        'bin': '0000000000',
        'last_four_digits': '0000',
        'expiry_year': '2029',
        'expiry_month': '04'
    }
    PAYMENT_METHOD: Final[dict] = {
        'type': 'credit_card',
        'credit_card_info': CARD_INFO
    }
    LOCATION: Final[dict] = {
        'latitude': 0.000,
        'longitude': 89.000,
        'collected_at': TIMESTAMP.isoformat()
    }
    INVALID_LOCATION_EMPTY_LATITUDE: Final[dict] = {
        'latitude': None,
        'longitude': 13.123,
        'collected_at': TIMESTAMP.isoformat()
    }
    INVALID_LOCATION_EMPTY_LONGITUDE: Final[dict] = {
        'latitude': 0.000,
        'longitude': None,
        'collected_at': TIMESTAMP.isoformat()
    }
    INVALID_LOCATION_WRONG_TIMESTAMP: Final[dict] = {
        'latitude': 0.000,
        'longitude': 13.123,
        'collected_at': "12:04 14/10/2024"
    }
    REGISTER_VALID_FEEDBACK_DATA: Final[bytes] = encode({
        'event': f'{VALID_EVENT_FEEDBACK_TYPE}'
    })
    REGISTER_VALID_FEEDBACK_DATA_FULL: Final[bytes] = encode({
        'event': f'{VALID_EVENT_FEEDBACK_TYPE}',
        'external_id': f'{EXTERNAL_ID}',
        'login_id': f'{LOGIN_ID}',
        'payment_id': f'{PAYMENT_ID}',
        'signup_id': f'{SIGNUP_ID}',
        'account_id': f'{ACCOUNT_ID}',
        'installation_id': f'{INSTALLATION_ID}',
        'request_token': f'{REQUEST_TOKEN}',
        'person_id': PERSON_ID,
        'occurred_at': TIMESTAMP.isoformat(),
        'expires_at': TIMESTAMP.isoformat()
    })
    REGISTER_VALID_PAYMENT_DATA: Final[bytes] = encode({
        'type': 'payment',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'policy_id': f'{POLICY_ID}',
    })
    REGISTER_VALID_PAYMENT_DATA_ALL_FIELDS: Final[bytes] = encode({
        'type': 'payment',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'external_id': f'{EXTERNAL_ID}',
        'location': LOCATION,
        'addresses': [TRANSACTION_ADDRESS],
        'payment_value': PAYMENT_VALUE,
        'payment_methods': PAYMENT_METHOD,
        'policy_id': f'{POLICY_ID}',
        'custom_properties': CUSTOM_PROPERTIES,
        'coupon': COUPON,
        'device_os': f'{DEVICE_OS.lower()}',
        'app_version': f'{APP_VERSION}',
        'store_id': f'{STORE_ID}',
        'person_id': PERSON_ID
    })
    REGISTER_VALID_PAYMENT_DATA_WITH_LOCATION: Final[bytes] = encode({
        'type': 'payment',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'location': LOCATION,
        'policy_id': f'{POLICY_ID}',
    })
    REGISTER_INVALID_PAYMENT_DATA: Final[bytes] = encode({
        'type': 'payment',
        'request_token': f'{INVALID_REQUEST_TOKEN}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    REGISTER_VALID_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'policy_id': f'{POLICY_ID}'
    })
    REGISTER_VALID_LOGIN_DATA_WITH_LOCATION: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'location': LOCATION,
        'policy_id': f'{POLICY_ID}'
    })
    REGISTER_VALID_LOGIN_DATA_ALL_FIELDS: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'location': LOCATION,
        'external_id': f'{EXTERNAL_ID}',
        'policy_id': f'{POLICY_ID}',
        'device_os': f'{DEVICE_OS.lower()}',
        'app_version': f'{APP_VERSION}',
        'person_id': PERSON_ID
    })
    REGISTER_VALID_WEB_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'policy_id': f'{POLICY_ID}'
    })
    REGISTER_VALID_WEB_LOGIN_ALL_FIELDS: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{REQUEST_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'external_id': f'{EXTERNAL_ID}',
        'policy_id': f'{POLICY_ID}',
        'custom_properties': CUSTOM_PROPERTIES,
        'person_id': PERSON_ID
    })
    REGISTER_INVALID_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{INVALID_REQUEST_TOKEN}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    REGISTER_INVALID_WEB_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'request_token': f'{INVALID_REQUEST_TOKEN}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    DEFAULT_PARAMS: Final[None] = None

    def test_metaclass_singleton_should_always_return_the_same_instance(self):
        api1 = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        api2 = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertEqual(api1, api2)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_request_token_is_valid_should_return_a_valid_dict(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        response = api.register_new_signup(request_token=self.REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_SIGNUP_DATA)

        self.assertEqual(response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_web_signup_when_request_token_is_valid_should_return_a_valid_dict(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        response = api.register_new_web_signup(request_token=self.REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_WEB_SIGNUP_DATA)

        self.assertEqual(response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_request_token_is_valid_should_return_full_valid_dict_(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        response = api.register_new_signup(address_line=self.ADDRESS_LINE,
                                           structured_address=self.STRUCTURED_ADDRESS,
                                           address_coordinates=self.ADDRESS_COORDINATES,
                                           external_id=self.EXTERNAL_ID,
                                           policy_id=self.POLICY_ID,
                                           account_id=self.ACCOUNT_ID,
                                           request_token=self.REQUEST_TOKEN,
                                           device_os=self.DEVICE_OS,
                                           app_version=self.APP_VERSION,
                                           person_id=self.PERSON_ID,
                                           custom_properties=self.CUSTOM_PROPERTIES)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.FULL_REGISTER_SIGNUP_DATA)

        self.assertEqual(response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_web_signup_when_request_token_is_valid_should_return_full_valid_dict_(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        response = api.register_new_web_signup(request_token=self.REQUEST_TOKEN,
                                               policy_id=self.POLICY_ID,
                                               account_id=self.ACCOUNT_ID,
                                               custom_properties=self.CUSTOM_PROPERTIES,
                                               person_id=self.PERSON_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.FULL_REGISTER_WEB_SIGNUP_DATA)

        self.assertEqual(response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_request_token_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_new_signup, request_token='')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_web_signup_when_request_token_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_new_web_signup, request_token='')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_request_token_is_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_new_signup, self.INVALID_REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_INVALID_SIGNUP_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_web_signup_if_request_token_is_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_new_web_signup,
                          self.INVALID_REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_INVALID_WEB_SIGNUP_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_required_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        api.register_feedback(self.VALID_EVENT_FEEDBACK_TYPE)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.FEEDBACKS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_VALID_FEEDBACK_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_all_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        api.register_feedback(self.VALID_EVENT_FEEDBACK_TYPE,
                              occurred_at=self.TIMESTAMP,
                              expires_at=self.TIMESTAMP,
                              external_id=self.EXTERNAL_ID,
                              login_id=self.LOGIN_ID,
                              payment_id=self.PAYMENT_ID,
                              signup_id=self.SIGNUP_ID,
                              account_id=self.ACCOUNT_ID,
                              installation_id=self.INSTALLATION_ID,
                              request_token=self.REQUEST_TOKEN,
                              person_id=self.PERSON_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.FEEDBACKS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_VALID_FEEDBACK_DATA_FULL)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_event_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_feedback, event='')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_occurred_at_does_not_have_timezone_should_raise_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError,
                          api.register_feedback,
                          event=self.VALID_EVENT_FEEDBACK_TYPE,
                          occurred_at=self.TIMESTAMP_WITHOUT_TIMEZONE)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_expires_at_does_not_have_timezone_should_raise_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError,
                          api.register_feedback,
                          event=self.VALID_EVENT_FEEDBACK_TYPE,
                          expires_at=self.TIMESTAMP_WITHOUT_TIMEZONE)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_required_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_payment(self.REQUEST_TOKEN,
                                                self.ACCOUNT_ID,
                                                policy_id=self.POLICY_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_PAYMENT_DATA)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_with_all_fields_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_payment(
            request_token=self.REQUEST_TOKEN,
            account_id=self.ACCOUNT_ID,
            external_id=self.EXTERNAL_ID,
            location=self.LOCATION,
            addresses=[self.TRANSACTION_ADDRESS],
            payment_value=self.PAYMENT_VALUE,
            payment_methods=self.PAYMENT_METHOD,
            policy_id=self.POLICY_ID,
            custom_properties=self.CUSTOM_PROPERTIES,
            coupon=self.COUPON,
            device_os=self.DEVICE_OS,
            app_version=self.APP_VERSION,
            store_id=self.STORE_ID,
            person_id=self.PERSON_ID
        )

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_PAYMENT_DATA_ALL_FIELDS)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_request_token_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_payment,
                          request_token='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_account_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_payment,
                          request_token=self.REQUEST_TOKEN,
                          account_id='')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_payment,
                          request_token=self.INVALID_REQUEST_TOKEN,
                          account_id=self.INVALID_ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_INVALID_PAYMENT_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_required_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_login(self.REQUEST_TOKEN,
                                              self.ACCOUNT_ID,
                                              policy_id=self.POLICY_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_LOGIN_DATA)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_request_token_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_login,
                          request_token='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_account_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_login,
                          request_token=self.REQUEST_TOKEN,
                          account_id='')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_login,
                          request_token=self.INVALID_REQUEST_TOKEN,
                          account_id=self.INVALID_ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_INVALID_LOGIN_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_required_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_web_login(self.REQUEST_TOKEN,
                                                  self.ACCOUNT_ID,
                                                  policy_id=self.POLICY_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_WEB_LOGIN_DATA)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_all_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_web_login(self.REQUEST_TOKEN,
                                                  self.ACCOUNT_ID,
                                                  external_id=self.EXTERNAL_ID,
                                                  policy_id=self.POLICY_ID,
                                                  custom_properties=self.CUSTOM_PROPERTIES,
                                                  person_id=self.PERSON_ID)
        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_WEB_LOGIN_ALL_FIELDS)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_request_token_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_web_login,
                          request_token='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_account_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_web_login,
                          request_token=self.REQUEST_TOKEN,
                          account_id='')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_web_login,
                          account_id=self.INVALID_ACCOUNT_ID,
                          request_token=self.INVALID_REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_INVALID_WEB_LOGIN_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_with_valid_location_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_login(self.REQUEST_TOKEN,
                                              self.ACCOUNT_ID,
                                              location=self.LOCATION,
                                              policy_id=self.POLICY_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_LOGIN_DATA_WITH_LOCATION)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_with_all_fields_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_login(self.REQUEST_TOKEN,
                                              self.ACCOUNT_ID,
                                              location=self.LOCATION,
                                              external_id=self.EXTERNAL_ID,
                                              policy_id=self.POLICY_ID,
                                              device_os=self.DEVICE_OS,
                                              app_version=self.APP_VERSION,
                                              person_id=self.PERSON_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_LOGIN_DATA_ALL_FIELDS)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_with_location_and_empty_latitude_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(
            IncogniaError, api.register_login,
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.INVALID_LOCATION_EMPTY_LATITUDE,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_with_location_and_empty_longitude_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(
            IncogniaError,
            api.register_login,
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.INVALID_LOCATION_EMPTY_LONGITUDE,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_with_location_and_wrong_timestamp_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(
            IncogniaError,
            api.register_login,
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.INVALID_LOCATION_WRONG_TIMESTAMP,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_with_valid_location_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_payment(
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.LOCATION,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(
            Endpoints.TRANSACTIONS,
            headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
            params=self.DEFAULT_PARAMS,
            data=self.REGISTER_VALID_PAYMENT_DATA_WITH_LOCATION,
        )

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_with_location_and_empty_latitude_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(
            IncogniaError, api.register_payment,
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.INVALID_LOCATION_EMPTY_LATITUDE,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_with_location_and_empty_longitude_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(
            IncogniaError, api.register_payment,
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.INVALID_LOCATION_EMPTY_LONGITUDE,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_with_location_and_wrong_timestamp_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):

        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(
            IncogniaError,
            api.register_payment,
            self.REQUEST_TOKEN,
            self.ACCOUNT_ID,
            location=self.INVALID_LOCATION_WRONG_TIMESTAMP,
            policy_id=self.POLICY_ID,
        )

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()
