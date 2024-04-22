

from .sxm import StarXMediaRolesTemplate
from tendril.authz.roles.artefacts import ArtefactSpec
from tendril.authz.roles.interests_approvals import InterestApprovalRolesMixin
from tendril.authz.roles.interests_approvals import InterestApprovalContextRolesMixin


class AdvertisingAgencyRoleSpec(StarXMediaRolesTemplate):
    prefix = 'advertising_agency'
    allowed_children = ['advertising_agency', 'advertiser']
    roles = ['Administrator', 'Media Manager', 'Advertising Manager', 'Member']


class AdvertiserRoleSpec(StarXMediaRolesTemplate,
                         InterestApprovalContextRolesMixin):
    prefix = 'advertiser'
    allowed_children = ['advertiser', 'campaign', 'advertisement']
    roles = ['Administrator', 'Media Manager', 'Advertising Manager', 'Member', 'Advertiser Media Approver']
    approval_role = 'Advertiser Media Approver'


class CampaignRoleSpec(StarXMediaRolesTemplate):
    prefix = 'campaign'
    allowed_children = ['campaign', 'advertisement']
    roles = ['Administrator', 'Media Manager', 'Advertising Manager', 'Member']


class AdvertisementRoleSpec(StarXMediaRolesTemplate,
                            InterestApprovalRolesMixin):
    prefix = 'advertisement'
    allowed_children = []
    roles = ['Administrator', 'Media Manager', 'Member']
    artefact_add_role = 'Media Manager'
    artefact_delete_role = 'Media Manager'
