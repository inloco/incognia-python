from typing import Final
from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from incognia.base_request import BaseRequest, USER_AGENT_HEADER
from incognia.exceptions import IncogniaHTTPError
from incognia.json_util import encode


class TestBaseRequest(TestCase):
    URL: Final[str] = 'https://some-valid-link.com'
    JSON_RESPONSE: Final[dict] = {
        'first-key': 'first-value',
        'second-key': 'second-value'
    }
    OK_STATUS_CODE: Final[int] = 200
    CLIENT_ERROR_CODE: Final[int] = 400

    @patch('requests.post')
    def test_post_when_parameters_are_valid_should_return_a_valid_dict(
            self, mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = encode(
                self.JSON_RESPONSE), self.OK_STATUS_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        base_request = BaseRequest()
        result = base_request.post(url=self.URL)
        mock_requests_post.assert_called_with(url=self.URL, headers=USER_AGENT_HEADER, data=None,
                                              params=None,
                                              timeout=base_request.timeout(), auth=None)
        self.assertEqual(result, self.JSON_RESPONSE)

    @patch('requests.post')
    def test_post_when_parameters_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_requests_post: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = encode(
                self.JSON_RESPONSE), self.CLIENT_ERROR_CODE
            return response

        mock_requests_post.configure_mock(return_value=get_mocked_response())

        base_request = BaseRequest()
        self.assertRaises(IncogniaHTTPError, base_request.post, url=self.URL)
        mock_requests_post.assert_called_with(url=self.URL, headers=USER_AGENT_HEADER, data=None,
                                              params=None,
                                              timeout=base_request.timeout(), auth=None)

    @patch('requests.get')
    def test_get_when_parameters_are_valid_should_return_a_valid_dict(self,
                                                                      mock_requests_get: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = encode(
                self.JSON_RESPONSE), self.OK_STATUS_CODE
            return response

        mock_requests_get.configure_mock(return_value=get_mocked_response())

        base_request = BaseRequest()
        result = base_request.get(url=self.URL)
        mock_requests_get.assert_called_with(url=self.URL, headers=USER_AGENT_HEADER, data=None,
                                             timeout=base_request.timeout())
        self.assertEqual(result, self.JSON_RESPONSE)

    @patch('requests.get')
    def test_get_when_parameters_are_invalid_should_raise_an_IncogniaHTTPError(
            self, mock_requests_get: Mock):
        def get_mocked_response() -> requests.Response:
            response = requests.Response()
            response._content, response.status_code = encode(
                self.JSON_RESPONSE), self.CLIENT_ERROR_CODE
            return response

        mock_requests_get.configure_mock(return_value=get_mocked_response())

        base_request = BaseRequest()
        self.assertRaises(IncogniaHTTPError, base_request.get, url=self.URL)
        mock_requests_get.assert_called_with(url=self.URL, headers=USER_AGENT_HEADER, data=None,
                                             timeout=base_request.timeout())
