

from typing import Literal
from typing import Optional
from pydantic import Field
from tendril.caching import transit
from tendril.iotedge import profiles
from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseEditTModel

from tendril.common.states import LifecycleStatus
from tendril.db.models.devices import DeviceModel
from tendril.db.models.deviceconfig import cfg_option_spec
from tendril.db.controllers.deviceconfig_sxm import validate_device_content
from tendril.db.controllers.deviceconfig_sxm import validate_carousel_content
from tendril.common.interests.representations import ExportLevel

from tendril.interests.mixins.monitors import InterestMonitorsMixin
from tendril.interests.mixins.monitors import InterestBaseMonitorsTMixin
from tendril.monitors.sxm_device import sxm_device_monitors_spec
from tendril.monitors.sxm_media import sxm_media_player_monitors_spec

from tendril.interests.mixins.localizers import InterestLocalizersMixin
from tendril.interests.mixins.localizers import InterestBaseLocalizersTMixin

from tendril.interests.mixins.policies import InterestPoliciesMixin
from tendril.interests.mixins.graphs import InterestGraphsMixin
from tendril.graphs.device import DeviceDetailsDashboard
from tendril.graphs.device import DeviceHighlightsDashboard


from tendril.authz.roles.interests import require_state
from tendril.authz.roles.interests import require_permission

from tendril.core.mq.aio import with_mq_client
from tendril.utils.db import with_db
from tendril.utils import log
logger = log.get_logger(__name__)


class DeviceCreateTModel(InterestBaseCreateTModel):
    type: Literal['device']
    appname: str = Field(..., max_length=32)


class DeviceEditTModel(InterestBaseEditTModel):
    appname: Optional[str] = Field(default='', max_length=32)


class DeviceMonitorsMixin(InterestMonitorsMixin):
    # TODO Use appname / id to build this spec dynamically
    #   from a manager / the database
    monitors_spec = (sxm_device_monitors_spec +
                     sxm_media_player_monitors_spec)


class DeviceGraphsMixin(InterestGraphsMixin):
    graphs_specs = [
        DeviceHighlightsDashboard,
        DeviceDetailsDashboard
    ]


class Device(InterestBase,
             DeviceMonitorsMixin,
             DeviceGraphsMixin,
             InterestPoliciesMixin,
             InterestLocalizersMixin):

    model = DeviceModel
    tmodel_create = DeviceCreateTModel
    tmodel_edit = DeviceEditTModel

    additional_fields = [('appname', ExportLevel.STUB, str, [], {'default': "", 'max_length': 32})]
    additional_tmodel_mixins = {
        ExportLevel.NORMAL: [InterestBaseMonitorsTMixin,
                             InterestBaseLocalizersTMixin]
    }

    localizers_spec = {
        'ancestors': ['platform', 'fleet_agency', 'fleet'],
    }

    def __init__(self, *args, appname=None, **kwargs):
        self._appname = appname
        self._profile = None
        super(Device, self).__init__(*args, **kwargs)

    @property
    def appname(self):
        if self._appname:
            return self._appname
        else:
            return self._model_instance.appname

    @with_db
    def activate(self, background_tasks=None, auth_user=None, session=None):
        result, msg = super(Device, self).activate(background_tasks=background_tasks,
                                                   auth_user=auth_user, session=session)

        if not self.model_instance.status == LifecycleStatus.ACTIVE:
            return result, msg

        from tendril.authn.users import find_user_by_email
        from tendril.authn.users import set_user_password
        from tendril.authn.users import create_mechanized_user
        from tendril.authn.users import get_mechanized_user_email

        username = self.name
        prefix = self.appname

        # If an account exists for the user, nuke it. We're here because
        # someone changed the device state to new, we assume for re-registration.
        mu_email = get_mechanized_user_email(username, prefix)
        mu_existing = find_user_by_email(mu_email)
        if len(mu_existing):
            logger.info(f"Changing password of exiting mechanized user {mu_existing}")
            # Change password instead of creating
            password = set_user_password(mu_existing[0])
        else:
            # Create an account for the device if it does not exist
            logger.info(f"Creating new mechanized user for {username}, {prefix}")
            password = create_mechanized_user(username, prefix)
        # Publish the generated password onto redis for transmission.
        transit.write(value=password, namespace="ott:dp", key=username)
        return result, msg

    @with_db
    @require_permission('read_settings', strip_auth=False, required=False)
    def profile(self, auth_user=None, session=None):
        if not self._profile:
            self._profile = profiles.profile(self.appname)(self._model_instance)
        return self._profile

    @with_mq_client
    async def send_message_to_device_async(self, msg, mq=None):
        # TODO Consider making this send_message_to_interest.
        key = f'device.to.{self.model_instance.name}'
        await mq.publish(key, msg)

    def send_message_to_device(self, msg, background_tasks=None):
        if background_tasks:
            background_tasks.add_task(self.send_message_to_device_async, msg)
        else:
            # TODO Implement some alternative mechanism
            pass

    def trigger_device_settings_update(self, background_tasks=None):
        self.send_message_to_device_async(msg={'action': 'get_settings'},
                                          background_tasks=background_tasks)

    def trigger_device_publish_logs(self, background_tasks=None):
        self.send_message_to_device_async(msg={'action': 'publish_logs'},
                                          background_tasks=background_tasks)

    @with_db
    def _marquee_styling_gatekeeper(self, user=None, session=None):
        mwp_policy = self.policy_get('marquee_write')
        if mwp_policy and not mwp_policy["styling"]:
            return False
        return True

    @with_db
    def _marquee_default_gatekeeper(self, user=None, session=None):
        mwp_policy = self.policy_get('marquee_write')
        if mwp_policy and not mwp_policy["default"]:
            return False
        return True

    @with_db
    def _device_content_gatekeeper(self, user=None, session=None):
        dcw_policy = self.policy_get('device_content_write', session=session)
        if dcw_policy and not dcw_policy["value"]:
            return False
        return True

    @with_db
    def _device_content_validator(self, content_id, user=None, session=None):
        if not content_id:
            return None
        return validate_device_content(content_id, user, session=session)

    @with_db
    def _carousel_content_gatekeeper(self, user=None, session=None):
        ccw_policy = self.policy_get('carousel_content_write', session=session)
        if ccw_policy and not ccw_policy["value"]:
            return False
        return True

    @with_db
    def _carousel_content_validator(self, content_id, user=None, session=None):
        if not content_id:
            return None
        return validate_carousel_content(content_id, user, session=session)

    @with_db
    def _apply_configuration(self, spec, settings, config, user, session=None):
        for key, lspec in spec.items():
            if isinstance(lspec, cfg_option_spec):
                if lspec.read_only:
                    continue
                value = getattr(settings, key)
                if lspec.gatekeeper:
                    if isinstance(lspec.gatekeeper, str):
                        gatekeeper = getattr(self, lspec.gatekeeper)
                    else:
                        gatekeeper = lspec.gatekeeper
                    allowed = gatekeeper(user=user, session=session)
                    if not allowed:
                        continue
                if value is None and not lspec.allow_none:
                    continue
                if lspec.validator:
                    if isinstance(lspec.validator, str):
                        validator = getattr(self, lspec.validator)
                    else:
                        validator = lspec.validator
                    value = validator(value, user=user, session=session)
                setattr(config, lspec.accessor, value)
            elif isinstance(lspec, dict):
                lsettings = getattr(settings, key)
                if not lsettings:
                    continue
                self._apply_configuration(lspec, lsettings, config,
                                          user=user, session=None)
            else:
                raise TypeError("Unsupported Type of key {} "
                                "for Device Configuration: {}"
                                "".format(lspec, cfg_option_spec))

    @with_db
    @require_state(LifecycleStatus.ACTIVE)
    @require_permission('write_settings', strip_auth=False)
    def configure(self, settings, auth_user=None, session=None):
        # TODO Consider whether this should be refactored to put more / all of
        #  it into iotedge deviceconfig model. .
        # TODO Verify settings / permissions here first
        config = self.model_instance.config
        spec = config.configuration_spec()
        logger.info(f"Applying settings to device {self.id} : {settings}")
        self._apply_configuration(spec, settings, config,
                                  user=auth_user, session=session)


def load(manager):
    manager.register_interest_type('Device', Device)
