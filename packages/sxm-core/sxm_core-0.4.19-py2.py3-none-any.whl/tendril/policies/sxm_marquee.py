

from typing import List
from typing import Optional
from pydantic import Field
from tendril.utils.pydantic import TendrilTBaseModel
from tendril.policies.base import PolicyBase


class ColorTModel (TendrilTBaseModel):
    rgbhex: str

class EventFrequencyTModel (TendrilTBaseModel):
    value: int

class MarqueeDefaultTModel (TendrilTBaseModel):
    frequency: EventFrequencyTModel = Field(title="Frequency")
    default: Optional[List[str]] = Field(title="Content")

class MarqueeStylingTModel (TendrilTBaseModel):
    bgcolor: Optional[ColorTModel] = Field(title="Background Color")
    color: Optional[ColorTModel] = Field(title="Text Color")

class MarqueeWriteTModel (TendrilTBaseModel):
    styling: bool = Field(title="Allow Styling Overrides", default=False)
    default: bool = Field(title="Allow Default Overrides", default=False)


class MarqueeDefaultPolicy(PolicyBase):
    name = 'marquee_default'
    context_spec = [
        {'domain': 'interests',
         'interest_type': 'device',
         'inherits_from': 'ancestors'}
    ]
    write_requires = {
        'interest_type': ['fleet', 'platform'],
        'role': 'Media Manager'
    }
    schema = MarqueeDefaultTModel
    hints = {
        'label_text': "Default Marquee Content",
        'user_hint': "Marquee Content to show on all devices, "
                     "unless otherwise configured closer to the device."
    }


class MarqueeStylingPolicy(PolicyBase):
    name = 'marquee_styling'
    context_spec = [
        {'domain': 'interests',
         'interest_type': 'device',
         'inherits_from': 'ancestors'}
    ]
    write_requires = {
        'interest_type': ['fleet', 'platform'],
        'role': 'Device Manager'
    }
    hints = {
        'user_hint': "Styling to use for Marquee display on all devices, "
                     "unless otherwise configured closer to the device",
        'label_text': "Marquee Styling"
    }
    schema = MarqueeStylingTModel


class MarqueeWritePolicy(PolicyBase):
    name = 'marquee_write'
    context_spec = [{'domain': 'interests',
         'interest_type': 'device',
         'inherits_from': 'ancestors'}
    ]
    write_requires = {
        'interest_type': ['fleet', 'platform'],
        'role': 'Device Manager'
    }
    hints = {
        'user_hint': "Whether override of marquee controls at the device "
                     "level is allowed",
        'label_text': "Marquee Write"
    }
    schema = MarqueeWriteTModel


policy_templates = [
    MarqueeDefaultPolicy,
    MarqueeStylingPolicy,
    MarqueeWritePolicy
]
