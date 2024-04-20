from .BaseSolution import  BaseSolution
from recflows.resources.tutorial import Tutorial


class CloudRunCollaborativeFiltering(BaseSolution):
    def __init__(self, top_users):
        super().__init__()
        self.top_users = top_users
        self.tutorials = [
            Tutorial(
                id="CloudRunCollaborativeFiltering-tutorial-1",
                name="Quick Start 1: Create CloudRunCollaborativeFiltering from Prebuilded Solution",
                content="Create you CloudRunCollaborativeFiltering SR in a few steps",
                solution_id=self.id,
            ),
            Tutorial(
                id="CloudRunCollaborativeFiltering-tutorial-2",
                name="Quick Start 2: Create CloudRunCollaborativeFiltering from Prebuilded Solution",
                content="Create you CloudRunCollaborativeFiltering SR in a few steps",
                solution_id=self.id,
            )
        ]

    def preprocessing(self):
        pass

    def compile(self):
        pass

    def fit(self):
        pass

    def predict(self):
        pass

    def show(self):
        pass

    def deploy(self):
        pass
