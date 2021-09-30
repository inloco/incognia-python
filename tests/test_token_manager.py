import datetime as dt
from typing import Final
from unittest import TestCase
from unittest.mock import Mock, patch

from incognia_api.exceptions import IncogniaHTTPError
from incognia_api.token_manager import TokenManager, TokenValues


class TestTokenManager(TestCase):
    CLIENT_ID: Final[str] = 'ANY_ID'
    CLIENT_SECRET: Final[str] = 'ANY_SECRET'
    TOKEN_VALUES: Final[TokenValues] = TokenValues('ACCESS_TOKEN', 'TOKEN_TYPE')
    SECOND_TOKEN_VALUES: Final[TokenValues] = TokenValues('SECOND_ACCESS_TOKEN', 'SECOND_TOKEN_TYPE')
    EXPIRATION_TIME: Final[dt.datetime] = dt.datetime.fromisoformat('2000-01-01')

    @patch.object(TokenManager, 'refresh_token')
    def test_get_when_credentials_are_valid_should_return_a_valid_token(self, mock_refresh_token: Mock):
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)

        def refresh_token_side_effect():
            token_manager._TokenManager__token_values = self.TOKEN_VALUES

        mock_refresh_token.configure_mock(side_effect=refresh_token_side_effect)

        token_values = token_manager.get()
        mock_refresh_token.assert_called()
        self.assertEqual(token_values, self.TOKEN_VALUES)

    @patch.object(TokenManager, 'refresh_token')
    def test_get_when_credentials_are_invalid_should_raise_an_IncogniaHTTPError(self, mock_refresh_token: Mock):
        mock_refresh_token.configure_mock(side_effect=IncogniaHTTPError())
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        self.assertRaises(IncogniaHTTPError, token_manager.get)
        mock_refresh_token.assert_called()

    @patch.object(TokenManager, 'is_expired')
    @patch.object(TokenManager, 'refresh_token')
    def test_get_when_token_is_expired_should_return_a_new_valid_token(self, mock_refresh_token: Mock,
                                                                       mock_is_expired: Mock):
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)

        def refresh_token_first_side_effect():
            token_manager._TokenManager__token_values = self.TOKEN_VALUES
            token_manager._TokenManager__expiration_time = self.EXPIRATION_TIME

        mock_refresh_token.configure_mock(side_effect=refresh_token_first_side_effect)

        first_token_values = token_manager.get()
        mock_refresh_token.assert_called()

        def refresh_token_second_side_effect():
            token_manager._TokenManager__token_values = self.SECOND_TOKEN_VALUES
            token_manager._TokenManager__expiration_time = self.EXPIRATION_TIME + dt.timedelta(seconds=5)

        mock_is_expired.configure_mock(return_value=True)
        mock_refresh_token.reset_mock()
        mock_refresh_token.configure_mock(side_effect=refresh_token_second_side_effect)

        second_token_values = token_manager.get()
        mock_refresh_token.assert_called()
        mock_is_expired.assert_called()

        self.assertEqual(first_token_values, self.TOKEN_VALUES)
        self.assertEqual(second_token_values, self.SECOND_TOKEN_VALUES)
