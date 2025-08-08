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


class Coupon (TypedDict, total=False):
    type: Literal['percent_off', 'fixed_value']
    value: float
    max_discount: float
    id: str
    name: str


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
    type: Literal['account_balance', 'apple_pay', 'bancolombia',
                  'boleto_bancario', 'cash', 'credit_card', 'debit_card',
                  'google_pay', 'meal_voucher', 'nu_pay', 'paypal', 'pix']
    credit_card_info: CardInfo
    debit_card_info: CardInfo


class Location(TypedDict, total=False):
    latitude: float
    longitude: float
    collected_at: str


class PersonID(TypedDict, total=False):
    type: str
    value: str
