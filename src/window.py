# window.py
#
# Copyright 2020 Latesil
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

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/window.ui')
class EnfuseGuiWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'EnfuseGuiWindow'

    label = Gtk.Template.Child()
    about_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name(_("Enfuse GUI"))
        about.set_version("0.0.1")
        about.set_authors(["Latesil"])
        #about.set_logo_icon_name('com.gitlab.Latesil.enfuse-gui')
        about.set_copyright("GPLv3+")
        about.set_comments(_("A simple GUI for enfuse script"))
        about.set_website("https://gitlab.com/Latesil/enfuse-gui")
        about.set_website_label(_("Website"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()
