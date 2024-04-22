

from .sxm import StarXMediaRolesTemplate


class ContentProviderRoleSpec(StarXMediaRolesTemplate):
    prefix = 'content_provider'
    allowed_children = []
    roles = ['Administrator', 'Member']
