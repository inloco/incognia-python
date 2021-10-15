from typing import TypedDict, Literal


class Coordinates(TypedDict):
    lat: float
    lng: float


class StructuredAddress(TypedDict, total=False):
    locale: str
    country_name: str
    country_code: str
    state: str
    city: str
    borough: str
    neighborhood: str
    street: str
    number: str
    complements: str
    postal_code: str


class TransactionAddress(TypedDict, total=False):
    type: Literal['shipping', 'billing', 'home']
    structured_address: StructuredAddress
    address_coordinates: Coordinates


class PaymentValue(TypedDict):
    amount: float
    currency: str


class CardInfo(TypedDict, total=False):
    bin: str
    last_four_digits: str
    expiry_year: str
    expiry_month: str


class PaymentMethod(TypedDict, total=False):
    type: Literal['credit', 'debit']
    credit_card_info: CardInfo
    debit_card_info: CardInfo
