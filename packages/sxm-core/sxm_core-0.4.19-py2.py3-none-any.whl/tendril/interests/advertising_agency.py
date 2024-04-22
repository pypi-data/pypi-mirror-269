

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.db.models.advertising import AdvertisingAgencyModel


class AdvertisingAgencyCreateTModel(InterestBaseCreateTModel):
    type: Literal['advertising_agency']


class AdvertisingAgency(InterestBase):
    model = AdvertisingAgencyModel
    tmodel_create = AdvertisingAgencyCreateTModel


def load(manager):
    manager.register_interest_type('AdvertisingAgency', AdvertisingAgency)
