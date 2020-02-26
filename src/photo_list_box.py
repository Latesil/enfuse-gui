import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/photo_list_box.ui')
class PhotoListBox(Gtk.Box):

    __gtype_name__ = "PhotoListBox"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
