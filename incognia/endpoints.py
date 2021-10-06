from typing import Final, Literal


class Endpoints:
    def __init__(self, region: Literal['br', 'us']):
        self.base: Final[str] = f'https://api.{region}.incognia.com'

        self.token: Final[str] = f'{self.base}/api/v1/token'
        self.signups: Final[str] = f'{self.base}/api/v2/onboarding/signups'
        self.feedbacks: Final[str] = f'{self.base}/api/v2/feedbacks'
        self.transactions: Final[str] = f'{self.base}/api/v2/authentication/transactions'
