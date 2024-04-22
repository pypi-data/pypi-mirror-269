

from tendril.db.models.deviceconfig_sxm import SXMDeviceConfigurationModel
from tendril.iotedge.profiles.base import DeviceProfile


class SXMSignageNode(DeviceProfile):
    appname = 'sxm'
    config_model = SXMDeviceConfigurationModel


def load(manager):
    manager.register_device_profile('sxm', SXMSignageNode)
