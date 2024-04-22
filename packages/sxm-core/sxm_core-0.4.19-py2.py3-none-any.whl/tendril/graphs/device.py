

from tendril.connectors.grafana.models.dashboard import DashboardSpecBase
from tendril.connectors.grafana.models.variables import QueriedVariable
from tendril.connectors.grafana.models.panel import PanelSpecBase


class DeviceNameQueryVariable(QueriedVariable):
    query = "SELECT descriptive_name FROM \"Interest\"\nWHERE name = '${device}';"


class DeviceConnectionStatusPanel(PanelSpecBase):
    library_panel_name = 'device-connection-status'


class DeviceDeviceContentPlayCountsPanel(PanelSpecBase):
    library_panel_name = 'device-device-content-play-counts'


class DeviceCpuFrequencyPanel(PanelSpecBase):
    library_panel_name = 'device-cpu-frequency'


class DeviceLoadAveragePanel(PanelSpecBase):
    library_panel_name = 'device-load-average'


class DeviceMemoryPanel(PanelSpecBase):
    library_panel_name = 'device-memory-status'


class DeviceStoragePanel(PanelSpecBase):
    library_panel_name = 'device-storage-status'


class DeviceUptimePanel(PanelSpecBase):
    library_panel_name = 'device-uptime'


class DeviceTemperaturesPanel(PanelSpecBase):
    library_panel_name = 'device-temperatures'


class DeviceDashboardBase(DashboardSpecBase):
    @property
    def container(self):
        for parent in self._actual.parents():
            if parent.type_name in ['fleet', 'platform']:
                return parent

    @property
    def variables_constant(self):
        return {
            self.container.type_name: self.container.name
        }

    @property
    def variables_url(self):
        return {
            self._actual.type_name: self._actual.name
        }

    @property
    def variables_query(self):
        return {
            f'{self._actual.type_name}_name': DeviceNameQueryVariable()
        }

class DeviceHighlightsDashboard(DeviceDashboardBase):
    name = "highlights"
    title = "Device Monitors - Highlights"

    @property
    def uid(self):
        return f'{self.container.type_name}-{self.container.id}-device-highlights'

    @property
    def panels(self):
        return [
            DeviceConnectionStatusPanel(),
            DeviceDeviceContentPlayCountsPanel(),
        ]


class DeviceDetailsDashboard(DeviceDashboardBase):
    name = "details"
    title = "Device Monitors - Details"

    @property
    def uid(self):
        return f'{self.container.type_name}-{self.container.id}-device-details'

    @property
    def panels(self):
        return [
            DeviceConnectionStatusPanel(),
            DeviceUptimePanel(),
            DeviceDeviceContentPlayCountsPanel(),
            DeviceTemperaturesPanel(),
            DeviceStoragePanel(),
            DeviceMemoryPanel(),
            DeviceCpuFrequencyPanel(),
            DeviceLoadAveragePanel(),
        ]