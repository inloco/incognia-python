import base64
from typing import Final
from unittest import TestCase
from unittest.mock import Mock, patch

from incognia.base_request import BaseRequest
from incognia.endpoints import Endpoints
from incognia.exceptions import IncogniaHTTPError
from incognia.token_manager import TokenManager, TokenValues


class TestTokenManager(TestCase):
    CLIENT_ID: Final[str] = 'ANY_ID'
    CLIENT_SECRET: Final[str] = 'ANY_SECRET'
    TOKEN_VALUES: Final[TokenValues] = TokenValues('ACCESS_TOKEN', 'TOKEN_TYPE')
    JSON_POST_RESPONSE: Final[dict] = {
        'access_token': 'ACCESS_TOKEN',
        'token_type': 'TOKEN_TYPE',
        'expires_in': 900
    }
    SHORT_EXPIRATION_TOKEN_VALUES: Final[TokenValues] = \
        TokenValues('S_E_ACCESS_TOKEN', 'S_E_TOKEN_TYPE')
    SHORT_EXPIRATION_JSON_POST_RESPONSE: Final[dict] = {
        'access_token': 'S_E_ACCESS_TOKEN',
        'token_type': 'S_E_TOKEN_TYPE',
        'expires_in': 5
    }
    CLIENT_ID_AND_SECRET_ENCODED: Final[str] = base64.urlsafe_b64encode(
        f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii')).decode('utf-8')
    HEADERS: Final[dict] = {'Authorization': f'Basic {CLIENT_ID_AND_SECRET_ENCODED}'}
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400

    @patch.object(BaseRequest, 'post')
    def test_get_when_credentials_are_valid_should_return_a_valid_token(self,
                                                                        mock_requests_post: Mock):
        mock_requests_post.configure_mock(return_value=self.JSON_POST_RESPONSE)

        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        token_values = token_manager.get()
        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))
        self.assertEqual(token_values, self.TOKEN_VALUES)

    @patch.object(BaseRequest, 'post')
    def test_get_when_credentials_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_requests_post: Mock):
        mock_requests_post.configure_mock(side_effect=IncogniaHTTPError)

        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        self.assertRaises(IncogniaHTTPError, token_manager.get)
        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))

    @patch.object(BaseRequest, 'post')
    def test_get_when_token_is_expired_should_return_a_new_valid_token(self,
                                                                       mock_requests_post:
                                                                       Mock):
        mock_requests_post.configure_mock(return_value=self.SHORT_EXPIRATION_JSON_POST_RESPONSE)

        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        first_token_values = token_manager.get()

        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))

        mock_requests_post.reset_mock()
        mock_requests_post.configure_mock(return_value=self.JSON_POST_RESPONSE)

        second_token_values = token_manager.get()

        mock_requests_post.assert_called_with(url=Endpoints.TOKEN, headers=self.HEADERS,
                                              auth=(self.CLIENT_ID, self.CLIENT_SECRET))

        self.assertEqual(first_token_values, self.SHORT_EXPIRATION_TOKEN_VALUES)
        self.assertEqual(second_token_values, self.TOKEN_VALUES)
