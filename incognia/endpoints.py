from typing import Final


class Endpoints:
    BASE: Final[str] = 'https://api.incognia.com'

    TOKEN: Final[str] = f'{BASE}/api/v2/token'
    SIGNUPS: Final[str] = f'{BASE}/api/v2/onboarding/signups'
    FEEDBACKS: Final[str] = f'{BASE}/api/v2/feedbacks'
    TRANSACTIONS: Final[str] = f'{BASE}/api/v2/authentication/transactions'
