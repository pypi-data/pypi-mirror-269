

from tendril.utils.pydantic import TendrilTBaseModel
from tendril.policies.base import PolicyBase

from tendril.interests.mixins.export import InterestIdOnlyTModel
from tendril.db.controllers.interests import get_interest


# TODO Move to Tendril Core
class SimpleInterestReferencePolicyMixin(PolicyBase):
    # Not sure if having this as a separate mixin is valuable enough to
    # warrant the headache. In case it needs to be recombined into the
    # users of this mixin, that is probably fine.
    def validate(self, data: InterestIdOnlyTModel):
        # TODO Check if the ID is valid to begin with?
        if not self.tendril_spec['allowed_referred_interest_types']:
            return
        assert get_interest(data.id).type_name in self.tendril_spec['allowed_referred_interest_types']
        super().validate(data)


# TODO Move to Tendril Core
class SimpleBooleanTModel(TendrilTBaseModel):
    # TODO Is this really the best way to do this?
    value: bool


class FallbackCarouselContentPolicy(SimpleInterestReferencePolicyMixin,
                                    PolicyBase):
    name = 'fallback_carousel_content'
    context_spec = [
        {'domain': 'interests',
         'interest_type': 'device',
         'inherits_from': 'ancestors'}
    ]
    write_requires = {
        'interest_type': ['fleet', 'platform'],
        'role': 'Media Manager'
    }
    schema = InterestIdOnlyTModel
    hints = {
        'refers_interest': True,
        'allowed_referred_interest_types': ['carousel_content'],
        'label_text': "Fallback Carousel Content",
        'user_hint': "Carousel Content to use when not specifically set at a Device. "
                     "This can be set at the Platform or Fleet Level. Can be used in "
                     "combination with the 'Carousel Content Write Policy' to lock all "
                     "fleet devices to a single carousel content."
    }


class CarouselContentWritePolicy(PolicyBase):
    name = 'carousel_content_write'
    context_spec = [
        {'domain': 'interests',
         'interest_type': 'device',
         'inherits_from': 'ancestors'}
    ]
    write_requires = {
        'interest_type': ['fleet', 'platform'],
        'role': 'Media Manager'
    }
    hints = {
        'user_hint': "Whether Carousel Content can be set at the device level. When used "
                     "in combination with the 'Fallback Carousel Content Policy', all "
                     "fleet devices can be locked to a single carousel content.",
        'true_text': "Allowed",
        'false_text': "Not Allowed",
    }
    schema = SimpleBooleanTModel


policy_templates = [
    FallbackCarouselContentPolicy,
    CarouselContentWritePolicy,
]
