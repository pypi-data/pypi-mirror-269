
import arrow
from decimal import Decimal
from datetime import timedelta

from tendril.utils.types.time import Frequency
from tendril.utils.types.time import TimeSpan
from tendril.utils.types.memory import MemorySize
from tendril.utils.types.thermodynamic import Temperature

from tendril.monitors.spec import MonitorSpec
from tendril.monitors.spec import MonitorExportLevel
from tendril.monitors.spec import MonitorPublishFrequency
from tendril.monitors.spec import ensure_str

from tendril.core.tsdb.constants import TimeSeriesFundamentalType

# TODO Replace these with a play_success.duration and play_success.count
#   Each published value represents a single successful play, so there
#   is no need to divide duration by estimated duration, etc.

sxm_media_monitors_spec = [
    MonitorSpec('play_success', default=0,
                localization_from_hierarchy=False,
                flatten_cardinality=('filename',),
                structure='duration', deserializer=timedelta,
                serializer=lambda x: x.total_seconds(),
                publish_frequency=MonitorPublishFrequency.ALWAYS,
                export_level=MonitorExportLevel.NEVER,
                fundamental_type=TimeSeriesFundamentalType.NUMERIC,
                is_cumulative=True, is_continuous=False,
                drill_down=['device', 'fleet', 'platform']),
]

sxm_media_player_monitors_spec = [
    MonitorSpec('play_success.duration.*', default=0,
                localization_from_hierarchy=True,
                structure='duration', deserializer=timedelta,
                serializer=lambda x: x.total_seconds(),
                multiple_container = dict,
                multiple_discriminators = ['device_content', 'advertisement'],
                publish_frequency=MonitorPublishFrequency.ALWAYS,
                publish_measurement='play_success',
                export_level=MonitorExportLevel.NEVER,
                fundamental_type=TimeSeriesFundamentalType.NUMERIC,
                is_cumulative=True,is_continuous=False,
                drill_down=['device_content', 'advertisement', 'gallery-content']),
]