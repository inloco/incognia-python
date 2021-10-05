from typing import Optional, TypedDict


class Coordinates(TypedDict):
    lat: float
    lng: float


class StructuredAddress(TypedDict, total=False):
    locale: Optional[str]
    country_name: Optional[str]
    country_code: Optional[str]
    state: Optional[str]
    city: Optional[str]
    borough: Optional[str]
    neighborhood: Optional[str]
    street: Optional[str]
    number: Optional[str]
    complements: Optional[str]
    postal_code: Optional[str]


class TransactionAddress(TypedDict, total=False):
    type: Optional[str]
    structured_address: Optional[StructuredAddress]
    address_coordinates: Optional[Coordinates]
