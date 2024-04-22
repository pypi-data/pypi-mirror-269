

import arrow
from decimal import Decimal

from tendril.utils.types.time import Frequency
from tendril.utils.types.time import TimeSpan
from tendril.utils.types.memory import MemorySize
from tendril.utils.types.thermodynamic import Temperature

from tendril.monitors.spec import MonitorSpec
from tendril.monitors.spec import MonitorExportLevel
from tendril.monitors.spec import MonitorPublishFrequency
from tendril.monitors.spec import ensure_str

from tendril.core.tsdb.constants import TimeSeriesFundamentalType


# These things are very hardcoded in sxm-watchdog-devices.
# Don't change without changing there as well.
sxm_device_container_monitors_spec = [
    MonitorSpec('devices_online.direct', default=0,
                deserializer=int, localization_from_hierarchy=False,
                publish_frequency=MonitorPublishFrequency.ONCHANGE,
                publish_measurement='devices_online',
                export_level=MonitorExportLevel.NORMAL),
    MonitorSpec('devices_online.total', default=0,
                deserializer=int, localization_from_hierarchy=False,
                publish_frequency=MonitorPublishFrequency.ONCHANGE,
                publish_measurement='devices_online',
                export_level=MonitorExportLevel.NORMAL),
    MonitorSpec('devices_registered.direct', default=0,
                deserializer=int, localization_from_hierarchy=False,
                publish_frequency=MonitorPublishFrequency.ONCHANGE,
                publish_measurement='devices_registered',
                export_level=MonitorExportLevel.NORMAL, is_constant=True),
    MonitorSpec('devices_registered.total', default=0,
                deserializer=int, localization_from_hierarchy=False,
                publish_frequency=MonitorPublishFrequency.ONCHANGE,
                publish_measurement='devices_registered',
                export_level=MonitorExportLevel.NORMAL, is_constant=True),
]

sxm_device_monitors_spec = [
    # Use of expiry here is not sufficient. We never actually get a
    #  false when device initiates write. watchdog-devices listens
    #  to the data stream and injects false packets when expiry is needed.
    MonitorSpec('online', expire=120, default=False, deserializer=bool,
                publish_frequency=MonitorPublishFrequency.ALWAYS,
                export_level=MonitorExportLevel.STUB),
    MonitorSpec('last_seen',
                export_processor=lambda x: x.humanize(), export_level=MonitorExportLevel.STUB,
                serializer=lambda x: x.for_json(), deserializer=lambda x: arrow.get(ensure_str(x)),
                publish_frequency=MonitorPublishFrequency.NEVER,
                fundamental_type=TimeSeriesFundamentalType.TIMESTAMP),
    MonitorSpec('cpu.frequency.current', export_name='cpu.frequency',
                deserializer=Frequency, preprocessor=[lambda x: int(x), lambda x: 1000000 * x],
                publish_measurement='frequency',
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('cpu.load_avg[0]', export_name='cpu.load_avg_1',
                deserializer=Decimal,
                preprocessor=[lambda x: f"{x:.2f}", ensure_str],
                publish_measurement='load_avg_1',
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('cpu.load_avg[1]', export_name='cpu.load_avg_5',
                deserializer=Decimal, preprocessor=lambda x: f"{x:.2f}",
                publish_measurement='load_avg_5',
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('cpu.load_avg[2]', export_name='cpu.load_avg_15',
                deserializer=Decimal, preprocessor=lambda x: f"{x:.2f}",
                publish_measurement='load_avg_15',
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('disks.capacity', deserializer=MemorySize, is_constant=True,
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('disks.free', deserializer=MemorySize,
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('memory.capacity', deserializer=MemorySize, is_constant=True,
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('memory.available', deserializer=MemorySize,
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('temperature.*', deserializer=Temperature,
                preprocessor=lambda x: f"{x:.1f}C", multiple_container=dict,
                publish_measurement='temperature',
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('uptime', deserializer=TimeSpan, preprocessor=lambda x: int(x),
                export_processor=lambda x: x.timedelta.trim(),
                publish_frequency=MonitorPublishFrequency.ALWAYS,
                is_monotonic=True),
    MonitorSpec('display.connected', deserializer=bool,
                export_level=MonitorExportLevel.NORMAL,
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('streamwatcher.running', deserializer=bool,
                export_level=MonitorExportLevel.FULL,
                publish_frequency=MonitorPublishFrequency.ONCHANGE),
    MonitorSpec('impressions.current', deserializer=int,
                export_level=MonitorExportLevel.NORMAL,
                publish_frequency=MonitorPublishFrequency.ALWAYS),
    MonitorSpec('impressions.new', deserializer=int, export_level=MonitorExportLevel.NORMAL,
                publish_frequency=MonitorPublishFrequency.ALWAYS,
                is_cumulative=True, is_continuous=False),
    MonitorSpec('impressions.total', deserializer=int, export_level=MonitorExportLevel.FULL,
                publish_frequency=MonitorPublishFrequency.NEVER),
]
