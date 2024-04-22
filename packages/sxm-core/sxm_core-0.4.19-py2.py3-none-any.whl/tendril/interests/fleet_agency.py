

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.db.models.devices import FleetAgencyModel

from tendril.interests.mixins.monitors import InterestMonitorsMixin
from tendril.monitors.sxm_device import sxm_device_container_monitors_spec
from tendril.interests.mixins.monitors import InterestBaseMonitorsTMixin

from tendril.interests.mixins.localizers import InterestLocalizersMixin
from tendril.interests.mixins.localizers import InterestBaseLocalizersTMixin
from tendril.common.interests.representations import ExportLevel

from tendril.interests.mixins.policies import InterestPoliciesMixin



class FleetAgencyCreateTModel(InterestBaseCreateTModel):
    type: Literal['fleet_agency']


class FleetAgencyMonitorsMixin(InterestMonitorsMixin):
    monitors_spec = sxm_device_container_monitors_spec


class FleetAgency(InterestBase,
                  FleetAgencyMonitorsMixin,
                  InterestPoliciesMixin,
                  InterestLocalizersMixin):
    model = FleetAgencyModel
    tmodel_create = FleetAgencyCreateTModel

    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseMonitorsTMixin,
                             InterestBaseLocalizersTMixin]
    }

    localizers_spec = {
        'ancestors': ['platform', 'fleet_agency'],
    }


def load(manager):
    manager.register_interest_type('FleetAgency', FleetAgency)
