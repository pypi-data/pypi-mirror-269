

from fastapi import BackgroundTasks
from sqlalchemy.exc import NoResultFound

from tendril.db.controllers.content import get_content_by_filename
from tendril.iotedge.registration import get_registration
from tendril.common.sxm.formats import IoTMediaEventType
from tendril.common.sxm.formats import IoTMediaEventReportTModel
from tendril.common.sxm.formats import IoTMediaEventReportsTModel
from tendril.common.interests.representations import rewrap_interest
from tendril.utils.db import get_session
from tendril.utils.db import with_db
from tendril.utils import log
logger = log.get_logger(__name__)


common_event_sources = ('rm',)
device_content_event_sources = ('bg', 'bg_seq')


@with_db
def get_device_content_by_filename(filename=None, session=None):
    # TODO Consider Caching
    content = get_content_by_filename(filename, content_type='media', bucket='cdn', session=session)
    return content.device_content


async def _process_media_event(event_type: IoTMediaEventType,
                               report: IoTMediaEventReportTModel,
                               localizers=None, session=None):
    # TODO This only works for stored files. We need to actually
    #  check the type here before querying the db.
    try:
        context = get_content_by_filename(f'%{report.filename}', content_type='media',
                                          bucket='cdn', session=session)
    except NoResultFound:
        logger.warn(f"Could not determine context for "
                    f"{event_type} event with filename {report.filename}")
        return False
    if report.event_source in device_content_event_sources:
        context = context.device_content
    elif report.event_source in common_event_sources:
        if context.device_content:
            context = context.device_content
        elif context.advertisement:
            context = context.advertisement
    else:
        logger.warn(f"Could not determine context for "
                    f"{event_type} event with filename {report.filename}"
                    f"from device {localizers['device']}")
        return False

    context = rewrap_interest(context)
    localizers['filename'] = report.filename
    localizers['subsystem'] = report.event_source

    spec = context.monitor_get_spec(event_type.value)
    if not spec:
        logger.warn(f"Context {context} does not have a {event_type.value} monitor.")
        return False

    await context.monitor_write(spec, value=report.duration,
                                timestamp=report.timestamp,
                                additional_localizers=localizers)
    return True


async def _process_media_events(event_type: IoTMediaEventType = None,
                                report: IoTMediaEventReportsTModel = None):
    rv = {'success': []}
    with get_session() as session:
        device = get_registration(report.id, session=session)
        # Get device localizers
        # TODO Consider Caching
        localizers = device.interest().cached_localizers(session=session)
        for key in localizers.keys():
            localizers[key] = localizers[key]['name']
        localizers['device'] = device.model_instance.name

        for r in report.reports:
            result = await _process_media_event(event_type=event_type, report=r,
                                                localizers=localizers, session=session)
            if result:
                rv['success'].append(True)
            else:
                rv['success'].append(False)
    return rv


try:
    from tendril.apiserver.routers.iotedge import iotedge_reports_router

    @iotedge_reports_router.post("/event/media/{event_type}")
    async def report_media_event(
            event_type: IoTMediaEventType,
            report: IoTMediaEventReportsTModel,
            background_tasks: BackgroundTasks):
        background_tasks.add_task(_process_media_events,
                                  event_type=event_type,
                                  report=report)

except ImportError:
    pass


routers = []
