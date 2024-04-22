

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.db.models.advertising import AdvertiserModel
from tendril.interests.mixins.approvals import InterestApprovalsContextMixin
from tendril.interests.mixins.approvals import InterestBaseApprovalTMixin
from tendril.authz.approvals import approval_types
from tendril.common.interests.representations import ExportLevel


class AdvertiserCreateTModel(InterestBaseCreateTModel):
    type: Literal['advertiser']


class Advertiser(InterestBase,
                 InterestApprovalsContextMixin):
    model = AdvertiserModel
    tmodel_create = AdvertiserCreateTModel
    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseApprovalTMixin]
    }
    approval_types = [approval_types['advertiser_media_approval']]


def load(manager):
    manager.register_interest_type('Advertiser', Advertiser)
