

from typing import Literal
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.db.models.devices import CarouselContentModel
from tendril.common.interests.representations import ExportLevel
from tendril.interests.mixins.imageset import InterestImageSetMixin
from tendril.interests.mixins.localizers import InterestLocalizersMixin
from tendril.interests.mixins.localizers import InterestBaseLocalizersTMixin
from tendril.interests.mixins.policies import InterestPoliciesMixin


class CarouselContentCreateTModel(InterestBaseCreateTModel):
    type: Literal['carousel_content']


class CarouselContent(InterestImageSetMixin,
                      InterestLocalizersMixin,
                      InterestPoliciesMixin,
                      InterestBase):

    model = CarouselContentModel
    tmodel_create = CarouselContentCreateTModel

    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseLocalizersTMixin]
    }

    localizers_spec = {
        'ancestors': ['platform', 'fleet', 'device'],
    }


def load(manager):
    manager.register_interest_type('CarouselContent', CarouselContent)
