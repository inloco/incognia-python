# Incognia API Python Client 🐍

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-360/)
![test workflow](https://github.com/inloco/incognia-api-java/actions/workflows/test.yaml/badge.svg)

## Installation

You can install the IncogniaAPI using the following command:

```shell
pip install incognia-python
```

## Usage

### Configuration

Before calling the API methods, you need to create an instance of the `IncogniaAPI` class.

```python3
from incognia.api import IncogniaAPI

api = IncogniaAPI('client-id', 'client-secret')
```

### Incognia API

The implementation is based on the [Incognia API Reference](https://developer.incognia.com/docs/).

#### Authentication

Authentication is done transparently, so you don't need to worry about it.

#### Registering New Signup

This method registers a new signup for the given installation and a structured address, an address
line or coordinates, returning a `dict`, containing the risk assessment and supporting evidence:

```python3
from incognia.api import IncogniaAPI
from incognia.models import StructuredAddress, Coordinates

api = IncogniaAPI('client-id', 'client-secret')

# with structured address, a dict:
structured_address: StructuredAddress = {
    'locale': 'en-US',
    'country_name': 'United States of America',
    'country_code': 'US',
    'state': 'NY',
    'city': 'New York City',
    'borough': 'Manhattan',
    'neighborhood': 'Midtown',
    'street': 'W 34th St.',
    'number': '20',
    'complements': 'Floor 2',
    'postal_code': '10001'
}
assessment: dict = api.register_new_signup('installation-id', structured_address=structured_address)

# with address line:
address_line: str = '350 Fifth Avenue, Manhattan, New York 10118'
assessment: dict = api.register_new_signup('installation-id', address_line=address_line)

# with coordinates, a dict:
coordinates: Coordinates = {
    'lat': 40.74836007062138,
    'lng': -73.98509720487937
}
assessment: dict = api.register_new_signup('installation-id', address_coordinates=coordinates)

# with external_id:
external_id: str = 'external-id'
assessment: dict = api.register_new_signup('installation-id', external_id=external_id)

# with policy_id:
policy_id: str = 'policy-id'
assessment: dict = api.register_new_signup('installation-id', policy_id=policy_id)

# with account_id:
account_id: str = 'account-id'
assessment: dict = api.register_new_signup('installation-id', account_id=account_id)

```

#### Getting a Signup

This method allows you to query the latest assessment for a given signup event, returning a `dict`,
containing the risk assessment and supporting evidence:

```python3
from incognia.api import IncogniaAPI

api = IncogniaAPI('client-id', 'client-secret')

assessment: dict = api.get_signup_assessment('signup-id')
```

#### Registering Feedback

This method registers a feedback event for the given identifiers (optional arguments) related to a
signup, login or payment.

```python3
import datetime as dt
from incognia.api import IncogniaAPI
from incognia.feedback_events import FeedbackEvents  # feedbacks are strings.

api = IncogniaAPI('client-id', 'client-secret')

api.register_feedback(FeedbackEvents.SIGNUP_ACCEPTED, dt.datetime.now(),
                      installation_id='installation-id',
                      account_id='account-id',
                      signup_id='signup-id')
```

#### Registering Payment

This method registers a new payment for the given installation and account, returning a `dict`,
containing the risk assessment and supporting evidence.

```python3
from typing import List
from incognia.api import IncogniaAPI
from incognia.models import TransactionAddress, PaymentValue, PaymentMethod

api = IncogniaAPI('client-id', 'client-secret')

addresses: List[TransactionAddress] = [
    {
        'type': 'shipping',
        'structured_address': {
            'locale': 'pt-BR',
            'country_name': 'Brasil',
            'country_code': 'BR',
            'state': 'SP',
            'city': 'São Paulo',
            'borough': '',
            'neighborhood': 'Bela Vista',
            'street': 'Av. Paulista',
            'number': '1578',
            'complements': 'Andar 2',
            'postal_code': '01310-200'
        },
        'address_coordinates': {
            'lat': -23.561414,
            'lng': -46.6558819
        }
    }
]

payment_value: PaymentValue = {
    'amount': 5.0,
    'currency': 'BRL'
}

payment_methods: List[PaymentMethod] = [
    {
        'type': 'credit_card',
        'credit_card_info': {
            'bin': '123456',
            'last_four_digits': '1234',
            'expiry_year': '2027',
            'expiry_month': '10'
        }
    },
    {
        'type': 'debit_card',
        'debit_card_info': {
            'bin': '123456',
            'last_four_digits': '1234',
            'expiry_year': '2027',
            'expiry_month': '10'
        }
    }
]

assessment: dict = api.register_payment('installation-id',
                                        'account-id',
                                        'external-id',
                                        addresses=addresses,
                                        payment_value=payment_value,
                                        payment_methods=payment_methods)
```

#### Registering Login

This method registers a new login for the given installation and account, returning a `dict`,
containing the risk assessment and supporting evidence.

```python3
from incognia.api import IncogniaAPI

api = IncogniaAPI('client-id', 'client-secret')

assessment: dict = api.register_login('installation-id', 'account-id', 'external-id')
```

## Evidences

Every assessment response includes supporting evidence in a dict. You can find all available
evidences [here](https://docs.incognia.com/apis/understanding-assessment-evidence).

## Error Handling

Every method call can throw `IncogniaHTTPError` and `IncogniaError`.

`IncogniaHTTPError` is thrown when the API returned an unexpected http status code.

`IncogniaError` represents unknown errors, like required parameters none or empty.

## How to Contribute

Your contributions are highly appreciated. If you have found a bug or if you have a feature request,
please report them at this repository
[issues section](https://github.com/inloco/incognia-python/issues).

### Development

#### Versioning

This project uses [Semantic Versioning](https://semver.org/), where version follows
`v{MAJOR}.{MINOR}.{PATCH}` format. In summary:

- _Major version update_ - Major functionality changes. Might not have direct backward
  compatibility.
  For example, multiple public API parameter changes.
- _Minor version update_ - Additional features. Major bug fixes. Might have some minor backward
  compatibility issues. For example, an extra parameter on a callback function.
- _Patch version update_ - Minor features. Bug fixes. Full backward compatibility. For example,
  extra fields added to the public structures with version bump.

#### Release

On GitHub, you should merge your changes to the `main` branch, create the git
[versioning](#Versioning) tag and finally push those changes:

```shell
$ git checkout main
$ git pull
$ git merge <your_branch>
$ git tag -a v<version> -m "<description>"
$ git push origin HEAD --tags
```

- example:

```shell
$ git checkout main
$ git pull
$ git merge feat/some-feature
$ git tag -a v2.1.0 -m "This release adds some feature..."
$ git push origin HEAD --tags
```

Our CI will build images with the tagged version and publish them
to [our PyPI repository](https://pypi.org/project/incognia-python/).

## What is Incognia?

Incognia is a location identity platform for mobile apps that enables:

- Real-time address verification for onboarding
- Frictionless authentication
- Real-time transaction verification

## Create a Free Incognia Account

1. Go to [Incognia](https://www.incognia.com/) and click on "Sign Up For Free"
2. Create an Account
3. You're ready to integrate [Incognia SDK](https://docs.incognia.com/sdk/getting-started) and
   use [Incognia APIs](https://dash.incognia.com/api-reference)

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
