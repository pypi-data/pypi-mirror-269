

# AdvertisingAgency represents various Advertisers
# Advertisers create specific Advertisements
# Advertisers run various advertising Campaigns
# Campaigns consist of AdvertisingEvents
#   across various Devices
#   using specific Advertisements
# Advertising Agencies, Advertisers, and Campaigns can all
#   be composite entities, represent more than one of the same type

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from tendril.db.models.interests import InterestModel

from tendril.authz.roles.advertising import AdvertisingAgencyRoleSpec
from tendril.authz.roles.advertising import AdvertiserRoleSpec
from tendril.authz.roles.advertising import CampaignRoleSpec
from tendril.authz.roles.advertising import AdvertisementRoleSpec
from tendril.authz.approvals.content import AdvertisementContentApprovalSpec

from tendril.db.models.content import ContentModel
from tendril.db.models.interests_approvals import InterestModelApprovalMixin
from tendril.db.models.interests_approvals import InterestModelApprovalContextMixin

from tendril.utils import log
logger = log.get_logger(__name__)


class AdvertisingAgencyModel(InterestModel):
    type_name = "advertising_agency"
    role_spec = AdvertisingAgencyRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class AdvertiserModel(InterestModel, InterestModelApprovalContextMixin):
    type_name = "advertiser"
    role_spec = AdvertiserRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class CampaignModel(InterestModel):
    type_name = "campaign"
    role_spec = CampaignRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class AdvertisementModel(InterestModel,
                         InterestModelApprovalMixin):
    type_name = "advertisement"
    role_spec = AdvertisementRoleSpec()
    approval_spec = AdvertisementContentApprovalSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)
    content_id = Column(Integer, ForeignKey("Content.id"))

    @declared_attr
    def content(cls):
        return relationship(ContentModel, back_populates='advertisement', lazy='selectin')

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }
