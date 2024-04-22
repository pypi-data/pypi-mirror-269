

from typing import Any
from typing import List
from typing import Literal
from typing import Optional

from tendril.interests.base import InterestBase
from tendril.interests.base import InterestBaseCreateTModel
from tendril.interests.base import InterestBaseEditTModel

from tendril.db.models.content_providers import ContentProviderModel
from tendril.utils.pydantic import TendrilTBaseModel

from tendril.common.states import LifecycleStatus
from tendril.authz.roles.interests import require_state
from tendril.authz.roles.interests import require_permission
from tendril.common.interests.representations import ExportLevel

from tendril.interests.mixins.policies import InterestPoliciesMixin

from tendril.utils.db import with_db
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


class ArgSpecTModel(TendrilTBaseModel):
    name: str
    type: Optional[str]
    hint: Optional[Any]


class ContentProviderCreateTModel(InterestBaseCreateTModel):
    type: Literal['content_provider']
    path: str
    args: Optional[List[ArgSpecTModel]]
    requires_app: str


class ContentProviderEditTModel(InterestBaseEditTModel):
    path: Optional[str]
    requires_app: Optional[str]


class ContentProvider(InterestPoliciesMixin,
                      InterestBase):
    model = ContentProviderModel
    tmodel_create = ContentProviderCreateTModel
    tmodel_edit = ContentProviderEditTModel

    additional_fields = [
        'path',
        ('args', ExportLevel.NORMAL, Optional[List[ArgSpecTModel]], [], {}),
        'requires_app']

    def __init__(self, *args, path=None, iargs=None, requires_app=None, **kwargs):
        self._path = path
        self._args = iargs or []
        self._requires_app = requires_app
        super(ContentProvider, self).__init__(*args, **kwargs)

    @property
    def path(self):
        if self._path:
            return self._path
        else:
            return self._model_instance.path

    @property
    def args(self):
        if self._args:
            return self._args
        else:
            return self._model_instance.args

    @property
    def requires_app(self):
        if self._requires_app:
            return self._requires_app
        else:
            return self._model_instance.requires_app

    @with_db
    @require_state(LifecycleStatus.ACTIVE)
    @require_permission('read', strip_auth=False)
    def generate(self, args, auth_user=None, session=None):

        vargs = {}
        for argspec in self.args['args']:
            if argspec['name'] in args.keys():
                v = args[argspec['name']]
                assert isinstance(v, eval(argspec['type']))
                if argspec['hint']:
                    pass
                vargs[argspec['name']] = args.pop(argspec['name'])

        if len(args):
            raise ValueError(f"Unknown arguments provided : {args}")

        return {
            'path': self.path,
            'args': vargs
        }


def load(manager):
    manager.register_interest_type('ContentProvider', ContentProvider)
