from typing import Final
from unittest import TestCase

from incognia_api.post_signup_request_body import Coordinates, StructuredAddress
from incognia_api.post_signup_request_json_encoder import PostSignupRequestJSONEncoder


class TestPostSignupRequestJSONEncoder(TestCase):
    DICT_WITH_NONE_VALUES: Final[dict] = {
        'key_none_one': None,
        'key_none_two': None,
        'key_array': [1, 2, 3],
        'key_empty_str': '',
        'key_nested': {'key': 'value'},
        'key_int': 42,
        'key_float': 42.24
    }
    ADDRESS_LINE: Final[str] = 'Av. Paulista, 1578 - Bela Vista, São Paulo - SP, 01310-200'
    STRUCTURED_ADDRESS: Final[StructuredAddress] = StructuredAddress(locale='pt-BR',
                                                                     country_name='Brasil',
                                                                     country_code='BR',
                                                                     state='SP',
                                                                     city='São Paulo',
                                                                     borough='',
                                                                     neighborhood='Bela Vista',
                                                                     street='Av. Paulista',
                                                                     number='1578',
                                                                     complements='Andar 2',
                                                                     postal_code='01310-200')
    STRUCTURED_ADDRESS_WITH_NONE_VALUES: Final[StructuredAddress] = StructuredAddress(locale='pt-BR',
                                                                                      country_name=None,
                                                                                      country_code='BR',
                                                                                      state=None,
                                                                                      city='São Paulo',
                                                                                      borough=None,
                                                                                      neighborhood='Bela Vista',
                                                                                      street=None,
                                                                                      number='1578',
                                                                                      complements=None,
                                                                                      postal_code='01310-200')
    ADDRESS_COORDINATES: Final[Coordinates] = Coordinates(-23.561414, -46.6558819)

    def test_default_when_given_dict_with_keys_without_values_should_remove_these_keys(self):
        encoder = PostSignupRequestJSONEncoder()
        fixed_dict: dict = encoder.default(self.DICT_WITH_NONE_VALUES)
        self.assertEqual(fixed_dict, {
            'key_array': [1, 2, 3],
            'key_empty_str': '',
            'key_nested': {'key': 'value'},
            'key_int': 42,
            'key_float': 42.24
        })

    def test_default_when_given_coordinates_should_keep_all_keys(self):
        encoder = PostSignupRequestJSONEncoder()
        fixed_dict: dict = encoder.default(self.ADDRESS_COORDINATES)

        self.assertIn('lat', fixed_dict)
        self.assertIn('lng', fixed_dict)

    def test_default_when_given_structured_address_should_keep_all_keys(self):
        encoder = PostSignupRequestJSONEncoder()
        fixed_dict: dict = encoder.default(self.STRUCTURED_ADDRESS)

        self.assertIn('locale', fixed_dict)
        self.assertIn('country_name', fixed_dict)
        self.assertIn('country_code', fixed_dict)
        self.assertIn('state', fixed_dict)
        self.assertIn('city', fixed_dict)
        self.assertIn('borough', fixed_dict)
        self.assertIn('neighborhood', fixed_dict)
        self.assertIn('street', fixed_dict)
        self.assertIn('number', fixed_dict)
        self.assertIn('complements', fixed_dict)
        self.assertIn('postal_code', fixed_dict)

    def test_default_when_given_structured_address_with_none_values_should_remove_keys_with_none_values(self):
        encoder = PostSignupRequestJSONEncoder()
        fixed_dict: dict = encoder.default(self.STRUCTURED_ADDRESS_WITH_NONE_VALUES)
        self.assertEqual(fixed_dict, {
            'locale': 'pt-BR',
            'country_code': 'BR',
            'city': 'São Paulo',
            'neighborhood': 'Bela Vista',
            'number': '1578',
            'postal_code': '01310-200'
        })
