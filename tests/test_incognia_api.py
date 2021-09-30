import json
from typing import Final
from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from incognia_api.endpoints import Endpoints
from incognia_api.exceptions import IncogniaHTTPError, IncogniaError
from incognia_api.incognia_api import IncogniaAPI
from incognia_api.token_manager import TokenValues, TokenManager


class TestIncogniaAPI(TestCase):
    CLIENT_ID: Final[str] = 'ANY_ID'
    CLIENT_SECRET: Final[str] = 'ANY_SECRET'
    INSTALLATION_ID: Final[str] = 'ANY_ID'
    TOKEN_VALUES: Final[TokenValues] = TokenValues('ACCESS_TOKEN', 'TOKEN_TYPE')
    JSON_POST_RESPONSE: Final[ascii] = b'{ "id": "signup_identifier", "request_id": "request_identifier",' \
                                       b' "risk_assessment": "unknown_risk", "evidence": [] }'
    HEADERS: Final[dict] = {
        'Content-type': 'application/json',
        'Authorization': f'{TOKEN_VALUES.token_type} {TOKEN_VALUES.access_token}'
    }
    DATA: Final[str] = f'{{"installation_id": "{INSTALLATION_ID}"}}'
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_valid_should_return_a_valid_dict(self,
                                                                                          mock_token_manager_get: Mock,
                                                                                          mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = self.JSON_POST_RESPONSE, self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)
        request_response = api.register_new_signup(installation_id=self.INSTALLATION_ID)

        mock_token_manager_get.assert_called()
        mock_requests_post.assert_called_with(Endpoints.SIGNUPS, headers=self.HEADERS, data=self.DATA)

        self.assertEqual(request_response, json.loads(self.JSON_POST_RESPONSE.decode('utf-8')))

    @patch('requests.post')
    @patch.object(TokenManager, 'get', return_value=TOKEN_VALUES)
    def test_register_new_signup_when_installation_id_is_invalid_should_raise_an_Exception(self,
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
        mock_requests_post.assert_called()

    @patch('requests.post')
    @patch.object(TokenManager, 'get')
    def test_register_new_signup_when_installation_id_is_empty_should_raise_an_Exception(self,
                                                                                         mock_token_manager_get: Mock,
                                                                                         mock_requests_post: Mock):
        api = IncogniaAPI(self.CLIENT_ID, self.CLIENT_SECRET)

        self.assertRaises(IncogniaError, api.register_new_signup, '')

        mock_token_manager_get.assert_not_called()
        mock_requests_post.assert_not_called()
