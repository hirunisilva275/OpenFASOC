# this file contains functions which dynamically create and import cells
import importlib.util
import inspect
import os
import re
from typing import Callable, Union
from pathlib import Path
import tempfile
import run
import relational

from glayout.pdk.mappedpdk import MappedPDK
from glayout.pdk.util.port_utils import PortTree

def get_default_arguments(func: Callable, pdk: MappedPDK) -> dict:
    """Gets default arguments to a function based on its argument types.

    Args:
        func (callable): The function to which default arguments will be added.
        pdk (MappedPDK): If one of the non default args is of type MappedPDK, then this pdk is used for default value

    Returns:
        dict: A dictionary containing default arguments with values based on the argument types of the input function.
    """
    # get args that dont have a default
    argspec = inspect.getfullargspec(func)
    args_with_defaults = argspec.defaults or []
    num_args_without_defaults = len(argspec.args) - len(args_with_defaults)
    args_without_defaults = argspec.args[:num_args_without_defaults]
    # loop through non default args and try to set some value for them
    kwargs = {}
    for arg, arg_type in zip(args_without_defaults, argspec.annotations.values()):
        # pick some default value
        if arg_type == int:
            default_value = 2
        elif arg_type == float:
            default_value = 2.5
        elif arg_type == bool:
            default_value = True
        elif arg_type == str:
            default_value = "met1"
        # hard to guess what a person might want with a tuple, but make it a pair of ints (size) is a safe bet
        elif arg_type == tuple:
            default_value = (1,1)
        # hard to guess what a person might want with a list, but make it a long list of ints is a safe bet
        elif arg_type == list:
            default_value = [1,1,1,1,1,1,1,1,1]
        elif arg_type == MappedPDK:
            default_value = pdk
        else:  # for other types, set default to None
            default_value = None
        # add this argument to the kwargs
        kwargs[arg] = default_value
    return kwargs


def get_funccell_name(glayout_code: str) -> str:
    pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)cell\s*\("
    return re.search(pattern, glayout_code).group().lstrip("def").rstrip("(").strip()

class CodeImportHandler:
    """create, manage, destroy temporary files created as part of dynamic importing
    contains
        self.function (Callable): the function handle
        self.func_name (str): the name of the function imported
        self.temp_module: the imported module handle
    """

    def __init__(self, glayout_code: Union[str, Path]):
        """create temporary file with glayout python code from glayout_code string
        and import the module
        Args:
            glayout_code (str, Path): string containing cell function and imports.
            ****or, string or pathlib.Path: path to a convo file
        """
        # check if this is a code string or a file
        precompiled_code = False
        if isinstance(glayout_code, str):
            if relational.GlayoutCode.HEAD_MARKER in glayout_code:
                precompiled_code = True
        # if this is not a code string, convert NLP file to python code
        if not precompiled_code:
            glayout_code = run.run_session(glayout_code, restore_and_exit=True)
        # figure out what the cell is called
        self.func_name = get_funccell_name(glayout_code)
        pymodule_name = self.func_name.removesuffix("_cell") + ".py"
        # create the cell py module
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir).resolve()
            pythonfile = temp_dir_path / pymodule_name
            with pythonfile.open(mode="w") as pyfile:
                pyfile.write(glayout_code)
            # import the cell
            spec = importlib.util.spec_from_file_location(self.func_name, pythonfile)
            self.temp_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.temp_module)
            self.function = getattr(self.temp_module, self.func_name)



def run_glayout_code_cell(pdk: MappedPDK, glayout_code: str) -> bool:
    """Instantiate a layout from the given glayout cell code and returns Component

    Args:
        pdk (MappedPDK): pdk to instantiate this cell
        glayout_code (str): string containg the cell function and all needed imports

    Returns:
        Component: gdsfactory Component corresponding to the produced layout
    """
    testcell = CodeImportHandler(glayout_code).function
    return testcell(**get_default_arguments(testcell, pdk))


def show_glayout_code_cell(pdk: MappedPDK, glayout_code: str):
    """Instantiate and show a layout from the given glayout cell code

    Args:
        pdk (MappedPDK): pdk to instantiate this cell
        glayout_code (str): string containg the cell function and all needed imports
    """
    run_glayout_code_cell(pdk, glayout_code).show()


def getPortTree_glayout_code_cell(pdk: MappedPDK, glayout_code: str) -> PortTree:
    """return PortTree for a given glayout cell

    Args:
        pdk (MappedPDK): pdk to instantiate this cell
        glayout_code (str): string containg the cell function and all needed imports
    
    Returns PortTree
    """
    return PortTree(run_glayout_code_cell(pdk, glayout_code))

def printPortTree_glayout_code_cell(pdk: MappedPDK, glayout_code: str):
    """return PortTree for a given glayout cell

    Args:
        pdk (MappedPDK): pdk to instantiate this cell
        glayout_code (str): string containg the cell function and all needed imports
    """
    PortTree(run_glayout_code_cell(pdk, glayout_code)).print(depth=6)