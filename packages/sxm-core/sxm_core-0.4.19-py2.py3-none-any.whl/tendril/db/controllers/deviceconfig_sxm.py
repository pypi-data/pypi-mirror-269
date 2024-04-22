

from sqlalchemy.exc import NoResultFound

from tendril.db.controllers.interests import get_interest
from tendril.common.interests.representations import rewrap_interest
from tendril.common.states import LifecycleStatus
from tendril.common.sxm.exceptions import DeviceContentNotRecognized
from tendril.common.sxm.exceptions import DeviceContentNotReady
from tendril.common.sxm.exceptions import DeviceContentUserUnauthorized
from tendril.common.sxm.exceptions import CarouselContentNotRecognized
from tendril.common.sxm.exceptions import CarouselContentNotReady
from tendril.common.sxm.exceptions import CarouselContentUserUnauthorized

from tendril.utils.db import with_db
from tendril.utils import log
logger = log.get_logger(__name__)


@with_db
def validate_device_content(content_id, user, session=None):
    # Check content_id is a content
    try:
        content = get_interest(id=content_id, type='device_content', session=session)
        content = rewrap_interest(content)
    except NoResultFound:
        raise DeviceContentNotRecognized(id=content_id)

    # Check content_id is active
    if content.status != LifecycleStatus.ACTIVE:
        raise DeviceContentNotReady(id=content_id, name=content.name,
                                    status=content.status)

    # Check user has access to content_id
    if not content.check_user_access(user=user, action='read', session=session):
        raise DeviceContentUserUnauthorized(id=content_id, name=content.status, user=user)

    # TODO Check for Approvals

    logger.debug(f"Validated device_content {content_id} for use by {user.id}.")
    return content_id


@with_db
def validate_carousel_content(carousel_content_id, user, session=None):
    try:
        content = get_interest(id=carousel_content_id, type='carousel_content', session=session)
        content = rewrap_interest(content)
    except NoResultFound:
        raise CarouselContentNotRecognized(id=carousel_content_id)

    # Check content_id is active
    if content.status != LifecycleStatus.ACTIVE:
        raise CarouselContentNotReady(id=carousel_content_id, name=content.name,
                                      status=content.status)

    # Check user has access to content_id
    if not content.check_user_access(user=user, action='read', session=session):
        raise CarouselContentUserUnauthorized(id=carousel_content_id, name=content.status, user=user)

    # TODO Check for Approvals

    logger.debug(f"Validated carousel_content {carousel_content_id} for use by {user.id}.")
    return carousel_content_id
