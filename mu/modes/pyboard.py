"""
A mode for working with MicroPython Pyboards.

Copyright (c) 2015-2020 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import ctypes
from subprocess import check_output
from mu.modes.base import MicroPythonMode
from mu.modes.api import SHARED_APIS


class PyBoardMode(MicroPythonMode):
    """
    Represents the functionality required by the PyBoard mode.
    """

    name = ("PyBoard")
    description = ("Write code for PyBoards.")
    icon = "pyboard"
    save_timeout = 0
    valid_boards = [
        (0xf055, 0x9801),  # PYBv1.0
        (0xf055, 0x9800),  # PYBD
    ]
    # Modules built into MicroPython which mustn't be used as file names
    # for source code.
    module_names = {
        "storage",
        "os",
        "touchio",
        "microcontroller",
        "bitbangio",
        "digitalio",
        "audiobusio",
        "multiterminal",
        "nvm",
        "pulseio",
        "usb_hid",
        "analogio",
        "time",
        "busio",
        "random",
        "audioio",
        "sys",
        "math",
        "builtins",
    }

    def actions(self):
        """
                Return an ordered list of actions provided by this module. An action
                is a name (also used to identify the icon) , description, and handler.
                """
        buttons = [
            {
                "name": "serial",
                "display_name": _("Serial"),
                "description": _("Open a serial connection to your device."),
                "handler": self.toggle_repl,
                "shortcut": "CTRL+Shift+U",
            }
        ]
        return buttons

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS
