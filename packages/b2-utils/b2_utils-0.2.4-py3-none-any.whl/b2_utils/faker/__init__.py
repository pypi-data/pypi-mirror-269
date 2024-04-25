from faker import Faker as _Faker

from .providers import BrazilPersonProvider as _BrazilPersonProvider
from .providers import PhoneProvider as _PhoneProvider
from .providers import ProductProvider as _ProductProvider

faker = _Faker("pt_BR")

faker.add_provider(_PhoneProvider)
faker.add_provider(_ProductProvider)
faker.add_provider(_BrazilPersonProvider)
