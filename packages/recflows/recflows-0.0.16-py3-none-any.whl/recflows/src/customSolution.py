from recflows.resources.solutions import BaseSolution

class customSolution(BaseSolution):
    def __init__(self, id):
        super().__init__()
        self.id = id