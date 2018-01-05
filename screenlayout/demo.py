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

"""Demo application, primarily used to make sure the screenlayout library can
be used independent of ARandR.

Run by calling the main() function. For interactive testing, call `main(False)`
from IPython or anything else that runs a GTK main loop. In that case, you can
fetch the current tab widgets from the `current_tabs` global variable.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from .widget import TransitionWidget, TransitionOutputWidget

current_tabs = [] # kept here just for sake of global access in IPython sessions

def update_tabs(widget, notebook):
    print("Current configuration:", widget.save_to_string())
    for ok, od in list(widget._transition.outputs.items()):
        print(ok, vars(od))
    print(dict((k,d) for (k, d) in list(vars(widget._transition).items()) if k not in ('outputs', 'predicted_server', 'server')))
    print()

    outputs = list(widget._transition.outputs.keys())

    for t in notebook.get_children():
        if t.output_name in outputs:
            outputs.remove(t.output_name)
            t.update()
        else:
            notebook.remove(t)
            current_tabs.remove(t)

    for output_name in outputs:
        tabwidget = TransitionOutputWidget(widget, output_name)
        notebook.insert_page(tabwidget, tab_label=Gtk.Label(output_name.decode('utf8', errors='replace')), position=-1)
        current_tabs.append(tabwidget)
        tabwidget.connect('changed', lambda *args: widget.emit('changed'))
        tabwidget.update()

    notebook.show_all()

def main(do_run=True):
    """Create a demo widget in a window with some peripherials, and either run
    it in GTK or return the widget"""
    w = Gtk.Window()
    w.connect('destroy',Gtk.main_quit)

    r = TransitionWidget()
    r.load_from_x()

    output_properties = Gtk.Notebook()
    r.connect('changed', update_tabs, output_properties)
    r.emit('changed')

    b1 = Gtk.Button(stock="gtk-refresh")
    b1.connect('clicked', lambda *args: r.load_from_x())

    b2 = Gtk.Button("Preview command")
    b2.props.image = Gtk.Image()
    b2.props.image.props.icon_name = "gtk-find"
    def preview(*args):
        d = Gtk.Dialog("Command preview", w, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, (Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        l = Gtk.Label(r.save_to_string())
        d.vbox.add(l)
        d.show_all()
        d.run()
        d.destroy()
    b2.connect('clicked', preview)

    b3 = Gtk.Button(stock='gtk-apply')
    b3.connect('clicked', lambda *args: r.save_to_x())

    v = Gtk.VBox()
    w.add(v)
    v.add(r)
    v.add(output_properties)
    v.pack_end(b1, expand=False, fill=False, padding=0)
    v.pack_end(b2, expand=False, fill=False, padding=0)
    v.pack_end(b3, expand=False, fill=False, padding=0)
    w.set_title('Simple ARandR Widget Demo')
    w.show_all()
    if do_run:
        Gtk.main()
    else:
        return r

if __name__ == "__main__":
    main()
