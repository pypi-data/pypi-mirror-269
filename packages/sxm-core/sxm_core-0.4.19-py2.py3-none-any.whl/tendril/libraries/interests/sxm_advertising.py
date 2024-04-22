
from tendril.libraries.interests.base import GenericInterestLibrary
from tendril.libraries.interests.manager import InterestLibraryManager

from tendril.interests.advertising_agency import AdvertisingAgency
from tendril.interests.advertiser import Advertiser
from tendril.interests.campaign import Campaign
from tendril.interests.advertisement import Advertisement
from tendril.libraries.mixins.content import ContentLibraryMixin
from tendril.libraries.mixins.interests_approvals import ApprovalsLibraryMixin
from tendril.libraries.mixins.interests_approvals import ApprovalContextLibraryMixin
from tendril.libraries.mixins.interests_monitors import MonitorsLibraryMixin

from tendril.config import ADVERTISEMENT_TYPES_ALLOWED


class AdvertisingAgencyLibrary(GenericInterestLibrary):
    interest_class = AdvertisingAgency


class AdvertiserLibrary(GenericInterestLibrary,
                        ApprovalContextLibraryMixin):
    interest_class = Advertiser


class CampaignLibrary(GenericInterestLibrary):
    interest_class = Campaign


class AdvertisementLibrary(ContentLibraryMixin,
                           ApprovalsLibraryMixin,
                            MonitorsLibraryMixin,
                           GenericInterestLibrary):
    interest_class = Advertisement
    media_types_allowed = ADVERTISEMENT_TYPES_ALLOWED


def load(manager: InterestLibraryManager):
    manager.install_library('advertising_agencies', AdvertisingAgencyLibrary())
    manager.install_library('advertisers', AdvertiserLibrary())
    manager.install_library('campaigns', CampaignLibrary())
    manager.install_library('advertisements', AdvertisementLibrary())
