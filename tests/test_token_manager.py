import datetime as dt
from typing import Final
from unittest import TestCase
from unittest.mock import Mock, patch

from exceptions import IncogniaHTTPError
from incognia_api.token_manager import TokenManager, TokenValues


class TestTokenManager(TestCase):
    CLIENT_ID: Final[str] = 'ANY_ID'
    CLIENT_SECRET: Final[str] = 'ANY_SECRET'
    TOKEN_VALUES: Final[TokenValues] = TokenValues('ACCESS_TOKEN', 'TOKEN_TYPE')
    EXPIRED_TOKEN_VALUES: Final[TokenValues] = TokenValues('EXPIRED_ACCESS_TOKEN', 'EXPIRED_TOKEN_TYPE')
    EXPIRATION_TIME: Final[dt.datetime] = dt.datetime.fromisoformat('2000-01-01')

    @patch.object(TokenManager, '_TokenManager__refresh_token')
    def test_get_whenCredentialsAreValid_shouldReturnAValidToken(self, mock_refresh_token: Mock):
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)

        def refresh_token_side_effect():
            token_manager._TokenManager__token_values = self.TOKEN_VALUES

        mock_refresh_token.configure_mock(side_effect=refresh_token_side_effect)

        token_values = token_manager.get()
        mock_refresh_token.assert_called()
        self.assertEqual(token_values, self.TOKEN_VALUES)

    @patch.object(TokenManager, '_TokenManager__refresh_token')
    def test_get_whenCredentialsAreInvalid_shouldRaiseAnIncogniaHTTPError(self, mock_refresh_token: Mock):
        mock_refresh_token.configure_mock(side_effect=IncogniaHTTPError())
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)
        self.assertRaises(IncogniaHTTPError, token_manager.get)
        mock_refresh_token.assert_called()

    @patch.object(TokenManager, '_TokenManager__is_expired')
    @patch.object(TokenManager, '_TokenManager__refresh_token')
    def test_get_whenTokenIsExpired_shouldReturnANewValidToken(self, mock_refresh_token: Mock, mock_is_expired: Mock):
        token_manager = TokenManager(self.CLIENT_ID, self.CLIENT_SECRET)

        def refresh_token_expired_side_effect():
            token_manager._TokenManager__token_values = self.EXPIRED_TOKEN_VALUES
            token_manager._TokenManager__expiration_time = self.EXPIRATION_TIME

        mock_refresh_token.configure_mock(side_effect=refresh_token_expired_side_effect)

        expired_token_values = token_manager.get()
        mock_refresh_token.assert_called()

        def refresh_token_new_side_effect():
            token_manager._TokenManager__token_values = self.TOKEN_VALUES
            token_manager._TokenManager__expiration_time = self.EXPIRATION_TIME + dt.timedelta(seconds=5)

        mock_is_expired.configure_mock(return_value=True)
        mock_refresh_token.reset_mock()
        mock_refresh_token.configure_mock(side_effect=refresh_token_new_side_effect)

        new_token_values = token_manager.get()
        mock_refresh_token.assert_called()
        mock_is_expired.assert_called()
        self.assertNotEqual(expired_token_values, new_token_values)
