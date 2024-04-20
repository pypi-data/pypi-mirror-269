from .BaseSolution import  BaseSolution
from recflows.resources.tutorial import Tutorial


class LocalCollaborativeFiltering(BaseSolution):
    def __init__(self, top_users):
        super().__init__()
        self.top_users = top_users
        self.tutorials = [
            Tutorial(
                id="LocalCollaborativeFiltering-tutorial-1",
                name="Quick Start 1: Create LocalCollaborativeFiltering from Prebuilded Solution",
                content="Create you LocalCollaborativeFiltering SR in a few steps",
                solution_id=self.id,
            ),
            Tutorial(
                id="LocalCollaborativeFiltering-tutorial-2",
                name="Quick Start 2: Create LocalCollaborativeFiltering from Prebuilded Solution",
                content="Create you LocalCollaborativeFiltering SR in a few steps",
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
