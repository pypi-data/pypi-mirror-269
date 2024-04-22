

from typing import Literal
from pydantic import Field
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.mixins.content import MediaContentInterest
from tendril.interests.mixins.approvals import InterestApprovalsMixin
from tendril.db.models.advertising import AdvertisementModel


class AdvertisementCreateTModel(InterestBaseCreateTModel):
    type: Literal['advertisement']
    content_type: str = Field(..., max_length=32)


class Advertisement(MediaContentInterest, InterestApprovalsMixin):
    model = AdvertisementModel
    tmodel_create = AdvertisementCreateTModel


def load(manager):
    manager.register_interest_type('Advertisement', Advertisement)
