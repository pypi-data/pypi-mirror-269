from recflows.resources.base import BaseResource
from recflows.vars import TABLE_SOLUTIONS


class BaseSolution(BaseResource):
    def __init__(self):
        super().__init__(TABLE_SOLUTIONS, self.__class__.__name__)
        self.module = self.__class__.__module__

        self.mount_resource({
            "id": self.id,
            "module": self.module,
        })

    def preprocessing(self):
        raise Exception("Function 'preprocessing' wasn't implemented")

    def compile(self):
        raise Exception("Function 'compile' wasn't implemented")

    def fit(self):
        raise Exception("Function 'fit' wasn't implemented")

    def predict(self):
        raise Exception("Function 'predict' wasn't implemented")

    def show(self):
        raise Exception("Function 'show' wasn't implemented")

    def deploy(self):
        raise Exception("Function 'deploy' wasn't implemented")
