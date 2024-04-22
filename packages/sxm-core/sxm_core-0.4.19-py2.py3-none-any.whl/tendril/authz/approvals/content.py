

from tendril.common.states import LifecycleStatus
from tendril.authz.approvals.interests import ApprovalRequirement
from tendril.authz.approvals.interests import InterestApprovalSpec


platform_media_approval = ApprovalRequirement('Platform Media Approval',
                                              'Platform Media Approver', 1,
                                              [LifecycleStatus.APPROVAL, LifecycleStatus.ACTIVE],
                                              'platform')


fleet_media_approval = ApprovalRequirement('Fleet Media Approval', 'Fleet Media Approver', 0,
                                           [LifecycleStatus.APPROVAL, LifecycleStatus.ACTIVE],
                                           'fleet')


advertiser_media_approval = ApprovalRequirement('Advertiser Media Approval', 'Advertiser Media Approver', 0,
                                                [LifecycleStatus.APPROVAL, LifecycleStatus.ACTIVE],
                                                'advertiser')


class ContentApprovalSpec(InterestApprovalSpec):
    _required_approvals = [platform_media_approval]


class DeviceContentApprovalSpec(ContentApprovalSpec):
    _optional_approvals = [fleet_media_approval]


class AdvertisementContentApprovalSpec(ContentApprovalSpec):
    _optional_approvals = [advertiser_media_approval,
                           fleet_media_approval]


approval_types = {
    'platform_media_approval': platform_media_approval,
    'fleet_media_approval': fleet_media_approval,
    'advertiser_media_approval': advertiser_media_approval
}
