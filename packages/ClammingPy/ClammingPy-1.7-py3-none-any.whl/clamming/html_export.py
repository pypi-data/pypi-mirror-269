# clamming.html_export.py
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
from typing import NoReturn

# ---------------------------------------------------------------------------


class HTMLDocExport:
    """Store the options and content for an export to a standalone HTML file.

    HTMLDocExport is a data class, used to store options and content for exporting
    a standalone HTML file. It provides methods to set and get various HTML
    information such as software name, copyright, icon, title, favicon, and
    theme. It also allows setting the names of the next and previous classes
    or modules for generating a table of contents.

    :example:
    >>> h = HTMLDocExport()
    >>> h.software = "Clamming"
    >>> h.theme = "light"
    >>> html_head = h.get_head()
    >>> html_nav = h.get_nav()
    >>> html_footer = h.get_footer()

    """

    # ----------------------------------------------------------------------------
    # Public Constants
    # ----------------------------------------------------------------------------

    HTML_HEAD = \
        """
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes" />
            <title>{TITLE}</title>
            <link rel="logo icon" href="{STATICS}/{FAVICON}" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css/wexa.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css/layout.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css/book.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css/menu.css" type="text/css" />
            <link rel="stylesheet" href="{WEXA_STATICS}/css/code.css" type="text/css" />
            <link rel="stylesheet" href="{STATICS}/clamming.css" type="text/css" />

            <script src="{WEXA_STATICS}/js/purejs-tools/OnLoadManager.js"  type="application/javascript"></script>
            <script src="{WEXA_STATICS}/js/book.js" type="application/javascript"></script>
            <script type="application/javascript">
                OnLoadManager.addLoadFunction(() => {{
                    let book = new Book("main-content");
                    book.fill_table(false);
                }});
            </script>
       </head>
       
       """

    HTML_BUTTON_SKIP = \
        """
                <a role="button" class="skip" href="#main-content" aria-label="Go to main content">
                Go to main content
                </a>
        """

    HTML_FOOTER = \
        """
            <footer>
                <p class="copyright">{COPYRIGHT}</p>
            </footer>
        """

    # ----------------------------------------------------------------------------
    # Customized HTML information
    # ----------------------------------------------------------------------------

    # About the documented software
    DEFAULT_SOFTWARE = ""
    DEFAULT_COPYRIGHT = ""
    DEFAULT_ICON = ""
    DEFAULT_URL = ""

    # For the created HTML pages
    DEFAULT_WEXA_STATICS = "./wexa_statics"
    DEFAULT_STATICS = "./statics"
    DEFAULT_TITLE = ""
    DEFAULT_FAVICON = "clamming32x32.ico"
    DEFAULT_THEME = "light"

    # ----------------------------------------------------------------------------

    def __init__(self):
        """Create an HTML documentation export system for a ClamsPack.

        Main functionalities:

        - Store options and content for exporting a standalone HTML file;
        - Set and get HTML information such as software name, copyright, icon, title, favicon, and theme;
        - Set the names of the next and previous classes or modules for generating a table of contents.

        """

        # HTML information
        self.__software = HTMLDocExport.DEFAULT_SOFTWARE
        self.__copyright = HTMLDocExport.DEFAULT_COPYRIGHT
        self.__url = HTMLDocExport.DEFAULT_URL
        self.__icon = HTMLDocExport.DEFAULT_ICON
        self.__title = HTMLDocExport.DEFAULT_TITLE
        self.__favicon = HTMLDocExport.DEFAULT_FAVICON
        self.__theme = HTMLDocExport.DEFAULT_THEME
        self.__statics = HTMLDocExport.DEFAULT_STATICS
        self.__wexa_statics = HTMLDocExport.DEFAULT_WEXA_STATICS

        # Previous and next class and module names for the TOC
        self.__next_class = None
        self.__prev_class = None
        self.__next_pack = None
        self.__prev_pack = None

    # ----------------------------------------------------------------------------

    def get_software(self) -> str:
        """Return the name of the software."""
        return self.__software

    def set_software(self, name: str = DEFAULT_SOFTWARE) -> NoReturn:
        """Set a software name.

        :param name: (str) Name of the documented software
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.software. Got {} instead."
                            "".format(name))
        self.__software = name

    software = property(get_software, set_software)

    # ----------------------------------------------------------------------------

    def get_url(self) -> str:
        """Return the url of the software."""
        return self.__url

    def set_url(self, name: str = "") -> NoReturn:
        """Set a software url.

        :param name: (str) URL of the documented software
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.url. Got {} instead."
                            "".format(name))
        self.__url = name

    url = property(get_url, set_url)

    # ----------------------------------------------------------------------------

    def get_copyright(self) -> str:
        """Return the copyright of the HTML page."""
        return self.__copyright

    def set_copyright(self, text: str = DEFAULT_COPYRIGHT) -> NoReturn:
        """Set a copyright text, added to the footer of the page.

        :param text: (str) Copyright of the documented software
        :raises: TypeError: Given text is not a string

        """
        if isinstance(text, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.copyright. Got {} instead."
                            "".format(text))
        self.__copyright = text

    copyright = property(get_copyright, set_copyright)

    # ----------------------------------------------------------------------------

    def get_icon(self) -> str:
        """Return the icon filename of the software."""
        return self.__icon

    def set_icon(self, name: str = DEFAULT_ICON) -> NoReturn:
        """Set an icon filename.

        :param name: (str) Filename of the icon of the documented software
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.icon. Got {} instead."
                            "".format(name))
        self.__icon = name

    icon = property(get_icon, set_icon)

    # ----------------------------------------------------------------------------

    def get_title(self) -> str:
        """Return the title of the HTML page."""
        return self.__title

    def set_title(self, text: str = DEFAULT_TITLE) -> NoReturn:
        """Set a title to the output HTML pages.

        :param text: (str) Title of the HTML pages
        :raises: TypeError: Given text is not a string

        """
        if isinstance(text, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.title. Got {} instead."
                            "".format(text))
        self.__title = text

    title = property(get_title, set_title)

    # ----------------------------------------------------------------------------

    def get_statics(self) -> str:
        """Return the static path of the CSS, JS, etc."""
        return self.__statics

    def set_statics(self, name: str = DEFAULT_STATICS) -> NoReturn:
        """Set the static path of the customs CSS, JS, etc.

        :param name: (str) Path of the static elements
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.statics. Got {} instead."
                            "".format(name))
        self.__statics = name

    statics = property(get_statics, set_statics)

    # ----------------------------------------------------------------------------

    def get_wexa_statics(self) -> str:
        """Return the static path of the CSS, JS, etc. of Whakerexa. """
        return self.__wexa_statics

    def set_wexa_statics(self, name: str = DEFAULT_WEXA_STATICS) -> NoReturn:
        """Set the static path of the customs CSS, JS, etc. of Whakerexa.

        :param name: (str) Path of the static elements
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.wexa_statics. Got {} instead."
                            "".format(name))
        self.__wexa_statics = name

    wexa_statics = property(get_wexa_statics, set_wexa_statics)

    # ----------------------------------------------------------------------------

    def get_favicon(self) -> str:
        """Return the favicon filename of the HTML pages."""
        return self.__favicon

    def set_favicon(self, name: str = DEFAULT_FAVICON) -> NoReturn:
        """Set a favicon to the output HTML pages.

        :param name: (str) Favicon of the HTML pages
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.favicon. Got {} instead."
                            "".format(name))
        self.__favicon = name

    favicon = property(get_favicon, set_favicon)

    # ----------------------------------------------------------------------------

    def get_theme(self) -> str:
        """Return the theme of the HTML page."""
        return self.__theme

    def set_theme(self, name: str = DEFAULT_THEME) -> NoReturn:
        """Set a theme name.

        :param name: (str) Name of the theme of the HTML pages
        :raises: TypeError: Given name is not a string

        """
        if isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' for the HTMLDocExport.theme. Got {} instead."
                            "".format(name))
        self.__theme = name

    theme = property(get_theme, set_theme)

    # ----------------------------------------------------------------------------

    def get_next_class(self) -> str:
        """Return the name of the next documented class."""
        return self.__next_class

    def set_next_class(self, name: str | None = None) -> NoReturn:
        """Set the name of the next documented class.

        :param name: (str|None) Name of the next documented class
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.next_class. Got {} instead."
                            "".format(name))
        self.__next_class = name

    next_class = property(get_next_class, set_next_class)

    # ----------------------------------------------------------------------------

    def get_prev_class(self) -> str:
        """Return the name of the previous documented class, for the ToC."""
        return self.__prev_class

    def set_prev_class(self, name: str | None = None) -> NoReturn:
        """Set the name of the previous documented class.

        :param name: (str|None) Name of the previous documented class
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.prev_class. "
                            "Got {} instead.".format(name))
        self.__prev_class = name

    prev_class = property(get_prev_class, set_prev_class)

    # ----------------------------------------------------------------------------

    def get_next_module(self) -> str:
        """Return the name of the next documented module."""
        return self.__next_pack

    def set_next_module(self, name: str | None = None) -> NoReturn:
        """Set the name of the next documented module.

        :param name: (str|None) Name of the next documented module
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.next_module. "
                            "Got {} instead.".format(name))
        self.__next_pack = name

    next_module = property(get_next_module, set_next_module)

    # ----------------------------------------------------------------------------

    def get_prev_module(self) -> str:
        """Return the name of the previous documented module, for the ToC."""
        return self.__prev_pack

    def set_prev_module(self, name: str | None = None) -> NoReturn:
        """Set the name of the previous documented module.

        :param name: (str|None) Name of the previous documented module
        :raises: TypeError: Given name is not a string

        """
        if name is not None and isinstance(name, (str, bytes)) is False:
            raise TypeError("Expected a 'str' or None for the HTMLDocExport.prev_module. "
                            "Got {} instead.".format(name))
        self.__prev_pack = name

    prev_module = property(get_prev_module, set_prev_module)

    # ----------------------------------------------------------------------------
    # Export of the HTML contents
    # ----------------------------------------------------------------------------

    def get_head(self) -> str:
        """Return the HTML 'head' of the page."""
        return HTMLDocExport.HTML_HEAD.format(
            TITLE=self.__title,
            FAVICON=self.__favicon,
            THEME=self.__theme,
            STATICS=self.__statics,
            WEXA_STATICS=self.__wexa_statics
        )

    # ----------------------------------------------------------------------------

    def get_header(self) -> str:
        """Return the 'header' of the HTML->body of the page."""
        h = list()
        h.append("    <header>")
        h.append(HTMLDocExport.HTML_BUTTON_SKIP)
        if len(self.__software) > 0:
            h.append("    <h1>{SOFTWARE}</h1>".format(SOFTWARE=self.__software))
        if len(self.__icon) > 0:
            h.append('        <p><img class="small-logo" src="{STATICS}/{ICON}" '
                     'alt="Software logo"/></p>'.format(STATICS=self.__statics, ICON=self.__icon))
        if len(self.__url) > 0:
            h.append('        <p><a class="external-link" href="{URL}">{URL}</a></p>'.format(URL=self.__url))
        h.append("    </header>")
        return "\n".join(h)

    # ----------------------------------------------------------------------------

    def get_nav(self) -> str:
        """Return the 'nav' of the HTML->body of the page."""
        nav = list()
        nav.append("<nav id=\"nav-book\" class=\"side-nav\">")
        if self.__software == HTMLDocExport.DEFAULT_SOFTWARE:
            nav.append("    <h1>Documentation</h1>")
        else:
            nav.append("    <h1>{SOFTWARE}</h1>".format(SOFTWARE=self.__software))
        if len(self.__icon) > 0:
            nav.append("    <img class=\"small-logo center\" src=\"{STATICS}/{ICON}\" alt=\"\"/>"
                       "".format(STATICS=self.__statics, ICON=self.__icon))
        if len(self.__url) > 0:
            nav.append('        <p><a class="external-link" href="{URL}">{URL}</a></p>'.format(URL=self.__url))
        nav.append("    <ul>")
        nav.append(HTMLDocExport.__nav_link("&crarr; Prev. Module", self.__prev_pack))
        nav.append(HTMLDocExport.__nav_link("&uarr; Prev. Class", self.__prev_class))
        nav.append(HTMLDocExport.__nav_link("&#8962; Index", "index.html"))
        nav.append(HTMLDocExport.__nav_link("&darr; Next Class", self.__next_class))
        nav.append(HTMLDocExport.__nav_link("&rdsh; Next Module", self.__next_pack))
        nav.append("    </ul>")
        nav.append("    <h2>Table of Contents</h2>")
        nav.append("    <ul id=\"toc\"></ul>")
        nav.append("    <hr>")
        nav.append("    <p><small>Automatically created</small></p><p><small>by <a class=\"external-link\" href=\"https://clamming.sf.net\">Clamming</a></small></p>")
        nav.append("</nav>")
        return "\n".join(nav)

    # -----------------------------------------------------------------------

    def get_footer(self) -> str:
        """Return the 'footer' of the HTML->body of the page."""
        return HTMLDocExport.HTML_FOOTER.format(COPYRIGHT=self.__copyright)

    # -----------------------------------------------------------------------
    # Private
    # -----------------------------------------------------------------------

    @staticmethod
    def __nav_link(text: str, link: str | None) -> str:
        if link is None:
            a = 'aria-disabled="true"'
        else:
            a = 'href="{:s}"'.format(link)
        return """<li><a role="button" tabindex="0" {LINK}> {TEXT}</a></li>""".format(LINK=a, TEXT=text)
