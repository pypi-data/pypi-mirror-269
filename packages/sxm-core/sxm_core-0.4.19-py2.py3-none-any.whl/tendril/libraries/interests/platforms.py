

from tendril.interests import Platform
from tendril.libraries.interests.base import GenericInterestLibrary
from tendril.libraries.interests.manager import InterestLibraryManager
from tendril.libraries.mixins.interests_approvals import ApprovalContextLibraryMixin
from tendril.libraries.mixins.interests_monitors import MonitorsLibraryMixin
from tendril.libraries.mixins.interests_policies import PolicyLibraryMixin
from tendril.libraries.mixins.interests_graphs import GraphsLibraryMixin


class PlatformLibrary(GenericInterestLibrary,
                      MonitorsLibraryMixin,
                      ApprovalContextLibraryMixin,
                      PolicyLibraryMixin,
                      GraphsLibraryMixin):
    interest_class = Platform


def load(manager: InterestLibraryManager):
    manager.install_library('platforms', PlatformLibrary())
