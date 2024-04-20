# clamming.clamspack.py
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
import codecs
import os
import logging
from typing import Any

import clamming
from clamming.clamsclass import ClamsClass
from clamming.classparser import ClammingClassParser
from clamming.html_export import HTMLDocExport
from clamming.clamutils import ClamUtils

# ---------------------------------------------------------------------------


class ClamsPack:
    """Create documentation of a module into Markdown or HTML.

    :example:
    >>> clams = ClamsPack(clamming)
    >>> md = clams.markdown()

    """

    def __init__(self, pack: Any):
        """Create documentation from the given package name.

        :param pack: (module) A Python module
        :raises: TypeError: given 'pack' is not a module

        """
        if inspect.ismodule(pack) is False:
            raise TypeError("Expected a Python module. Got {:s} instead.".format(str(pack)))

        self.__name = pack.__name__
        self.__clams = list()
        try:
            for class_name in pack.__all__:
                # Turn class_name into an instance name
                class_inst = ClamUtils.get_class(class_name, self.__name)
                if class_inst is not None:
                    # Parse the object and store collected information = clamming
                    clammer = ClammingClassParser(class_inst)
                    # Store the collected clams
                    self.__clams.append(ClamsClass(clammer))
        except AttributeError:
            logging.warning("Attribute __all__ is missing in package {:s} => No auto documentation."
                            "".format(self.__name))

    # -----------------------------------------------------------------------

    def get_name(self) -> str:
        """Return the name of the package."""
        return self.__name

    name = property(get_name, None)

    # -----------------------------------------------------------------------

    def markdown(self) -> str:
        """Return the documentation of the package as a standalone Markdown content."""
        md = list()
        md.append("## Package `{:s}`\n".format(self.__name))
        for clams in self.__clams:
            md.append(clams.markdown())
        md.append("\n\n~ Created using [Clamming](https://clamming.sf.net) version {:s} ~\n"
                  "".format(clamming.__version__))

        return "\n".join(md)

    # -----------------------------------------------------------------------

    def html(self) -> str:
        """Return the documentation of the package as an HTML content."""
        html = list()
        html.append("<h1> Package `{:s}` </h1>\n".format(self.__name))
        for clams in self.__clams:
            html.append(clams.html())
        html.append("\n\n<p>~ Created using <a href=\"https://clamming.sf.net\">Clamming</a> version {:s} ~</p>\n"
                    "".format(clamming.__version__))
        return "\n".join(html)

    # -----------------------------------------------------------------------

    def html_index(self, path_name: str | None = None) -> str:
        """Create the HTML content of an index for the package.

        :param path_name: (str) Path where the exported HTML files are, or None for a standalone content.
        :return: (str) HTML code

        """
        out = list()
        out.append("    <section id=\"#{:s}\">".format(self.__name))
        out.append("    <h1>Module {:s}</h1>".format(self.__name))
        out.append('        <section class="cards-panel">')

        for i in range(len(self.__clams)):
            clams = self.__clams[i]
            out.append('        <article class="card">')
            out.append('            <header><span>{:d}</span></header>'.format(i + 1))
            out.append('            <main>')
            out.append('                <h3>{:s}</h3>'.format(clams.name))
            out.append('            </main>')
            out.append('            <footer>')
            if path_name is not None:
                # External link
                out.append('                <a role="button" href="{:s}">Read me →</a>'
                           ''.format(os.path.join(path_name, clams.name + ".html")))
            else:
                # Local link
                out.append('                <a role="button" href="#{:s}">Read me →</a>'
                           ''.format(clams.name))
            out.append('            </footer>')
            out.append('        </article>')

        out.append("        </section>")
        out.append("    </section>")

        return "\n".join(out)

    # -----------------------------------------------------------------------

    def html_export_clams(self, path_name: str, html_exporter: HTMLDocExport) -> list[str]:
        """Create the HTML pages of all classes of the package.

        :param path_name: (str) Path where to add the exported HTML files
        :param html_exporter: (HTMLDocExport) Options for HTML output files
        :return: (list) Exported file names

        """
        out_html = os.path.join(path_name, self.__name + ".html")
        if os.path.exists(path_name) is False:
            os.mkdir(path_name)

        with codecs.open(out_html, "w", "utf-8") as fp:
            fp.write("<!DOCTYPE html>\n")
            fp.write("<html>\n")
            fp.write(html_exporter.get_head())
            fp.write("<body class=\"{:s}\">\n".format(html_exporter.get_theme()))
            fp.write("    {:s}\n".format(html_exporter.get_header()))
            fp.write("    {:s}\n".format(html_exporter.get_nav()))
            fp.write("    <main id=\"main-content\" class=\"toc-shift\">\n")
            fp.write("    <div id=\"toc-content\">\n")
            fp.write(self.html_index(path_name=""))
            fp.write("    </div>\n")
            fp.write("    </main>\n")
            fp.write("    {:s}\n".format(html_exporter.get_footer()))
            fp.write("</body>\n")
            fp.write("</html>\n")

        out = list()
        out.append(out_html)

        for i in range(len(self.__clams)):
            clams = self.__clams[i]
            out_html = os.path.join(path_name, clams.name + ".html")
            logging.info("Export {:s}".format(out_html))

            html_exporter.prev_class = None if i == 0 else self.__clams[i - 1].name + ".html"
            html_exporter.next_class = None if i + 1 == len(self.__clams) else self.__clams[i + 1].name + ".html"
            html_content = clams.html()

            with codecs.open(out_html, "w", "utf-8") as fp:
                fp.write("<!DOCTYPE html>\n")
                fp.write("<html>\n")
                fp.write(html_exporter.get_head())
                fp.write("<body class=\"{:s}\">\n".format(html_exporter.get_theme()))
                fp.write("    {:s}\n".format(html_exporter.get_header()))
                fp.write("    {:s}\n".format(html_exporter.get_nav()))
                fp.write("    <main id=\"main-content\" class=\"toc-shift\">\n")
                fp.write("    <div id=\"toc-content\">\n")
                fp.write("    <section id=\"#{:s}\">".format(self.__name))
                fp.write("    <h1>Module {:s}</h1>\n".format(self.__name))
                fp.write(html_content)
                fp.write("    </section>")
                fp.write("    </div>\n")
                fp.write("    </main>\n")
                fp.write("    {:s}\n".format(html_exporter.get_footer()))
                fp.write("</body>\n")
                fp.write("</html>\n")

        return out

    # -----------------------------------------------------------------------
    # Documentation for a list of modules.
    # -----------------------------------------------------------------------

    @staticmethod
    def markdown_export_packages(clams_packs: list[ClamsPack], path_name: str, html_exporter: HTMLDocExport) -> list[str]:
        """Create a Markdown file for each of the given packages.

        :param clams_packs: (list) List of ClamsPack
        :param path_name: (str) Path where to add the exported md files
        :param html_exporter: (HTMLDocExport) Options for output files
        :return: (list) Exported file names

        """
        out = list()

        for clams_pack in clams_packs:
            out_md = os.path.join(path_name, clams_pack.name + ".md")
            if os.path.exists(path_name) is False:
                os.mkdir(path_name)

            logging.info("Export {:s}".format(out_md))
            with codecs.open(out_md, "w", "utf-8") as fp:
                fp.write(clams_pack.markdown())
            out.append(out_md)

        return out

    # -----------------------------------------------------------------------

    @staticmethod
    def html_export_index(clams_packs: list[ClamsPack], path_name: str, html_exporter: HTMLDocExport) -> str:
        """Write the index.html file from the given list of packages.

        :param clams_packs: (list) List of ClamsPack
        :param path_name: (str) Path where to add the exported index.html file
        :param html_exporter: (HTMLDocExport) Options for HTML output files
        :return: (str) Filename of the created HTML index file

        """
        out = os.path.join(path_name, "index.html")
        if os.path.exists(path_name) is False:
            os.mkdir(path_name)

        with codecs.open(out, "w", "utf-8") as fp:
            fp.write("<!DOCTYPE html>\n")
            fp.write("<html>\n")
            fp.write(html_exporter.get_head())
            fp.write("<body class=\"{:s}\">\n".format(html_exporter.get_theme()))
            fp.write("    {:s}\n".format(html_exporter.get_header()))
            fp.write("    {:s}\n".format(html_exporter.get_nav()))
            fp.write("    <main id=\"main-content\" class=\"toc-shift\">\n")
            fp.write("    <div id=\"toc-content\">\n")
            for clams_pack in clams_packs:
                # path_name argument is a relative path of the pages to the index
                fp.write(clams_pack.html_index(path_name="."))
            fp.write("    </div>\n")
            fp.write("    </main>\n")
            fp.write("    {:s}\n".format(html_exporter.get_footer()))
            fp.write("</body>\n")
            fp.write("</html>\n")
        return out

    # -----------------------------------------------------------------------

    @staticmethod
    def html_export_packages(clams_packs: list[ClamsPack], path_name: str, html_exporter: HTMLDocExport) -> list:
        """Create all the HTML files from the given list of packages.

        - create the HTML file for each class of each given module;
        - create an index.html file.

        :param clams_packs: (list) List of ClamsPack
        :param path_name: (str) Path where to add the exported index.html file
        :param html_exporter: (HTMLDocExport) Options for HTML output files

        """
        out = list()

        # Create the index.html page. It's a table of content.
        out_index = ClamsPack.html_export_index(clams_packs, path_name, html_exporter)
        out.append(out_index)

        # Create an HTML page for each class of each module
        for i in range(len(clams_packs)):
            clams_pack = clams_packs[i]
            html_exporter.prev_module = None if i == 0 else clams_packs[i - 1].name + ".html"
            html_exporter.next_module = None if i + 1 == len(clams_packs) else clams_packs[i + 1].name + ".html"
            out_html = clams_pack.html_export_clams(path_name, html_exporter)
            out.extend(out_html)

        return out

    # ---------------------------------------------------------------------------
    # Overloads
    # ---------------------------------------------------------------------------

    def __len__(self):
        """Return the number of documented pages of the package."""
        return len(self.__clams)
