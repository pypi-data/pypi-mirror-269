# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of Tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
SXM Media Content Options
=========================
"""


from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__)

depends = ['tendril.config.media']

config_elements_sxm_content = [
    ConfigOption(
        'DEVICE_CONTENT_TYPES_ALLOWED',
        "['media', 'structured', 'sequence']",
        "List of media types allowed for device content.",
        parser=set,
    ),
    ConfigOption(
        'ADVERTISEMENT_TYPES_ALLOWED',
        "['media']",
        "List of media types allowed for advertisements.",
        parser=set
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_sxm_content,
                          doc="SXM Content Libraries Configuration")
