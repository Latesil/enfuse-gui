import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/photo_list_box.ui')
class PhotoListBox(Gtk.Box):

    __gtype_name__ = "PhotoListBox"

    i = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.gitlab.Latesil.enfuse-gui')

        PhotoListBox.i += 1
        self.settings.set_int('photos-quantity', PhotoListBox.i)

    @Gtk.Template.Callback()
    def on_photo_button_clicked(self, button):
        PhotoListBox.i -= 1

        self.settings.set_int('photos-quantity', PhotoListBox.i)
        self.get_parent().destroy()
