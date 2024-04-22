

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.mixins.approvals import InterestApprovalsContextMixin
from tendril.authz.approvals import approval_types

from tendril.interests.mixins.monitors import InterestMonitorsMixin
from tendril.interests.mixins.monitors import InterestBaseMonitorsTMixin
from tendril.monitors.sxm_device import sxm_device_container_monitors_spec
from tendril.monitors.sxm_media import sxm_media_player_monitors_spec

from tendril.interests.mixins.localizers import InterestLocalizersMixin
from tendril.interests.mixins.localizers import InterestBaseLocalizersTMixin
from tendril.common.interests.representations import ExportLevel

from tendril.interests.mixins.policies import InterestPoliciesMixin
from tendril.interests.mixins.graphs import InterestGraphsMixin

from tendril.db.models.platform import PlatformModel


class PlatformMonitorsMixin(InterestMonitorsMixin):
    monitors_spec = (sxm_device_container_monitors_spec +
                     sxm_media_player_monitors_spec)


class PlatformCreateTModel(InterestBaseCreateTModel):
    type: Literal['platform']


class PlatformGraphsMixin(InterestGraphsMixin):
    pass


class Platform(InterestBase,
               PlatformMonitorsMixin,
               PlatformGraphsMixin,
               InterestPoliciesMixin,
               InterestLocalizersMixin,
               InterestApprovalsContextMixin):
    model = PlatformModel
    tmodel_create = PlatformCreateTModel

    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseMonitorsTMixin,
                             InterestBaseLocalizersTMixin]
    }

    localizers_spec = {
        'ancestors': ['platform'],
    }

    approval_types = [approval_types['platform_media_approval']]


def load(manager):
    manager.register_interest_type('Platform', Platform)
