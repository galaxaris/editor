import os
import sys
import inspect
import importlib


def get_placeable_classes():
    results = {}

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    api_path = os.path.join(project_root, "api")

    for root, dirs, files in os.walk(api_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                full_path = os.path.join(root, file)

                rel_path = os.path.relpath(full_path, project_root)
                module_name = rel_path.replace(os.sep, ".").removesuffix(".py")

                try:
                    module = importlib.import_module(module_name)

                    importlib.reload(module)


                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if obj.__module__ == module_name:

                            tags = getattr(obj, "_EDITOR", set())
                            if "placeable" in tags:
                                results[name] = {"params": get_build_params(obj),"class_ref": obj}
                except Exception as e:
                    print(f"Erreur sur {module_name} : {e}")

    return results

def get_build_params(obj):
    init_sig = inspect.signature(obj.__init__)
    params = {
        p_name: p_obj.default if p_obj.default is not inspect.Parameter.empty else "&ToFill"
        for p_name, p_obj in init_sig.parameters.items()
        if p_name != 'self'  # we don't want self because it is useless
    }

    return params