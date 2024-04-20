from recflows.resources.base import BaseResource
from recflows.vars import TABLE_MODELS
from json import dumps


class Model(BaseResource):
    def __init__(self, id, app_id, name, solution, **kwargs):
        self.solution = solution(**kwargs)
        super().__init__(TABLE_MODELS, id)
        self.app_id = app_id
        self.name = name

        self.mount_resource({
            "id": self.id,
            "app_id": self.app_id,
            "solution_id": self.solution.id,
            "name": self.name,
            "kwargs": dumps(kwargs)
        })
