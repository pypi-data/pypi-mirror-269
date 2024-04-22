

import rich
import aiocron

from tendril.common.states import LifecycleStatus
from tendril.libraries.interests import platforms
from tendril.libraries.interests import fleets

from tendril.utils.db import get_session
from tendril.config import CRON_ENABLED
from tendril.utils import log
logger = log.get_logger(__name__)


async def get_direct_devices(interest, session=None):
    d = interest.children(child_type='device', session=session)
    return len([x for x in d if x.status in (LifecycleStatus.ACTIVE,
                                             LifecycleStatus.SUSPENDED)])


async def get_all_devices(interest, session=None):
    d = interest.descendents(child_type='device', session=session)
    return len([x for x in d if x.status in (LifecycleStatus.ACTIVE,
                                             LifecycleStatus.SUSPENDED)])


@aiocron.crontab('15 2 * * *', start=False)
async def device_census():
    logger.info("Executing Device Census")
    with get_session() as session:
        for interest in fleets.items(session=session) + platforms.items(session=session):
            direct = await get_direct_devices(interest, session=session)
            await interest.monitor_report_async('devices_registered.direct', direct)

            total = await get_all_devices(interest, session=session)
            await interest.monitor_report_async('devices_registered.total', total)


if CRON_ENABLED:
    device_census.start()
