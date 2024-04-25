# appteka - helpers collection

# Copyright (C) 2018-2024 Aleksandr Popov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Lesser GNU General Public License for more details.

# You should have received a copy of the Lesser GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Helpers for CLI."""

import time
import sys


class ProgressMessages:
    """This class provides the console progress messages in format:

    Some operation ... ready [n sec].
    """

    def __init__(self, digits=1, output=sys.stdout):
        self.start_time = None
        self.digits = digits
        self.__output = output

    def begin(self, message):
        """Show start part of message and three points."""
        self.start_time = time.time()
        self.__output.write(f'{message} ... ')
        self.__output.flush()

    def end(self):
        """Show end part of message."""
        end_time = round(time.time() - self.start_time, self.digits)

        self.__output.write(f'ready [{end_time} sec]\n')
