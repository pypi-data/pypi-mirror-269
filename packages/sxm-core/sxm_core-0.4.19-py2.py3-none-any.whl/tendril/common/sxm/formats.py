

from enum import Enum
from typing import List
from typing import Optional
from datetime import datetime
from datetime import timedelta

from tendril.common.iotedge.formats import IoTDeviceMessageTModel
from tendril.utils.pydantic import TendrilTBaseModel


class IoTMediaEventType(Enum):
    play_success='play_success'
    play_failure='play_failure'
    play_partial='play_partial'
    download_success='download_success'
    download_failure='download_failure'
    cache_eviction='cache_eviction'


class IoTMediaEventReportTModel(TendrilTBaseModel):
    filename: str
    event_source: Optional[str]
    reference: Optional[int]
    timestamp: datetime
    evidence: Optional[str]
    duration: Optional[timedelta] = None


class IoTMediaEventReportsTModel(IoTDeviceMessageTModel):
    reports: List[IoTMediaEventReportTModel]
