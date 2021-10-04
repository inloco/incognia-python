import base64
from typing import Final
from unittest import TestCase
from unittest.mock import Mock, patch

import requests

from incognia.endpoints import Endpoints
from incognia.exceptions import IncogniaHTTPError
from incognia.token_manager import TokenManager, TokenValues


class TestTokenManager(TestCase):
    CLIENT_ID: Final[str] = 'ANY_ID'
    CLIENT_SECRET: Final[str] = 'ANY_SECRET'
    TOKEN_VALUES: Final[TokenValues] = TokenValues('ACCESS_TOKEN', 'TOKEN_TYPE')
    JSON_POST_RESPONSE: Final[ascii] = b'{ "access_token": "ACCESS_TOKEN",' \
                                       b' "token_type": "TOKEN_TYPE", "expires_in": 900 }'
    SHORT_EXPIRATION_TOKEN_VALUES: Final[TokenValues] = TokenValues('S_E_ACCESS_TOKEN',
                                                                    'S_E_TOKEN_TYPE')
    SHORT_EXPIRATION_JSON_POST_RESPONSE: Final[ascii] = b'{ "access_token": "S_E_ACCESS_TOKEN",' \
                                                        b' "token_type": "S_E_TOKEN_TYPE",' \
                                                        b' "expires_in": 5 }'
    CLIENT_ID_AND_SECRET_ENCODED: Final[str] = base64.urlsafe_b64encode(
        f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii')).decode('utf-8')
    HEADERS: Final[dict] = {'Authorization': f'Basic {CLIENT_ID_AND_SECRET_ENCODED}'}
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400

    @patch('requests.post')
    def test_get_when_credentials_are_valid_should_return_a_valid_token(self,
                                                                        mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_POST_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        token_values = token_manager.get()
        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))
        self.assertEqual(token_values, self.TOKEN_VALUES)

    @patch('requests.post')
    def test_get_when_credentials_are_invalid_should_raise_an_IncogniaHTTPError(self,
                                                                                mock_requests_post:
                                                                                Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response.status_code = self.CLIENT_ERROR_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        self.assertRaises(IncogniaHTTPError, token_manager.get)
        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))

    @patch('requests.post')
    def test_get_when_token_is_expired_should_return_a_new_valid_token(self,
                                                                       mock_requests_post:
                                                                       Mock):
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)

        def get_first_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content = self.SHORT_EXPIRATION_JSON_POST_RESPONSE
            response.status_code = self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_first_mocked_response())

        first_token_values = token_manager.get()

        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))

        def get_second_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_POST_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_post.reset_mock()
        mock_requests_post.configure_mock(return_value=get_second_mocked_response())

        second_token_values = token_manager.get()

        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))

        self.assertEqual(first_token_values, self.SHORT_EXPIRATION_TOKEN_VALUES)
        self.assertEqual(second_token_values, self.TOKEN_VALUES)
