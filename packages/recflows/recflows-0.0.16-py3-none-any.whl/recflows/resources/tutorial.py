from recflows.resources.base import BaseResource
from recflows.vars import TABLE_TUTORIALS


class Tutorial(BaseResource):
    def __init__(self, id, name, content, solution_id=None):
        super().__init__(TABLE_TUTORIALS, id)
        self.solution_id = solution_id
        self.name = name
        self.content = content

        self.mount_resource({
            "id": self.id,
            "solution_id": self.solution_id,
            "name": self.name,
            "content": self.content,
        })
