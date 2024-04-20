# clamming.clamutils.py
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

from __future__ import annotations
import inspect
import importlib
from typing import Any

# ---------------------------------------------------------------------------


class ClamUtils:
    """Some utilities for Clamming.

    """

    @staticmethod
    def get_class(class_name: str, module_name: str | None = None) -> Any:
        """Return the class matching the given class name or None if invalid.

        :example:
        >>> c = ClamUtils.get_class("ClamsPack", "clamming")
        >>> print(c)
        <class 'clamming.clamspack.ClamsPack'>
        >>> c = ClamUtils.get_class("something", "clamming")
        >>> print(c)
        None

        :param class_name: (str) Name of a class
        :param module_name: (str) Name of the module to search for the class
        :return: (class|None) Class if valid given parameters, or None.

        """
        if module_name is None:
            module_name = __name__
        # Returns None if module with given name can't be imported
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            return None
        # Returns None if class with given name doesn't exist in the module
        class_inst = getattr(module, class_name, None)
        if class_inst is not None and inspect.isclass(class_inst) is False:
            # Returns None if given class_name does not match a valid class
            return None

        return class_inst
