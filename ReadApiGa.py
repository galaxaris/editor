import os
import sys
import inspect
import importlib


def get_placeable(type_: str):
    results = {}

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    api_path = os.path.join(project_root, "api" if type_ == "class" else "game")

    for root, dirs, files in os.walk(api_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                full_path = os.path.join(root, file)

                rel_path = os.path.relpath(full_path, project_root)
                module_name = rel_path.replace(os.sep, ".").removesuffix(".py")

                try:
                    module = importlib.import_module(module_name)

                    importlib.reload(module)

                    if type_ == "class":
                        for name, obj in inspect.getmembers(module, inspect.isclass):
                            if obj.__module__ == module_name:

                                tags = getattr(obj, "_EDITOR", set())
                                if "placeable" in tags:
                                    results[name] = {"params": get_params(obj, "class"),"class_ref": obj}
                    else:
                        for name, obj in inspect.getmembers(module, inspect.isfunction):
                            if obj.__module__ == module_name:

                                tags = getattr(obj, "_EDITOR", set())
                                if not "not_callable" in tags:
                                    results[name] = {"params": get_params(obj, "class"), "class_ref": obj}

                except Exception as e:
                    print(f"Erreur sur {module_name} : {e}")

    return results

def get_params(obj, type_: str) -> list:
    if type_ == "class":
        init_sig = inspect.signature(obj.__init__)
    else:
        init_sig = inspect.signature(obj)

    params = []

    for p_name, p_obj in init_sig.parameters.items():
        if type_ == "class" and p_name in ('self', 'args', 'kwargs', 'pos'):
            continue

        if p_obj.annotation is inspect.Parameter.empty:
            p_type = "Any"

        else:
            p_type = str(p_obj.annotation).replace("class", "").strip("<").strip(">").strip().strip("'")

        p_default = p_obj.default if p_obj.default is not inspect.Parameter.empty else "&ToFill"

        params.append(Param(p_name, p_type, p_default))

    return params

class Param:
    def __init__(self, name: str, type_: str, default_val: str = "#ToFill"):
        self.name = name
        self.type_ = type_
        self.default_val = default_val
        self.val = None
        self.many_types = []
        self.analyse_type()

    def analyse_type(self):
        types = self.type_.strip().split("|")
        self.type_ = types[0].strip()

        for type_ in types:
            if any(word in type_ for word in ["tuple", "list"]):

                type_name, separator, after = type_.partition("[")

                if separator:
                    intern_type, separator, _ = after.partition("]")

                else:
                    intern_type = type_

                values = intern_type.split(",")
                self.many_types.append({"val": values, "count": len(values)})

            elif type_ == "pygame.Vector2":
                self.many_types.append({"val":("float", "float"), "count":2})

            else:
                print("TYPE", self.type_)
                self.many_types.append({"val": None, "count": 0})
