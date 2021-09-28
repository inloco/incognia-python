from typing import Final
from urllib.parse import urljoin


class Endpoints:
    BASE: Final[str] = 'https://api.us.incognia.com'

    TOKEN: Final[str] = urljoin(BASE, 'api/v1/token')
    SIGNUPS: Final[str] = urljoin(BASE, 'api/v2/onboarding/signups')
    TRANSACTIONS: Final[str] = urljoin(BASE, 'api/v2/authentication/transactions')
