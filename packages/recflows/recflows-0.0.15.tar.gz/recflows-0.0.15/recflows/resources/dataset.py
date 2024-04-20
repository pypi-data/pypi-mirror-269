from recflows.resources.base import BaseResource
from recflows.vars import TABLE_DATASETS

class Dataset(BaseResource):
    def __init__(self, id, app_id, name):
        super().__init__(TABLE_DATASETS, id)
        self.app_id = app_id
        self.name = name

        self.mount_resource({
            "id": self.id,
            "app_id": self.app_id,
            "name": self.name
        })

