from importlib import import_module
import pkgutil


def load_moduls_from_dir(dir_path: str):
    package = import_module(dir_path)

    for _, modul_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        import_module(modul_name)

def load_src():
    load_moduls_from_dir("recflows.src")
