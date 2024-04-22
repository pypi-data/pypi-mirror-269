

from tendril.interests.manager import InterestManager


def register_interest_roles(manager):
    manager.register_interest_role(name='Administrator', doc="Full access")
    manager.register_interest_role(name='Media Manager', doc="Upload and Manage Media")
    manager.register_interest_role(name='Device Manager', doc="Manage Device Settings")
    manager.register_interest_role(name='Advertising Manager', doc="Manage Advertisement Orders")
    manager.register_interest_role(name='Finance Manager', doc='Manage Financial Information')
    manager.register_interest_role(name='User', doc="Basic Read Only User")
    manager.register_interest_role(name='Platform Media Approver', doc="Approve Media at the Platform Level")
    manager.register_interest_role(name='Advertiser Media Approver', doc="Approve Media at the Advertiser Level")
    manager.register_interest_role(name='Fleet Media Approver', doc="Approve Media at the Fleet Level")


def load(manager: InterestManager):
    register_interest_roles(manager)
    # TODO This causes a race condition at startup which can interfere with
    #   db.commit_metadata. A better place to put this is needed.
    # from tendril.db.controllers.platform import upsert_platform
    # upsert_platform('StarXMedia', info={}, session=session)
