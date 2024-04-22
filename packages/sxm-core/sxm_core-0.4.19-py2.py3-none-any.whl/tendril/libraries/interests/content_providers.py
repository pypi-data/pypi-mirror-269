

from tendril.interests import ContentProvider
from tendril.libraries.interests.base import GenericInterestLibrary
from tendril.libraries.interests.manager import InterestLibraryManager


class ContentProviderLibrary(GenericInterestLibrary):
    enable_creation_api = False
    enable_activation_api = False
    interest_class = ContentProvider


def load(manager: InterestLibraryManager):
    manager.install_library('content_providers', ContentProviderLibrary())
