from recflows.resources.base import BaseResource
from recflows.vars import TABLE_VARIABLES
from recflows.utils.encryption import encrypt_key
import os


class Variable(BaseResource):
    def __init__(self, id, key, value, app_id=None):
        super().__init__(TABLE_VARIABLES, id)
        self.app_id = app_id
        self.key = key
        self.value = value

        self.mount_resource({
            "id": self.id,
            "app_id": self.app_id,
            "key": self.key,
            "value": encrypt_key.encrypt(os.environ.get(self.value).encode()),
        })
