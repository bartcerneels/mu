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
import logging
from mu.modes.base import MicroPythonMode
from mu.modes.api import SHARED_APIS

logger = logging.getLogger(__name__)


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
                "name": "run",
                "display_name": _("Run"),
                "description": _(
                    "Run your code directly on the pyboard"
                    " via the REPL."
                ),
                "handler": self.run,
                "shortcut": "F5",
            },
            {
                "name": "repl",
                "display_name": _("REPL"),
                "description": _("Use the REPL to live-code on the board."),
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

    def run(self):
        """
        Takes the currently active tab, compiles the Python script therein into
        a hex file and flashes it all onto the connected device.
        """
        """
        if self.repl:
            message = _("Flashing cannot be performed at the same time as the "
                        "REPL is active.")
            information = _("File transfers use the same "
                            "USB serial connection as the REPL. Toggle the "
                            "REPL off and try again.")
            self.view.show_message(message, information)
            return
        """
        logger.info("Running script.")
        # Grab the Python script.
        tab = self.view.current_tab
        if tab is None:
            # There is no active text editor.
            message = _("Cannot run anything without any active editor tabs.")
            information = _(
                "Running transfers the content of the current tab"
                " onto the device. It seems like you don't have "
                " any tabs open."
            )
            self.view.show_message(message, information)
            return
        python_script = tab.text().split("\n")
        if not self.repl:
            self.toggle_repl(None)
        if self.repl:
            self.view.repl_pane.send_commands(python_script)
