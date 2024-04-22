

from typing import List
from functools import lru_cache
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import ARRAY
from sqlalchemy import ForeignKey
from sqlalchemy import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from tendril.db.models.deviceconfig import DeviceConfigurationModel
from tendril.db.models.deviceconfig import cfg_option_spec
from tendril.db.models.content import MediaContentInfoTModel
from tendril.db.models.imageset import ImageSetTModel
from tendril.common.states import LifecycleStatus
from tendril.common.interests.representations import rewrap_interest
from tendril.db.controllers.interests import get_interest

from tendril.utils import log
logger = log.get_logger(__name__)


class SXMDeviceConfigurationModel(DeviceConfigurationModel):
    device_type = "sxm"
    id = Column(Integer, ForeignKey(DeviceConfigurationModel.id), primary_key=True)

    allow_local_usb = Column(Boolean, nullable=False, default=False)
    portrait = Column(Boolean, nullable=False, default=False)
    flip = Column(Boolean, nullable=False, default=False)
    default_content_id = Column(Integer, ForeignKey('DeviceContent.id'))
    carousel_content_id = Column(Integer, ForeignKey('CarouselContent.id'))

    verbose_log = Column(Boolean, default=False)

    marquee_bgcolor = Column(VARCHAR(8), nullable=True)
    marquee_color = Column(VARCHAR(8), nullable=True)
    marquee_frequency = Column(Integer, nullable=True)
    marquee_default = Column(ARRAY(Unicode), nullable=True)

    @declared_attr
    def default_content(cls):
        return relationship('DeviceContentModel', lazy='selectin')

    @declared_attr
    def carousel_content(cls):
        return relationship('CarouselContentModel', lazy='selectin')

    def _get_policy(self, name):
        interest = rewrap_interest(self.devices[0])
        return interest.policy_get(name)

    def _get_policy_content_id(self):
        fdc_policy = self._get_policy('fallback_device_content')
        if not fdc_policy:
            return None
        return fdc_policy['id']

    def _check_content(self, dc):
        if not dc:
            return None
        if isinstance(dc, int):
            interest = get_interest(id=dc, raise_if_none=True)
        else:
            interest = dc
        if interest.type_name is not 'device_content':
            raise ValueError(f"Expecting the device_content "
                             f"to be a device_content. Got {interest.type_name}.")
        if not interest.status == LifecycleStatus.ACTIVE:
            logger.warn(f'device_content {interest.id} for device '
                        f'{self.id} is not ACTIVE. Not sending.')
            return None
        return dc

    def _export_content(self, interest):
        dc = rewrap_interest(interest).content
        return dc.export(full=False, explicit_durations_only=True)

    @property
    def effective_content_id(self):
        effective_dc_id = None
        if self.default_content_id:
            effective_dc_id = self._check_content(self.default_content_id)
        if not effective_dc_id:
            effective_dc_id = self._check_content(self._get_policy_content_id())
        return effective_dc_id

    def _use_content_from_policy(self):
        content_id = self._get_policy_content_id()
        if not content_id:
            return None
        from tendril.utils.db import get_session
        with get_session() as session:
            interest = get_interest(id=content_id, raise_if_none=True, session=session)
            interest = self._check_content(interest)
            if not interest:
                return None
            return self._export_content(interest)

    def _unpack_content(self, content_id):
        if not content_id:
            return self._use_content_from_policy()
        # TODO Check if this check is actually needed anymore.
        if content_id != self.default_content_id:
            raise ValueError("Expecting content_id to be default_content_id")
        content_interest = self._check_content(self.default_content)
        if not content_interest:
            return self._use_content_from_policy()
        return self._export_content(content_interest)

    def _get_policy_carousel_content_id(self):
        fcc_policy = self._get_policy('fallback_carousel_content')
        if not fcc_policy:
            return None
        return fcc_policy['id']

    def _check_carousel_content(self, cc):
        if not cc:
            return None
        if isinstance(cc, int):
            interest = get_interest(id=cc, raise_if_none=True)
        else:
            interest = cc
        if interest.type_name is not 'carousel_content':
            raise ValueError(f"Expecting the carousel_content "
                             f"to be a carousel_content. Got {interest.type_name}.")
        if not interest.status == LifecycleStatus.ACTIVE:
            logger.warn(f'carousel_content {interest.id} for device '
                        f'{self.id} is not ACTIVE. Not sending.')
            return None
        return cc

    def _export_carousel_content(self, interest):
        cc = rewrap_interest(interest)
        return cc.imageset_get_contents()

    @property
    def effective_carousel_content_id(self):
        effective_cc_id = None
        if self.carousel_content_id:
            effective_cc_id = self._check_carousel_content(self.carousel_content_id)
        if not effective_cc_id:
            effective_cc_id = self._check_carousel_content(self._get_policy_carousel_content_id())
        return effective_cc_id

    def _use_carousel_content_from_policy(self):
        carousel_content_id = self._get_policy_carousel_content_id()
        if not carousel_content_id:
            return None
        from tendril.utils.db import get_session
        with get_session() as session:
            interest = get_interest(id=carousel_content_id, raise_if_none=True, session=session)
            interest = self._check_carousel_content(interest)
            if not interest:
                return None
            return self._export_carousel_content(interest)

    def _unpack_carousel_content(self, carousel_content_id):
        if not carousel_content_id:
            return self._use_carousel_content_from_policy()
        # TODO Check if this check is actually needed anymore.
        if carousel_content_id != self.carousel_content_id:
            raise ValueError("Expecting carousel_content_id to be carousel_content_id")
        carousel_content_interest = self._check_carousel_content(self.carousel_content)
        if not carousel_content_interest:
            return self._use_carousel_content_from_policy()
        return self._export_carousel_content(carousel_content_interest)

    def _unpack_marquee_bgcolor(self, value):
        if value:
            return value
        policy = self._get_policy('marquee_styling')
        if policy:
            return policy['bgcolor']['rgbhex']

    @property
    def effective_marquee_bgcolor(self):
        return self._unpack_marquee_bgcolor(self.marquee_bgcolor)

    def _unpack_marquee_color(self, value):
        if value:
            return value
        policy = self._get_policy('marquee_styling')
        if policy:
            return policy['color']['rgbhex']

    @property
    def effective_marquee_color(self):
        return self._unpack_marquee_color(self.marquee_color)

    def _unpack_marquee_frequency(self, value):
        # TODO This does not actually work correctly. If the device sets 0,
        #   we fallback to the policy value which may be non-zero. Checking
        #   for None as intended does not work. There might be is a force
        #   cast happening somewhere which converts the None to 0, possibly
        #   on the setting side. Review and fix.
        if not value:
            return value
        policy = self._get_policy('marquee_default')
        if policy:
            return policy['frequency']['value']
        return 0

    @property
    def effective_marquee_frequency(self):
        return self._unpack_marquee_frequency(self.marquee_frequency)

    def _unpack_marquee_default(self, value):
        if value:
            return value
        policy = self._get_policy('marquee_default')
        if policy:
            return policy['default']

    @property
    def effective_marquee_default(self):
        return self._unpack_marquee_default(self.marquee_default)

    @classmethod
    @lru_cache(maxsize=None)
    def configuration_spec(cls):
        rv = super(SXMDeviceConfigurationModel, cls).configuration_spec()
        rv['display'] = {'portrait': cfg_option_spec('Portait Orientation', 'portrait',
                                                     type=bool, default=False),
                         'flip': cfg_option_spec('Flip Display Orientation', 'flip',
                                                 type=bool, default=False)}
        rv['local_usb'] = {'allow': cfg_option_spec('Allow local USB content', 'allow_local_usb',
                                                    type=bool, default=False)}
        rv['content'] = {'default': cfg_option_spec('Default Device Content', 'default_content_id',
                                                    validator='_device_content_validator',
                                                    exporter='_unpack_content', export_tmodel=MediaContentInfoTModel,
                                                    type=int, default=None, allow_none=True,
                                                    gatekeeper='_device_content_gatekeeper',
                                                    core_annex_accessor='effective_content_id')}
        rv['carousel'] = {'default': cfg_option_spec('Carousel Content', 'carousel_content_id',
                                                    validator='_carousel_content_validator',
                                                    exporter='_unpack_carousel_content', export_tmodel=ImageSetTModel,
                                                    type=int, default=None, allow_none=True,
                                                    gatekeeper='_carousel_content_gatekeeper',
                                                    core_annex_accessor='effective_carousel_content_id')}
        rv['debug'] = {'verbose_log': cfg_option_spec('Enable Verbose Logging', 'verbose_log',
                                                      type=bool, default=False)}
        rv['marquee'] = {'bgcolor': cfg_option_spec('Background Color', 'marquee_bgcolor',
                                                    exporter='_unpack_marquee_bgcolor',
                                                    type=str, default=None, allow_none=True,
                                                    gatekeeper='_marquee_styling_gatekeeper',
                                                    core_annex_accessor='effective_marquee_bgcolor'),
                         'color': cfg_option_spec('Text Color', 'marquee_color',
                                                    exporter='_unpack_marquee_color',
                                                    type=str, default=None, allow_none=True,
                                                    gatekeeper='_marquee_styling_gatekeeper',
                                                    core_annex_accessor='effective_marquee_color'),
                         'frequency': cfg_option_spec('Frequency', 'marquee_frequency',
                                                      exporter='_unpack_marquee_frequency',
                                                      type=str, default=None, allow_none=True,
                                                      gatekeeper='_marquee_default_gatekeeper',
                                                      core_annex_accessor='effective_marquee_frequency'),
                         'default': cfg_option_spec('Default Text', 'marquee_default',
                                                    exporter='_unpack_marquee_default',
                                                    type=List[str], default=None, allow_none=True,
                                                    gatekeeper='_marquee_default_gatekeeper',
                                                    core_annex_accessor='effective_marquee_default')}
        return rv

    __mapper_args__ = {
        "polymorphic_identity": device_type,
    }
