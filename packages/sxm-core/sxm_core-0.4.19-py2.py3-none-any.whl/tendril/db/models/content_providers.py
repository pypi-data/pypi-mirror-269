

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_json import mutable_json_type

from tendril.authz.roles.content_providers import ContentProviderRoleSpec
from tendril.db.models.interests import InterestModel

from tendril.utils import log
logger = log.get_logger(__name__)


class ContentProviderModel(InterestModel):
    type_name = "content_provider"
    role_spec = ContentProviderRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    path = Column(String, nullable=False)
    args = Column(mutable_json_type(dbtype=JSONB))
    requires_app = Column(String)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }
