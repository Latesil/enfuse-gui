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

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio


@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/window.ui')
class EnfuseGuiWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'EnfuseGuiWindow'

    about_button = Gtk.Template.Child()
    header_bar_menubutton = Gtk.Template.Child()
    start_button = Gtk.Template.Child()
    levels_spin_button = Gtk.Template.Child()
    levels_checkbutton = Gtk.Template.Child()
    advanced_options_frame_ = Gtk.Template.Child()

    jpeg_compression_jpeg = Gtk.Template.Child()
    jpeg_compression_jpeg_menubutton = Gtk.Template.Child()
    jpeg_compression_menubutton = Gtk.Template.Child()
    jpeg_compression_radio_button = Gtk.Template.Child()
    jpeg_arith_compression_radiobutton = Gtk.Template.Child()
    jpeg_compression_jpeg_arith_menubutton = Gtk.Template.Child()
    jpeg_compression_jpeg_arith_spinbutton = Gtk.Template.Child()

    tiff_compression_menubutton = Gtk.Template.Child()

    output_entry = Gtk.Template.Child()
    show_advanced_check_button = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.settings = Gio.Settings.new('com.gitlab.Latesil.enfuse-gui')

        self.start_button.set_visible(True)
        self.jpeg_compression_jpeg_arith_menubutton.set_sensitive(False)

        for s in self.settings.list_keys():
            self.settings.reset(s)

        self.settings.connect("changed::advanced", self.on_show_advanced_check_button_changed, self.show_advanced_check_button)
        self.settings.connect("changed::levels", self.on_scale_changed, self.levels_spin_button)
        self.settings.connect("changed::jpeg-compression", self.on_scale_changed, self.jpeg_compression_jpeg)
        self.settings.connect("changed::jpeg-compression-arith", self.on_scale_changed, self.jpeg_compression_jpeg_arith_spinbutton)
        self.settings.connect("changed::jpeg-compression-boolean", self.on_radiobutton_changed, self.jpeg_compression_radio_button)
        self.settings.connect("changed::jpeg-compression-arith-boolean", self.on_radiobutton_changed, self.jpeg_arith_compression_radiobutton)

    @Gtk.Template.Callback()
    def on_start_button_clicked(self, button):
        print('start_button')

    @Gtk.Template.Callback()
    def on_levels_spin_button_value_changed(self, scale):
        self.settings.set_int('levels', scale.get_value())

    @Gtk.Template.Callback()
    def on_levels_checkbutton_toggled(self, button):
        if button.get_active():
            self.levels_spin_button.set_sensitive(False)
        else:
            self.levels_spin_button.set_sensitive(True)

    @Gtk.Template.Callback()
    def on_output_entry_changed(self, entry):
        self.settings.set_string('output', entry.get_text())

    @Gtk.Template.Callback()
    def on_blend_colorspace_combobox_changed(self, widget):
        print('on_blend_colorspace_combobox_changed')

    @Gtk.Template.Callback()
    def on_depth_combobox_changed(self, widget):
        print('on_depth_combobox_changed')

    @Gtk.Template.Callback()
    def on_associated_alpha_hack_checkbutton_toggled(self, widget):
        print('on_associated_alpha_hack_checkbutton_toggled')

    @Gtk.Template.Callback()
    def on_wrap_combobox_changed(self, widget):
        print('on_wrap_combobox_changed')

    @Gtk.Template.Callback()
    def on_exposure_weight_spinbutton_value_changed(self, scale):
        print('on_exposure_weight_spinbutton_value_changed')

    @Gtk.Template.Callback()
    def on_saturation_weight_spin_button_value_changed(self, scale):
        print('on_saturation_weight_spin_button_value_changed')

    @Gtk.Template.Callback()
    def on_contrast_weight_spinbutton_value_changed(self, scale):
        print('on_contrast_weight_spinbutton_value_changed')

    @Gtk.Template.Callback()
    def on_entropy_weight_spinbutton_value_changed(self, scale):
        print('on_entropy_weight_spinbutton_value_changed')

    @Gtk.Template.Callback()
    def on_exposure_optimum_spinbutton_value_changed(self, scale):
        print('on_exposure_optimum_spinbutton_value_changed')

    @Gtk.Template.Callback()
    def on_exposure_width_spinbutton_value_changed(self, scale):
        print('on_exposure_width_spinbutton_value_changed')

    @Gtk.Template.Callback()
    def on_soft_mask_radio_button_group_changed(self, widget):
        print('on_soft_mask_radio_button_group_changed')

    @Gtk.Template.Callback()
    def on_show_advanced_check_button_toggled(self, button):
        self.advanced_options_frame_.set_visible(button.get_active())
        self.settings.set_boolean('advanced', button.get_active())

    def on_show_advanced_check_button_changed(self, settings, key, button):
        self.advanced_options_frame_.set_visible(settings.get_boolean(key))
        button.set_active(settings.get_boolean(key))

    @Gtk.Template.Callback()
    def on_position_entry_changed(self, widget):
        print('on_position_entry_changed')

    @Gtk.Template.Callback()
    def on_size_entry_changed(self, widget):
        print('on_size_entry_changed')

    @Gtk.Template.Callback()
    def on_soft_mask_radio_button_toggled(self, widget):
        print('on_soft_mask_radio_button_toggled')

    @Gtk.Template.Callback()
    def on_tiff_compression_combobox_changed(self, combobox):
        tree_iter = combobox.get_active_iter()
        model = combobox.get_model()
        tiff_compression_method = model[tree_iter][0]
        self.settings.set_string('tiff-compression', tiff_compression_method)

    @Gtk.Template.Callback()
    def on_exposure_weight_spinbutton_value_changed(self, widget):
        print('on_exposure_weight_spinbutton_value_changed')

    @Gtk.Template.Callback()
    def on_jpeg_compression_jpeg_value_changed(self, scale):
        self.settings.set_int('jpeg-compression', scale.get_value())

    @Gtk.Template.Callback()
    def on_jpeg_compression_jpeg_arith_spinbutton_value_changed(self, scale):
        self.settings.set_int('jpeg-compression-arith', scale.get_value())

    @Gtk.Template.Callback()
    def on_jpeg_compression_radio_button_toggled(self, button):
        if button.get_active():
            self.jpeg_compression_jpeg_menubutton.set_sensitive(True)
            self.jpeg_compression_jpeg_arith_menubutton.set_sensitive(False)
            self.settings.set_boolean('jpeg-compression-boolean', True)
            self.settings.set_boolean('jpeg-compression-arith-boolean', False)
        else:
            self.jpeg_compression_jpeg_menubutton.set_sensitive(False)
            self.jpeg_compression_jpeg_arith_menubutton.set_sensitive(True)
            self.settings.set_boolean('jpeg-compression-boolean', False)
            self.settings.set_boolean('jpeg-compression-arith-boolean', True)

    @Gtk.Template.Callback()
    def on_hard_mask_radio_button_toggled(self, widget):
        print('on_hard_mask_radio_button_toggled')

    @Gtk.Template.Callback()
    def on_about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name("Enfuse GUI")
        about.set_version("0.0.1")
        about.set_authors(["Latesil"])
        #about.set_logo_icon_name('com.gitlab.Latesil.enfuse-gui')
        about.set_copyright("GPLv3+")
        about.set_comments("A simple GUI for enfuse script")
        about.set_website("https://gitlab.com/Latesil/enfuse-gui")
        about.set_website_label("Website")
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()

    def on_scale_changed(self, settings, key, button):
        button.set_value(settings.get_int(key))

    def on_radiobutton_changed(self, settings, key, button):
        button.set_active(settings.get_boolean(key))
