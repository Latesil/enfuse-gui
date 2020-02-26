import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/photo_box.ui')
class PhotoBox(Gtk.ListBox):
    pass
