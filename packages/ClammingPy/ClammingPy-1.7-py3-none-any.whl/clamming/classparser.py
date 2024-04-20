# clamming.classparser.py
#
# This file is part of ClammingPy tool.
# (C) 2023-2024 Brigitte Bigi, Laboratoire Parole et Langage,
# Aix-en-Provence, France.
#
# Use of this software is governed by the GNU Public License, version 3.
#
# ClammingPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ClammingPy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClammingPy. If not, see <http://www.gnu.org/licenses/>.
#
# This banner notice must not be removed.
# ---------------------------------------------------------------------------

# Python standard libraries
import inspect
import ast
import textwrap
from typing import Any

# Clamming
from .claminfo import ClamInfo

# ----------------------------------------------------------------------------


class ClammingClassParser:
    """Inspect a python class and store relevant information for further doc.

    """

    def __init__(self, obj: Any):
        """Create lists of ClamInfo from a given Python object.

        List of public members:

        - obj_clams (ClamInfo): describes the object. It has a name and a docstring.
        - init_clams (ClamInfo): describes the constructor of the object, if the object does.
        - fct_clams (list of ClamInfo): describes all the functions of the object.

        :param obj: Any class object; its source code must be available.
        :raises TypeError: if the object is not a class.
        :raises TypeError: if the object is a built-in class.

        """
        # Get the text of the source code for an object
        if isinstance(obj, object) is False:
            raise TypeError("Expected a class object for clamming.")
        try:
            self.__obj_src = textwrap.dedent(inspect.getsource(obj))
            #self.__obj_src = inspect.getsource(obj)
            self.__obj = obj
        except TypeError:
            raise TypeError("Expected a class object for clamming but not a built-in one.")

        # Parse and store the information of the class
        self.obj_clams = self._inspect_class()
        self.init_clams = self._inspect_constructor()

        # Parse and store all the documented functions, with their arguments,
        # docstrings and source code
        self.fct_clams = self._inspect_functions()

    # -----------------------------------------------------------------------

    def _inspect_class(self) -> ClamInfo:
        """Inspect constructor of the given object.

        """
        class_name = self.__obj.__name__
        tree = ast.parse(self.__obj_src)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                return ClamInfo(class_name, [], "", ast.get_docstring(node))

        return ClamInfo(class_name, [], "", None)

    # -----------------------------------------------------------------------

    def _inspect_constructor(self) -> ClamInfo:
        """Inspect constructor of the given object.

        """
        try:
            # Get the source code of the Python object into str.
            #init_src = inspect.getsource(self.__obj.__init__)
            init_src = textwrap.dedent(inspect.getsource(self.__obj.__init__))
        except OSError:
            # There's no constructor for the given object.
            return ClamInfo("")
        except TypeError:
            # There's a different constructor for the given object.
            return ClamInfo("")

        # Store arguments, source code and docstring
        init_tree = ast.parse(textwrap.dedent(init_src))
        init_args = list()
        init_src = ""
        init_doc = None
        for node in ast.walk(init_tree):
            if isinstance(node, ast.FunctionDef):
                init_args = [arg.arg for arg in node.args.args]
                init_src = ast.unparse(node)
                init_doc = ast.get_docstring(node)
                break
        return ClamInfo(node.name, init_args, init_src, init_doc)

    # -----------------------------------------------------------------------

    def _inspect_functions(self) -> dict:
        """Inspect the documented functions of the given object.

        :return: (dict) key=function name, value=ClamInfo()

        """
        fct_infos = dict()
        tree = ast.parse(self.__obj_src)
        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                # Ignore class constructor
                if name in ("__init__", "__new__"):
                    continue
                # Store the function definition
                fct_infos[name] = ClamInfo(
                    name,
                    [arg.arg for arg in node.args.args],
                    ast.unparse(node),
                    ast.get_docstring(node))

        return fct_infos
