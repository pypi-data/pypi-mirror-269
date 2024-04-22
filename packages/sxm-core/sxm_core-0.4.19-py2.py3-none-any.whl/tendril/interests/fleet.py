

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.mixins.approvals import InterestApprovalsContextMixin

from tendril.interests.mixins.monitors import InterestMonitorsMixin
from tendril.interests.mixins.monitors import InterestBaseMonitorsTMixin
from tendril.monitors.sxm_device import sxm_device_container_monitors_spec
from tendril.monitors.sxm_media import sxm_media_player_monitors_spec

from tendril.interests.mixins.localizers import InterestLocalizersMixin
from tendril.interests.mixins.localizers import InterestBaseLocalizersTMixin
from tendril.common.interests.representations import ExportLevel

from tendril.interests.mixins.policies import InterestPoliciesMixin
from tendril.interests.mixins.graphs import InterestGraphsMixin

from tendril.authz.approvals import approval_types
from tendril.db.models.devices import FleetModel
from tendril.graphs.fleet import FleetHighlightsDashboard


class FleetCreateTModel(InterestBaseCreateTModel):
    type: Literal['fleet']


class FleetMonitorsMixin(InterestMonitorsMixin):
    monitors_spec = (sxm_device_container_monitors_spec +
                     sxm_media_player_monitors_spec)


class FleetGraphsMixin(InterestGraphsMixin):
    graphs_specs = [
        FleetHighlightsDashboard
    ]


class Fleet(InterestBase,
            FleetMonitorsMixin,
            FleetGraphsMixin,
            InterestPoliciesMixin,
            InterestLocalizersMixin,
            InterestApprovalsContextMixin):
    model = FleetModel
    tmodel_create = FleetCreateTModel

    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseMonitorsTMixin,
                             InterestBaseLocalizersTMixin]
    }

    localizers_spec = {
        'ancestors': ['platform', 'fleet_agency', 'fleet'],
    }

    approval_types = [approval_types['fleet_media_approval']]


def load(manager):
    manager.register_interest_type('Fleet', Fleet)
