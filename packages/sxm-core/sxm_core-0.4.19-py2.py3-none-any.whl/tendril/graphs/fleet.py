

from tendril.connectors.grafana.models.dashboard import DashboardSpecBase
from tendril.connectors.grafana.models.variables import QueriedVariable
from tendril.connectors.grafana.models.panel import PanelSpecBase


class FleetNameQueryVariable(QueriedVariable):
    query = "SELECT descriptive_name FROM \"Interest\"\nWHERE name = '${fleet}';"


class FleetDevicesOnlinePanel(PanelSpecBase):
    library_panel_name = 'fleet-devices-online'


class FleetDeviceContentPlayCountsPanel(PanelSpecBase):
    library_panel_name = 'fleet-device-content-play-counts'


class FleetHighlightsDashboard(DashboardSpecBase):
    name = 'highlights'
    title = "Fleet Monitors"

    @property
    def container(self):
        return self._actual

    @property
    def uid(self):
        return f'{self._actual.type_name}-{self._actual.id}-highlights'

    @property
    def variables_constant(self):
        return {
            self.container.type_name: self.container.name
        }

    @property
    def variables_query(self):
        return {
            f'{self._actual.type_name}_name': FleetNameQueryVariable(),
        }

    @property
    def panels(self):
        return [
            FleetDevicesOnlinePanel(),
            FleetDeviceContentPlayCountsPanel(),
        ]
