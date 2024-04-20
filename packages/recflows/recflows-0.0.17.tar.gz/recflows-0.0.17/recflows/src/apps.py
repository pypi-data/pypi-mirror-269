from recflows.resources.app import App
from recflows.resources.variable import Variable
from recflows.resources.model import Model
from recflows.resources.dataset import Dataset
from recflows.resources.tutorial import Tutorial

from recflows.resources.solutions import LocalCollaborativeFiltering, CloudRunCollaborativeFiltering


a = App("app-a", "App a", "this is a short description about my app")
b = App("app-b", "App b", "this is a short description about my app")
c = App("app-c", "App c", "this is a short description about my app")
d = App("app-d", "App d", "this is a short description about my app")

d1 = Dataset(id="dataset-1", app_id=a.id, name="Dataset-1",)
v = Variable(id="mi-variable-unica", app_id=a.id, key="database_conexion", value="DATABASE_HOST")
t1 = Tutorial(id="tutorial-1", name="Quick Start: Create new application", content="Create you SR in a few steps")
t2 = Tutorial(id="tutorial-2", name="Quick Start: Create Model from Prebuilded Solution", content="Create you SR in a few steps",)
t3 = Tutorial(id="tutorial-3", name="Quick Start: Create Model from Custom Solution (End to End)",
    content=f"""# Hola
* un poco de texto en markdown

```cp /path/to/file```
```js
const x = "mi variable"
```
```python
# my_class.py
class MyClass:
    pass
```
""")

m1 = Model(id="model-1", app_id=a.id, name="LocalCollaborativeFiltering5top_user", solution=LocalCollaborativeFiltering, top_users=5)
m2 = Model(id="model-2", app_id=a.id, name="LocalCollaborativeFiltering10top_user", solution=LocalCollaborativeFiltering, top_users=10)
m3 = Model(id="model-3", app_id=a.id, name="CloudRunCollaborativeFiltering5top_user", solution=CloudRunCollaborativeFiltering, top_users=5)
m4 = Model(id="model-4", app_id=a.id, name="CloudRunCollaborativeFiltering10top_user", solution=CloudRunCollaborativeFiltering, top_users=10)


'''
Tutorial(
    id="tutorial-1",
    name="Quick Start"
    content="Create you SR in a few steps"
)
from recflows.resources.solutions import BaseSolution
from recflows.src.customSolution import customSolution

class App:
    def __init__(self, id):
        self.id = id
    def run(self):
        print("This fuction run in /apps/{self.id}:run")
'''
