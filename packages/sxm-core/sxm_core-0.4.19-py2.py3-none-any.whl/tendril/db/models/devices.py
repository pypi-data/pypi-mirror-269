

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from tendril.authz.roles.devices import FleetAgencyRoleSpec
from tendril.authz.roles.devices import FleetRoleSpec
from tendril.authz.roles.devices import DeviceRoleSpec
from tendril.authz.roles.devices import DeviceContentRoleSpec
from tendril.authz.roles.devices import CarouselContentRoleSpec
from tendril.authz.approvals.content import DeviceContentApprovalSpec

from tendril.db.models.interests import InterestModel
from tendril.db.models.deviceconfig import DeviceConfigurationModel
from tendril.db.models.content import ContentModel
from tendril.db.models.interests_approvals import InterestModelApprovalMixin
from tendril.db.models.interests_approvals import InterestModelApprovalContextMixin
from tendril.db.models.imageset import ImageSetModel

from tendril.utils import log
logger = log.get_logger(__name__)


class FleetAgencyModel(InterestModel):
    type_name = "fleet_agency"
    role_spec = FleetAgencyRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class FleetModel(InterestModel, InterestModelApprovalContextMixin):
    type_name = "fleet"
    role_spec = FleetRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class DeviceModel(InterestModel):
    type_name = "device"
    role_spec = DeviceRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)
    appname = Column(String(32), nullable=False)
    config_id = Column(Integer, ForeignKey(DeviceConfigurationModel.id))

    @declared_attr
    def config(cls):
        return relationship(DeviceConfigurationModel, back_populates='devices', lazy='selectin')

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }


class DeviceContentModel(InterestModel, InterestModelApprovalMixin):
    type_name = "device_content"
    role_spec = DeviceContentRoleSpec()
    approval_spec = DeviceContentApprovalSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)
    content_id = Column(Integer, ForeignKey("Content.id"))

    @declared_attr
    def content(cls):
        return relationship(ContentModel, back_populates='device_content', lazy='selectin')

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }

class CarouselContentModel(InterestModel):
    type_name = "carousel_content"
    role_spec = CarouselContentRoleSpec()

    id = Column(Integer, ForeignKey("Interest.id"), primary_key=True)
    imageset_id = Column(Integer, ForeignKey("ImageSet.id"))

    @declared_attr
    def imageset(cls):
        return relationship(ImageSetModel, lazy='selectin')

    __mapper_args__ = {
        "polymorphic_identity": type_name,
    }
