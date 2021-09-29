from typing import Final


class Endpoints:
    BASE: Final[str] = 'https://api.us.incognia.com'

    TOKEN: Final[str] = f'{BASE}/api/v1/token'
    SIGNUPS: Final[str] = f'{BASE}/api/v2/onboarding/signups'
    TRANSACTIONS: Final[str] = f'{BASE}/api/v2/authentication/transactions'
