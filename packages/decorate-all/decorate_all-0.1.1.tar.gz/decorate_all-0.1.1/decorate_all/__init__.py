import sys
from types import FunctionType


def decorate_all_functions(decorator: FunctionType, module_name: str):
    """Apply the given decorator to all loaded functions in the given module.

    Args:
        decorator (FunctionType): the decorator to apply to functions
        module_name (str): the name of the module to apply the decorator to
    """
    module = sys.modules[module_name]
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, FunctionType):
            setattr(module, name, decorator(obj))
