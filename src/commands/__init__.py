import importlib
import pkgutil
import logging

__all__ = []

def recursive_import(module_name, module_path):
    for module_info in pkgutil.iter_modules(module_path, prefix=module_name + "."):
        submodule_name = module_info.name
        try:
            module = importlib.import_module(submodule_name)

            command_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "run"):
                    command_class = attr
                    break

            if command_class:
                __all__.append(submodule_name) 

        except Exception as e:
            logging.warning(f"Error importing {submodule_name}: {e}")


for module_info in pkgutil.iter_modules(__path__, prefix=__name__ + "."):
    module_name = module_info.name
    try:
        module = importlib.import_module(module_name)

        command_class = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, "run"):
                command_class = attr
                break

        if command_class:
            __all__.append(module_name)

        if hasattr(module, "__path__"):
            recursive_import(module_name, module.__path__)

    except Exception as e:
        logging.warning(f"Error importing {module_name}: {e}")

