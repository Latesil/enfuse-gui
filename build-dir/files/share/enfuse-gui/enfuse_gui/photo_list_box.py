import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/photo_list_box.ui')
class PhotoListBox(Gtk.Box):

    __gtype_name__ = "PhotoListBox"

    photo_label = Gtk.Template.Child()

    i = 0

    def __init__(self, label, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.gitlab.Latesil.enfuse-gui')

        PhotoListBox.i += 1
        self.settings.set_int('photos-quantity', PhotoListBox.i)
        self.label = label
        self.photo_label.set_text(self.label)

    @Gtk.Template.Callback()
    def on_photo_button_clicked(self, button):
        PhotoListBox.i -= 1

        self.settings.set_int('photos-quantity', PhotoListBox.i)
        self.get_parent().destroy()
