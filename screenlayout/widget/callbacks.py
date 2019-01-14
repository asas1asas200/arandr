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

def set_active(outputfactory, to_be_changed):
    """Construct a GTK set_active callback that, depending on the passed-in
    widget's active property, enables or disables the output given by factory,
    and issues a `changed` callback on another widget.

    The output is given as a factory so that the hook can outlive the creation
    of a new server state and connected outputs."""

    def set_active(widget):
        output = outputfactory()

        if widget.props.active == output.is_active():
            return

        if widget.props.active:
            output.enable()
        else:
            output.disable()

        to_be_changed.emit('changed')
    return set_active

def set_primary(outputfactory, to_be_changed):
    """Like set_active, but for primary"""
    def set_primary(widget):
        output = outputfactory()

        old_state = output.transition.primary is output
        if old_state == widget.props.active:
            return

        if widget.props.active:
            output.transition.primary = output
        else:
            output.transition.primary = output.transition.NO_PRIMARY

        to_be_changed.emit('changed')
    return set_primary
