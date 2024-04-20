from recflows.services.database import read_resource_by_id, insert_resouce, update_resouce


class BaseResource:
    def __init__(self, table, id):
        self.table = table
        self.id = id

    def mount_resource(self, record):

        if read_resource_by_id(self.table, record["id"]):
            update_resouce(self.table, record)
        else:
            insert_resouce(self.table, record)
