from recflows.resources.base import BaseResource
from recflows.vars import TABLE_APPS

class App(BaseResource):
    def __init__(self, id, name, description):
        super().__init__(TABLE_APPS, id)
        self.name = name
        self.description = description

        self.mount_resource({
            "id": self.id,
            "name": self.name,
            "description": self.description
        })
