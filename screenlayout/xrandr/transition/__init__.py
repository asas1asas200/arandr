# ARandR -- Another XRandR GUI
# Copyright (C) 2008 -- 2011 chrysn <chrysn@fsfe.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from . import primary, position, mode

from .base import FreezeLevel

class TransitionOutput(
        primary.TransitionOutputForPrimary,
        position.TransitionOutputForPosition,
        mode.TransitionOutputForMode
        ):
    # High-level functions that cause action across modules

    def enable(self):
        self.set_any_mode()
        self.set_any_position()

    def disable(self):
        self.named_mode = None
        self.rate = None
        self.precise_mode = None
        self.auto = False
        self.off = True
        self.position = None

class Transition(
        primary.TransitionForPrimary,
        position.TransitionForPosition,
        mode.TransitionForMode
        ):
    Output = TransitionOutput
