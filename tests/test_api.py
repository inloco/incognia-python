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
    SESSION_TOKEN: Final[str] = 'ANY_SESSION_TOKEN'
    REQUEST_TOKEN: Final[str] = 'ANY_REQUEST_TOKEN'
    INVALID_INSTALLATION_ID: Final[str] = 'INVALID_INSTALLATION_ID'
    INVALID_SESSION_TOKEN: Final[str] = 'INVALID_SESSION_TOKEN'
    ACCOUNT_ID: Final[str] = 'ANY_ACCOUNT_ID'
    INVALID_ACCOUNT_ID: Final[str] = 'INVALID_ACCOUNT_ID'
    ADDRESS_LINE: Final[str] = 'ANY_ADDRESS_LINE'
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
        'installation_id': f'{INSTALLATION_ID}'
    })
    FULL_REGISTER_SIGNUP_DATA: Final[bytes] = encode({
        'installation_id': f'{INSTALLATION_ID}',
        'address_line': f'{ADDRESS_LINE}',
        'structured_address': STRUCTURED_ADDRESS,
        'address_coordinates': ADDRESS_COORDINATES,
        'external_id': f'{EXTERNAL_ID}',
        'policy_id': f'{POLICY_ID}',
        'account_id': f'{ACCOUNT_ID}',
        'request_token': f'{REQUEST_TOKEN}'
    })
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400
    VALID_EVENT_FEEDBACK_TYPE: Final[str] = 'valid_event_feedback_type'
    INVALID_EVENT_FEEDBACK_TYPE: Final[str] = 'invalid_event_feedback_type'
    TIMESTAMP: Final[dt.datetime] = dt.datetime.now(dt.timezone.utc)
    TIMESTAMP_WITHOUT_TIMEZONE: Final[dt.datetime] = dt.datetime.now()
    LOGIN_ID: Final[str] = 'ANY_LOGIN_ID'
    PAYMENT_ID: Final[str] = 'ANY_PAYMENT_ID'
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
        'session_token': f'{SESSION_TOKEN}',
        'request_token': f'{REQUEST_TOKEN}',
        'timestamp': int((
            TIMESTAMP - dt.datetime.fromtimestamp(0, dt.timezone.utc)).total_seconds() * 1000.0),
        'occurred_at': TIMESTAMP.isoformat(),
        'expires_at': TIMESTAMP.isoformat(),
    })
    REGISTER_INVALID_FEEDBACK_DATA: Final[bytes] = encode({
        'event': f'{INVALID_EVENT_FEEDBACK_TYPE}'
    })
    REGISTER_VALID_PAYMENT_DATA: Final[bytes] = encode({
        'type': 'payment',
        'installation_id': f'{INSTALLATION_ID}',
        'account_id': f'{ACCOUNT_ID}',
        'policy_id': f'{POLICY_ID}',
        'request_token': f'{REQUEST_TOKEN}',
    })
    REGISTER_INVALID_PAYMENT_DATA: Final[bytes] = encode({
        'type': 'payment',
        'installation_id': f'{INVALID_INSTALLATION_ID}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    REGISTER_VALID_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'installation_id': f'{INSTALLATION_ID}',
        'account_id': f'{ACCOUNT_ID}',
        'policy_id': f'{POLICY_ID}',
        'request_token': f'{REQUEST_TOKEN}'
    })
    REGISTER_VALID_WEB_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'session_token': f'{SESSION_TOKEN}',
        'account_id': f'{ACCOUNT_ID}',
        'policy_id': f'{POLICY_ID}',
        'request_token': f'{REQUEST_TOKEN}'
    })
    REGISTER_INVALID_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'installation_id': f'{INVALID_INSTALLATION_ID}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    REGISTER_INVALID_WEB_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'session_token': f'{INVALID_SESSION_TOKEN}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    DEFAULT_PARAMS: Final[None] = None

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_valid_should_return_a_valid_dict(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        response = api.register_new_signup(installation_id=self.INSTALLATION_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_SIGNUP_DATA)

        self.assertEqual(response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_valid_should_return_full_valid_dict_(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        response = api.register_new_signup(installation_id=self.INSTALLATION_ID,
                                           address_line=self.ADDRESS_LINE,
                                           structured_address=self.STRUCTURED_ADDRESS,
                                           address_coordinates=self.ADDRESS_COORDINATES,
                                           external_id=self.EXTERNAL_ID,
                                           policy_id=self.POLICY_ID,
                                           account_id=self.ACCOUNT_ID,
                                           request_token=self.REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.FULL_REGISTER_SIGNUP_DATA)

        self.assertEqual(response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_new_signup, self.INSTALLATION_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.SIGNUPS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_SIGNUP_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get')
    def test_register_new_signup_when_installation_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_new_signup, '')

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

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
                              timestamp=self.TIMESTAMP,
                              occurred_at=self.TIMESTAMP,
                              expires_at=self.TIMESTAMP,
                              external_id=self.EXTERNAL_ID,
                              login_id=self.LOGIN_ID,
                              payment_id=self.PAYMENT_ID,
                              signup_id=self.SIGNUP_ID,
                              account_id=self.ACCOUNT_ID,
                              installation_id=self.INSTALLATION_ID,
                              session_token=self.SESSION_TOKEN,
                              request_token=self.REQUEST_TOKEN)

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
    def test_register_feedback_when_timestamp_does_not_have_timezone_should_raise_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError,
                          api.register_feedback,
                          event=self.VALID_EVENT_FEEDBACK_TYPE,
                          timestamp=self.TIMESTAMP_WITHOUT_TIMEZONE)

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
    def test_register_feedback_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_feedback,
                          event=self.INVALID_EVENT_FEEDBACK_TYPE)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.FEEDBACKS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_INVALID_FEEDBACK_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_required_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        request_response = api.register_payment(self.INSTALLATION_ID,
                                                self.ACCOUNT_ID,
                                                policy_id=self.POLICY_ID,
                                                request_token=self.REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_PAYMENT_DATA)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_installation_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_payment, installation_id='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_account_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_payment, installation_id=self.INSTALLATION_ID,
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
                          installation_id=self.INVALID_INSTALLATION_ID,
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

        request_response = api.register_login(self.INSTALLATION_ID,
                                              self.ACCOUNT_ID,
                                              policy_id=self.POLICY_ID,
                                              request_token=self.REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_LOGIN_DATA)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_installation_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_login, installation_id='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_account_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_login, installation_id=self.INSTALLATION_ID,
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
                          installation_id=self.INVALID_INSTALLATION_ID,
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

        request_response = api.register_web_login(self.SESSION_TOKEN,
                                                  self.ACCOUNT_ID,
                                                  policy_id=self.POLICY_ID,
                                                  request_token=self.REQUEST_TOKEN)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_VALID_WEB_LOGIN_DATA)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_session_token_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_web_login, session_token='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_web_login_when_account_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_web_login, session_token=self.SESSION_TOKEN,
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
                          session_token=self.INVALID_SESSION_TOKEN,
                          account_id=self.INVALID_ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.TRANSACTIONS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  params=self.DEFAULT_PARAMS,
                                                  data=self.REGISTER_INVALID_WEB_LOGIN_DATA)
