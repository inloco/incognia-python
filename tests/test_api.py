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
    INVALID_INSTALLATION_ID: Final[str] = 'INVALID_INSTALLATION_ID'
    ACCOUNT_ID: Final[str] = 'ANY_ACCOUNT_ID'
    INVALID_ACCOUNT_ID: Final[str] = 'INVALID_ACCOUNT_ID'
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
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400
    VALID_EVENT_FEEDBACK_TYPE: Final[str] = 'valid_event_feedback_type'
    INVALID_EVENT_FEEDBACK_TYPE: Final[str] = 'invalid_event_feedback_type'
    TIMESTAMP: Final[dt.datetime] = dt.datetime.utcfromtimestamp(0)
    REGISTER_VALID_FEEDBACK_DATA: Final[bytes] = encode({
        'event': f'{VALID_EVENT_FEEDBACK_TYPE}',
        'timestamp': 0
    })
    REGISTER_INVALID_FEEDBACK_DATA: Final[bytes] = encode({
        'event': f'{INVALID_EVENT_FEEDBACK_TYPE}',
        'timestamp': 0
    })
    REGISTER_VALID_PAYMENT_DATA: Final[bytes] = encode({
        'type': 'payment',
        'installation_id': f'{INSTALLATION_ID}',
        'account_id': f'{ACCOUNT_ID}'
    })
    REGISTER_INVALID_PAYMENT_DATA: Final[bytes] = encode({
        'type': 'payment',
        'installation_id': f'{INVALID_INSTALLATION_ID}',
        'account_id': f'{INVALID_ACCOUNT_ID}'
    })
    REGISTER_VALID_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'installation_id': f'{INSTALLATION_ID}',
        'account_id': f'{ACCOUNT_ID}'
    })
    REGISTER_INVALID_LOGIN_DATA: Final[bytes] = encode({
        'type': 'login',
        'installation_id': f'{INVALID_INSTALLATION_ID}',
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

    @patch.object(BaseRequest, 'get')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_get_signup_assessment_when_signup_id_is_valid_should_return_a_valid_dict(
            self, mock_token_manager_get: Mock, mock_base_request_get: Mock):
        mock_base_request_get.configure_mock(return_value=self.JSON_RESPONSE)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        request_response = api.get_signup_assessment(signup_id=self.SIGNUP_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_get.assert_called_with(f'{Endpoints.SIGNUPS}/{self.SIGNUP_ID}',
                                                 headers=self.AUTH_HEADER)

        self.assertEqual(request_response, self.JSON_RESPONSE)

    @patch.object(BaseRequest, 'get')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_get_signup_assessment_when_signup_id_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_get: Mock):
        mock_base_request_get.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.get_signup_assessment, self.SIGNUP_ID)

        mock_token_manager_get.assert_called()
        mock_base_request_get.assert_called_with(f'{Endpoints.SIGNUPS}/{self.SIGNUP_ID}',
                                                 headers=self.AUTH_HEADER)

    @patch.object(BaseRequest, 'get')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_get_signup_assessment_when_signup_id_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_get: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.get_signup_assessment, '')

        mock_token_manager_get.assert_not_called()
        mock_base_request_get.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_required_fields_are_valid_should_work(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        api.register_feedback(self.VALID_EVENT_FEEDBACK_TYPE, self.TIMESTAMP)

        mock_token_manager_get.assert_called()
        mock_base_request_post.assert_called_with(Endpoints.FEEDBACKS,
                                                  headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                                  data=self.REGISTER_VALID_FEEDBACK_DATA)

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_event_is_empty_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_feedback, event='', timestamp=self.TIMESTAMP)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_timestamp_is_none_should_raise_an_IncogniaError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_feedback,
                          event=self.VALID_EVENT_FEEDBACK_TYPE, timestamp=None)

        mock_token_manager_get.assert_not_called()
        mock_base_request_post.assert_not_called()

    @patch.object(BaseRequest, 'post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_token_manager_get: Mock, mock_base_request_post: Mock):
        mock_base_request_post.configure_mock(side_effect=IncogniaHTTPError)

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_feedback,
                          event=self.INVALID_EVENT_FEEDBACK_TYPE,
                          timestamp=self.TIMESTAMP)

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

        request_response = api.register_payment(self.INSTALLATION_ID, self.ACCOUNT_ID)

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

        request_response = api.register_login(self.INSTALLATION_ID, self.ACCOUNT_ID)

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
