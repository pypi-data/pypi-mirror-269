

from tendril.libraries.interests.base import GenericInterestLibrary
from tendril.libraries.interests.manager import InterestLibraryManager

from tendril.interests.fleet_agency import FleetAgency
from tendril.interests.fleet import Fleet
from tendril.interests.device import Device
from tendril.interests.device_content import DeviceContent
from tendril.interests.carousel_content import CarouselContent
from tendril.libraries.mixins.content import ContentLibraryMixin
from tendril.libraries.mixins.imageset import ImageSetLibraryMixin
from tendril.libraries.mixins.interests_approvals import ApprovalsLibraryMixin
from tendril.libraries.mixins.interests_approvals import ApprovalContextLibraryMixin
from tendril.libraries.mixins.interests_monitors import MonitorsLibraryMixin
from tendril.libraries.mixins.interests_policies import PolicyLibraryMixin
from tendril.libraries.mixins.interests_graphs import GraphsLibraryMixin


from tendril.config import DEVICE_CONTENT_TYPES_ALLOWED


class FleetAgencyLibrary(GenericInterestLibrary,
                         MonitorsLibraryMixin):
    interest_class = FleetAgency


class FleetLibrary(GenericInterestLibrary,
                   MonitorsLibraryMixin,
                   ApprovalContextLibraryMixin,
                   PolicyLibraryMixin,
                   GraphsLibraryMixin):
    interest_class = Fleet


class DeviceLibrary(GenericInterestLibrary,
                    MonitorsLibraryMixin,
                    PolicyLibraryMixin,
                    GraphsLibraryMixin):
    enable_creation_api = False
    interest_class = Device


class DeviceContentLibrary(GenericInterestLibrary,
                           ContentLibraryMixin,
                           ApprovalsLibraryMixin,
                           MonitorsLibraryMixin,
                           GraphsLibraryMixin):
    interest_class = DeviceContent
    media_types_allowed = DEVICE_CONTENT_TYPES_ALLOWED


class CarouselContentLibrary(ImageSetLibraryMixin,
                             GenericInterestLibrary):
    interest_class = CarouselContent


def load(manager: InterestLibraryManager):
    manager.install_library('fleet_agencies', FleetAgencyLibrary())
    manager.install_library('fleets', FleetLibrary())
    manager.install_library('devices', DeviceLibrary())
    manager.install_library('device_content', DeviceContentLibrary())
    manager.install_library('carousel_content', CarouselContentLibrary())
