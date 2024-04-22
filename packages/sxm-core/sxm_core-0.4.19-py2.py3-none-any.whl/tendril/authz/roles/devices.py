

from .sxm import StarXMediaRolesTemplate
from tendril.authz.roles.interests_approvals import InterestApprovalRolesMixin
from tendril.authz.roles.interests_approvals import InterestApprovalContextRolesMixin
from tendril.authz.roles.interests_policies import InterestPolicyRolesMixin


class FleetAgencyRoleSpec(StarXMediaRolesTemplate):
    prefix = 'fleet_agency'
    allowed_children = ['fleet_agency', 'fleet']
    roles = ['Administrator', 'Media Manager', 'Device Manager', 'Member']


class FleetRoleSpec(StarXMediaRolesTemplate,
                    InterestApprovalContextRolesMixin,
                    InterestPolicyRolesMixin):
    prefix = 'fleet'
    allowed_children = ['fleet', 'device', 'device_content', 'carousel_content']
    roles = ['Administrator', 'Media Manager', 'Device Manager', 'Member', 'Fleet Media Approver', 'Fleet Policies Manager']
    child_add_roles = {'device': 'Device Manager',
                       'device_content': 'Media Manager',
                       'carousel_content': 'Media Manager'}
    approval_role = 'Fleet Media Approver'
    policies_role = 'Fleet Policies Manager'


class DeviceRoleSpec(StarXMediaRolesTemplate,
                     InterestPolicyRolesMixin):
    prefix = 'device'
    allowed_children = ['device_content', 'carousel_content']
    roles = ['Administrator', 'Media Manager', 'Device Manager', 'Member']
    edit_role = 'Device Manager'
    child_add_roles = {'device_content': 'Media Manager',
                       'carousel_content': 'Media Manager'}

    def _custom_actions(self):
        return {
            'read_settings': ('Member', f'{self.prefix}:read'),
            'write_settings': ('Device Manager', f'{self.prefix}:write')
        }


class DeviceContentRoleSpec(StarXMediaRolesTemplate,
                            InterestApprovalRolesMixin):
    prefix = 'device_content'
    allowed_children = []
    roles = ['Administrator', 'Media Manager', 'Member']
    edit_role = 'Media Manager'
    artefact_add_role = 'Media Manager'
    artefact_delete_role = 'Media Manager'


class CarouselContentRoleSpec(StarXMediaRolesTemplate):
    prefix = 'carousel_content'
    allowed_children = []
    roles = ['Administrator', 'Media Manager', 'Member']
    edit_role = 'Media Manager'
    artefact_add_role = 'Media Manager'
    artefact_delete_role = 'Media Manager'
