import json
from typing import Optional, Any

from exceptions import IncogniaError


class Coordinates:
    def __init__(self, lat: float, lng: float):
        try:
            assert lat, 'lat is required.'
            assert lng, 'lng is required.'
            self.lat = lat
            self.lng = lng
        except AssertionError as e:
            raise IncogniaError(e)


class StructuredAddress:
    def __init__(self,
                 locale: Optional[str] = None,
                 country_name: Optional[str] = None,
                 country_code: Optional[str] = None,
                 state: Optional[str] = None,
                 city: Optional[str] = None,
                 borough: Optional[str] = None,
                 neighborhood: Optional[str] = None,
                 street: Optional[str] = None,
                 number: Optional[str] = None,
                 complements: Optional[str] = None,
                 postal_code: Optional[str] = None):
        self.locale = locale
        self.country_name = country_name
        self.country_code = country_code
        self.state = state
        self.city = city
        self.borough = borough
        self.neighborhood = neighborhood
        self.street = street
        self.number = number
        self.complements = complements
        self.postal_code = postal_code


class PostSignupRequestBody:
    def __init__(self,
                 installation_id: str,
                 address_line: Optional[str] = None,
                 structured_address: Optional[StructuredAddress] = None,
                 coordinates: Optional[Coordinates] = None):
        try:
            assert installation_id, 'installation_id is required.'
            self.installation_id = installation_id
            self.address_line = address_line
            self.structured_address = structured_address
            self.coordinates = coordinates
        except AssertionError as e:
            raise IncogniaError(e)


class SignupRequestEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if hasattr(o, '__dict__'):
            return {k: v for (k, v) in o.__dict__.items() if v is not None}
        return json.JSONEncoder.default(self, o)
