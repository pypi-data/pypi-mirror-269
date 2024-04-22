

from typing import Literal
from pydantic import Field
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.mixins.content import MediaContentInterest
from tendril.interests.mixins.approvals import InterestApprovalsMixin
from tendril.interests.mixins.approvals import InterestBaseApprovalTMixin
from tendril.db.models.devices import DeviceContentModel

from tendril.interests.mixins.monitors import InterestMonitorsMixin
from tendril.monitors.sxm_media import sxm_media_monitors_spec
from tendril.interests.mixins.localizers import InterestLocalizersMixin
from tendril.interests.mixins.monitors import InterestBaseMonitorsTMixin
from tendril.interests.mixins.localizers import InterestBaseLocalizersTMixin

from tendril.interests.mixins.policies import InterestPoliciesMixin
from tendril.interests.mixins.graphs import InterestGraphsMixin

from tendril.common.interests.representations import ExportLevel


class DeviceContentCreateTModel(InterestBaseCreateTModel):
    type: Literal['device_content']
    content_type: str = Field(..., max_length=32)


class DeviceContentMonitorsMixin(InterestMonitorsMixin):
    # TODO Use appname / id to build this spec dynamically
    #   from a manager / the database
    monitors_spec = sxm_media_monitors_spec


class DeviceContentGraphsMixin(InterestGraphsMixin):
    pass


class DeviceContent(MediaContentInterest,
                    DeviceContentMonitorsMixin,
                    DeviceContentGraphsMixin,
                    InterestLocalizersMixin,
                    InterestPoliciesMixin,
                    InterestApprovalsMixin):
    model = DeviceContentModel
    tmodel_create = DeviceContentCreateTModel

    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseApprovalTMixin,
                             InterestBaseMonitorsTMixin,
                             InterestBaseLocalizersTMixin]
    }

    localizers_spec = {
        'ancestors': ['platform', 'fleet', 'device', 'device_content'],
    }


def load(manager):
    manager.register_interest_type('DeviceContent', DeviceContent)
