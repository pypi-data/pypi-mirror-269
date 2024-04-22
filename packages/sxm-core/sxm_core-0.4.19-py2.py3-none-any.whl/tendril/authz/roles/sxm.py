

from tendril.authz.roles.interests import InterestRoleSpec


class StarXMediaRolesTemplate(InterestRoleSpec):
    apex_role = 'Administrator'
    base_role = 'Member'

    read_role = base_role
    edit_role = apex_role
    delete_role = apex_role

    authz_read_role = base_role
    authz_write_role = apex_role
    authz_write_peers = False

    child_read_role = base_role
    child_add_role = apex_role
    child_delete_role = apex_role

    inherits_from_parent = True
