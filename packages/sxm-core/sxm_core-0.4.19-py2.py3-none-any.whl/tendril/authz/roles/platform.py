

from .sxm import StarXMediaRolesTemplate
from tendril.authz.roles.interests_approvals import InterestApprovalContextRolesMixin
from tendril.authz.roles.interests_policies import InterestPolicyRolesMixin


class PlatformRoleSpec(StarXMediaRolesTemplate,
                       InterestApprovalContextRolesMixin,
                       InterestPolicyRolesMixin):
    prefix = "platform"
    allowed_children = ['*']
    parent_required = False
    approval_role = 'Platform Media Approver'
    policies_role = 'Platform Policies Manager'

    roles = ['Administrator',
             'Advertising Manager',
             'Media Manager',
             'Device Manager',
             'Member',
             'Platform Media Approver',
             'Platform Policies Manager']
