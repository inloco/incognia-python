import datetime as dt
import json
from typing import Final
from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from incognia.api import IncogniaAPI
from incognia.endpoints import Endpoints
from incognia.exceptions import IncogniaHTTPError, IncogniaError
from incognia.feedback_events import FeedbackEventType
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
    JSON_RESPONSE: Final[ascii] = b'{ "id": "signup_identifier",' \
                                  b' "request_id": "request_identifier",' \
                                  b' "risk_assessment": "unknown_risk", "evidence": [] }'
    AUTH_HEADER: Final[dict] = {
        'Authorization': f'{TOKEN_VALUES.token_type} {TOKEN_VALUES.access_token}'
    }
    AUTH_AND_JSON_CONTENT_HEADERS: Final[dict] = {
        'Content-type': 'application/json',
        'Authorization': f'{TOKEN_VALUES.token_type} {TOKEN_VALUES.access_token}'
    }
    REGISTER_SIGNUP_DATA: Final[ascii] = f'{{"installation_id": "{INSTALLATION_ID}"}}' \
        .encode('utf-8')
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400
    VALID_EVENT_FEEDBACK_TYPE: Final[FeedbackEventType] = 'valid_event_feedback_type'
    INVALID_EVENT_FEEDBACK_TYPE: Final[FeedbackEventType] = 'invalid_event_feedback_type'
    TIMESTAMP: Final[dt.datetime] = dt.datetime.utcfromtimestamp(0)
    REGISTER_VALID_FEEDBACK_DATA: Final[ascii] = f'{{"event": "{VALID_EVENT_FEEDBACK_TYPE}",' \
                                                 f' "timestamp": 0}}'.encode('utf-8')
    REGISTER_INVALID_FEEDBACK_DATA: Final[ascii] = f'{{"event": "{INVALID_EVENT_FEEDBACK_TYPE}",' \
                                                   f' "timestamp": 0}}'.encode('utf-8')
    REGISTER_VALID_PAYMENT_DATA: Final[ascii] = '{"type": "payment",' \
                                                f' "installation_id": "{INSTALLATION_ID}",' \
                                                f' "account_id": "{ACCOUNT_ID}"}}'.encode('utf-8')
    REGISTER_INVALID_PAYMENT_DATA: Final[ascii] = \
        '{"type": "payment",' \
        f' "installation_id": "{INVALID_INSTALLATION_ID}",' \
        f' "account_id": "{INVALID_ACCOUNT_ID}"}}'.encode('utf-8')
    REGISTER_VALID_LOGIN_DATA: Final[ascii] = '{"type": "login",' \
                                              f' "installation_id": "{INSTALLATION_ID}",' \
                                              f' "account_id": "{ACCOUNT_ID}"}}'.encode('utf-8')
    REGISTER_INVALID_LOGIN_DATA: Final[ascii] = \
        '{"type": "login",' \
        f' "installation_id": "{INVALID_INSTALLATION_ID}",' \
        f' "account_id": "{INVALID_ACCOUNT_ID}"}}'.encode('utf-8')
    ENDPOINTS: Final[Endpoints] = Endpoints('us')

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_valid_should_return_a_valid_dict(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        request_response = api.register_new_signup(installation_id=self.INSTALLATION_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.signups,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_SIGNUP_DATA)

        self.assertEqual(request_response, json.loads(self.JSON_RESPONSE.decode('utf-8')))

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_invalid_should_raise_an_IncogniaHTTPError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response.status_code = self.CLIENT_ERROR_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_new_signup, self.INSTALLATION_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.signups,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_SIGNUP_DATA)

    @patch('requests.post')
    @patch.object(TokenManager, 'get')
    def test_register_new_signup_when_installation_id_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_new_signup, '')

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.get')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_get_signup_assessment_when_signup_id_is_valid_should_return_a_valid_dict(
            self,
            mock_token_manager_get: Mock,
            mock_requests_get: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_get.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        request_response = api.get_signup_assessment(signup_id=self.SIGNUP_ID)

        mock_token_manager_get.assert_called()
        mock_requests_get.assert_called_with(f'{self.ENDPOINTS.signups}/{self.SIGNUP_ID}',
                                             headers=self.AUTH_HEADER)

        self.assertEqual(request_response, json.loads(self.JSON_RESPONSE.decode('utf-8')))

    @patch('requests.get')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_get_signup_assessment_when_signup_id_invalid_should_raise_an_IncogniaHTTPError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_get: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response.status_code = self.CLIENT_ERROR_CODE
            return response

        mock_requests_get.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.get_signup_assessment, self.SIGNUP_ID)

        mock_token_manager_get.assert_called()
        mock_requests_get.assert_called_with(f'{self.ENDPOINTS.signups}/{self.SIGNUP_ID}',
                                             headers=self.AUTH_HEADER)

    @patch('requests.get')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_get_signup_assessment_when_signup_id_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_get: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.get_signup_assessment, '')

        mock_token_manager_get.assert_not_called()
        mock_requests_get.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_required_fields_are_valid_should_work(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        api.register_feedback(self.VALID_EVENT_FEEDBACK_TYPE, self.TIMESTAMP)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.feedbacks,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_VALID_FEEDBACK_DATA)

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_event_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_feedback, event='', timestamp=self.TIMESTAMP)

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_timestamp_is_none_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_feedback,
                          event=self.VALID_EVENT_FEEDBACK_TYPE,
                          timestamp=None)

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_feedback_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response.status_code = self.CLIENT_ERROR_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_feedback,
                          event=self.INVALID_EVENT_FEEDBACK_TYPE,
                          timestamp=self.TIMESTAMP)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.feedbacks,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_INVALID_FEEDBACK_DATA)

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_required_fields_are_valid_should_work(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        api.register_payment(self.INSTALLATION_ID, self.ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.transactions,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_VALID_PAYMENT_DATA)

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_installation_id_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_payment, installation_id='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_account_id_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_payment, installation_id=self.INSTALLATION_ID,
                          account_id='')

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_payment_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response.status_code = self.CLIENT_ERROR_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_payment,
                          installation_id=self.INVALID_INSTALLATION_ID,
                          account_id=self.INVALID_ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.transactions,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_INVALID_PAYMENT_DATA)

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_required_fields_are_valid_should_work(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        api.register_login(self.INSTALLATION_ID, self.ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.transactions,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_VALID_LOGIN_DATA)

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_installation_id_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_login, installation_id='',
                          account_id=self.ACCOUNT_ID)

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_account_id_is_empty_should_raise_an_IncogniaError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_login, installation_id=self.INSTALLATION_ID,
                          account_id='')

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_login_when_required_fields_are_invalid_should_raise_an_IncogniaHTTPError(
            self,
            mock_token_manager_get: Mock,
            mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response.status_code = self.CLIENT_ERROR_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaHTTPError, api.register_login,
                          installation_id=self.INVALID_INSTALLATION_ID,
                          account_id=self.INVALID_ACCOUNT_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(self.ENDPOINTS.transactions,
                                              headers=self.AUTH_AND_JSON_CONTENT_HEADERS,
                                              data=self.REGISTER_INVALID_LOGIN_DATA)
