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

from locale import gettext as _
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, GLib

from .photo_list_box import PhotoListBox


@Gtk.Template(resource_path='/com/gitlab/Latesil/enfuse-gui/window.ui')
class EnfuseGuiWindow(Gtk.ApplicationWindow):

    __gtype_name__ = 'EnfuseGuiWindow'

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

    exposure_weight_spinbutton = Gtk.Template.Child()
    saturation_weight_spin_button = Gtk.Template.Child()
    contrast_weight_spinbutton = Gtk.Template.Child()
    entropy_weight_spinbutton = Gtk.Template.Child()
    exposure_optimum_spinbutton = Gtk.Template.Child()
    exposure_width_spinbutton = Gtk.Template.Child()
    hard_mask_radio_button = Gtk.Template.Child()
    soft_mask_radio_button = Gtk.Template.Child()

    blend_colorspace_combobox = Gtk.Template.Child()
    depth_combobox = Gtk.Template.Child()
    wrap_combobox = Gtk.Template.Child()
    associated_alpha_hack_checkbutton = Gtk.Template.Child()
    position_entry = Gtk.Template.Child()
    size_entry = Gtk.Template.Child()

    photos_list_box_row = Gtk.Template.Child()
    photos_viewport = Gtk.Template.Child()
    basic_label = Gtk.Template.Child()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.final_command = ['enfuse']
        self.touched = set()
        self.tiffs = ['tiff', 'tif', 'TIFF', 'TIF']
        self.jpegs = ['jpeg', 'jpg', 'JPEG', 'JPG']

        self.settings = Gio.Settings.new('com.gitlab.Latesil.enfuse-gui')

        self.create_basic_label()
        self.photos_list_box_row_exists = False
        self.jpeg_compression_jpeg_arith_menubutton.set_sensitive(False)

        self.reset_all()

        self.settings.connect("changed::advanced", self.on_show_advanced_check_button_changed, self.show_advanced_check_button)
        self.settings.connect("changed::associated-alpha-hack", self.on_boolean_change, self.associated_alpha_hack_checkbutton)
        self.settings.connect("changed::levels", self.on_scale_changed, self.levels_spin_button)
        self.settings.connect("changed::auto-levels", self.on_boolean_change, self.levels_spin_button)
        self.settings.connect("changed::jpeg-compression", self.on_scale_changed, self.jpeg_compression_jpeg)
        self.settings.connect("changed::jpeg-compression-arith", self.on_scale_changed, self.jpeg_compression_jpeg_arith_spinbutton)
        self.settings.connect("changed::jpeg-compression-boolean", self.on_radiobutton_changed, self.jpeg_compression_radio_button)
        self.settings.connect("changed::jpeg-compression-arith-boolean", self.on_radiobutton_changed, self.jpeg_arith_compression_radiobutton)
        self.settings.connect("changed::exposure-weight", self.on_double_scale_changed, self.exposure_weight_spinbutton)
        self.settings.connect("changed::saturation-weight", self.on_double_scale_changed, self.saturation_weight_spin_button)
        self.settings.connect("changed::contrast-weight", self.on_double_scale_changed, self.contrast_weight_spinbutton)
        self.settings.connect("changed::entropy-weight", self.on_double_scale_changed, self.entropy_weight_spinbutton)
        self.settings.connect("changed::exposure-optimum", self.on_double_scale_changed, self.exposure_optimum_spinbutton)
        self.settings.connect("changed::exposure-width", self.on_double_scale_changed, self.exposure_width_spinbutton)
        self.settings.connect("changed::hard-mask", self.on_radiobutton_changed, self.hard_mask_radio_button)
        self.settings.connect("changed::soft-mask", self.on_radiobutton_changed, self.soft_mask_radio_button)
        self.settings.connect("changed::position", self.on_scale_changed, self.position_entry)
        self.settings.connect("changed::size", self.on_scale_changed, self.size_entry)
        self.settings.connect("changed::photos-quantity", self.on_photos_quantity_changed, None)

    @Gtk.Template.Callback()
    def on_start_button_clicked(self, button):
        #_____________________________________________________________________________________

        self.final_command = ['enfuse']
        if self.settings.get_string('output') == "":
            self.settings.reset('output')

        try:
            extension = self.settings.get_string('output').rsplit('.', 1)[1]
        except IndexError:
            self.show_error_dialog(_("Please choose correct output filename"))
            return

        if len(self.photos_list_box_row.get_children()) <= 1:
            self.show_error_dialog(_("Need more than one file to blend"))
            return

        if extension not in self.tiffs and extension not in self.jpegs:
            self.show_error_dialog(_("Output file extension must be tiff or jpeg"))
            return
        #______________________________________________________________________________________

        if self.settings.get_boolean('auto-levels') == True and 'levels' in self.touched:
            self.touched.remove('levels')

        if self.settings.get_boolean('hard-mask') != True and 'hard-mask' in self.touched:
            self.touched.remove('hard-mask')
        if self.settings.get_boolean('soft-mask') != True and 'soft-mask' in self.touched:
            self.touched.remove('soft-mask')

        if self.settings.get_boolean('associated-alpha-hack') != True and 'associated-alpha-hack' in self.touched:
            self.touched.remove('associated-alpha-hack')

        if self.settings.get_string('wrap') == 'none' and 'wrap' in self.touched:
            self.touched.remove('wrap')

        self.final_command.append('-o')
        self.final_command.append(GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_PICTURES) + '/'  + self.settings.get_string('output'))

        if 'levels' in self.touched:
            self.final_command.append('-l')
            self.final_command.append(str(self.settings.get_int('levels')))

        if 'associated-alpha-hack' in self.touched:
            self.final_command.append('-g')

        if extension in self.tiffs:
            if self.settings.get_string('tiff-compression') != 'none':
                self.final_command.append('--compression=%s' % self.settings.get_string('tiff-compression'))

        if extension in self.jpegs:
            if self.settings.get_boolean('jpeg-compression-boolean'):
                if self.settings.get_int('jpeg-compression') != 0:
                    self.final_command.append('--compression=jpeg:%s' % self.settings.get_int('jpeg-compression'))

            if self.settings.get_boolean('jpeg-compression-arith-boolean'):
                if self.settings.get_int('jpeg-compression-arith') != 0:
                    self.final_command.append('--compression=jpeg-arith:%s' % self.settings.get_int('jpeg-compression-arith'))

        if 'blend-colorspace' in self.touched:
            self.final_command.append('--blend-colorspace=%s' % self.settings.get_string('blend-colorspace'))

        if 'depth' in self.touched:
            self.final_command.append('--depth=%s' % self.settings.get_string('depth'))

        if 'size' in self.touched and 'position' in self.touched:
            self.final_command.append('-f $sx%s' % self.settings.get_int('size'), self.settings.get_int('position'))

        if 'wrap' in self.touched:
            self.final_command.append('--wrap=%s' % self.settings.get_string('wrap'))

        if 'exposure-weight' in self.touched:
            self.final_command.append('--exposure-weight=%s' % round(self.settings.get_double('exposure-weight'), 2))

        if 'saturation-weight' in self.touched:
            self.final_command.append('--saturation-weight=%s' % round(self.settings.get_double('saturation-weight'), 2))

        if 'contrast-weight' in self.touched:
            self.final_command.append('--contrast-weight=%s' % round(self.settings.get_double('contrast-weight'), 2))

        if 'entropy-weight' in self.touched:
            self.final_command.append('--entropy-weight=%s' % round(self.settings.get_double('entropy-weight'), 2))

        if 'exposure-optimum' in self.touched:
            self.final_command.append('--exposure-optimum=%s' % round(self.settings.get_double('exposure-optimum'), 2))

        if 'exposure-width' in self.touched:
            self.final_command.append('--exposure-width=%s' % round(self.settings.get_double('exposure-width'), 2))

        if 'hard-mask' in self.touched:
            self.final_command.append('-hard-mask')

        if 'soft-mask' in self.touched:
            self.final_command.append('-soft-mask')

        for child in self.photos_list_box_row.get_children():
            self.final_command.append(child.get_child().label)

        subprocess.call(self.final_command)

    @Gtk.Template.Callback()
    def on_levels_spin_button_value_changed(self, scale):
        self.settings.set_int('levels', scale.get_value())
        self.touched.add('levels')

    @Gtk.Template.Callback()
    def on_levels_checkbutton_toggled(self, button):
        if button.get_active():
            self.levels_spin_button.set_sensitive(False)
            self.settings.set_boolean('auto-levels', True)
        else:
            self.levels_spin_button.set_sensitive(True)
            self.settings.set_boolean('auto-levels', False)

    @Gtk.Template.Callback()
    def on_output_entry_changed(self, entry):
        self.settings.set_string('output', entry.get_text())

    @Gtk.Template.Callback()
    def on_blend_colorspace_combobox_changed(self, combobox):
        self.settings.set_string('blend-colorspace', self.get_item_from_combobox(combobox))
        self.touched.add('blend-colorspace')


    @Gtk.Template.Callback()
    def on_depth_combobox_changed(self, combobox):
        self.settings.set_string('depth', self.get_item_from_combobox(combobox))
        self.touched.add('depth')

    @Gtk.Template.Callback()
    def on_associated_alpha_hack_checkbutton_toggled(self, button):
        self.settings.set_boolean('associated-alpha-hack', button.get_active())
        self.touched.add('associated-alpha-hack')

    @Gtk.Template.Callback()
    def on_wrap_combobox_changed(self, combobox):
        self.settings.set_string('wrap', self.get_item_from_combobox(combobox))
        self.touched.add('wrap')

    @Gtk.Template.Callback()
    def on_exposure_weight_spinbutton_value_changed(self, scale):
        self.settings.set_double('exposure-weight', scale.get_value())
        self.touched.add('exposure-weight')

    @Gtk.Template.Callback()
    def on_saturation_weight_spin_button_value_changed(self, scale):
        self.settings.set_double('saturation-weight', scale.get_value())
        self.touched.add('saturation-weight')

    @Gtk.Template.Callback()
    def on_contrast_weight_spinbutton_value_changed(self, scale):
        self.settings.set_double('contrast-weight', scale.get_value())
        self.touched.add('contrast-weight')

    @Gtk.Template.Callback()
    def on_entropy_weight_spinbutton_value_changed(self, scale):
        self.settings.set_double('entropy-weight', scale.get_value())
        self.touched.add('entropy-weight')

    @Gtk.Template.Callback()
    def on_exposure_optimum_spinbutton_value_changed(self, scale):
        self.settings.set_double('exposure-optimum', scale.get_value())
        self.touched.add('exposure-optimum')

    @Gtk.Template.Callback()
    def on_exposure_width_spinbutton_value_changed(self, scale):
        self.settings.set_double('exposure-width', scale.get_value())
        self.touched.add('exposure-width')

    @Gtk.Template.Callback()
    def on_show_advanced_check_button_toggled(self, button):
        self.advanced_options_frame_.set_visible(button.get_active())
        self.settings.set_boolean('advanced', button.get_active())

    @Gtk.Template.Callback()
    def on_position_entry_value_changed(self, scale):
        self.settings.set_int('position', scale.get_value())
        self.touched.add('position')

    @Gtk.Template.Callback()
    def on_size_entry_value_changed(self, scale):
        self.settings.set_int('size', scale.get_value())
        self.touched.add('size')

    @Gtk.Template.Callback()
    def on_soft_mask_radio_button_toggled(self, button):
        self.settings.set_boolean('soft-mask', button.get_active())
        self.touched.add('soft-mask')

    @Gtk.Template.Callback()
    def on_hard_mask_radio_button_toggled(self, button):
        self.settings.set_boolean('hard-mask', button.get_active())
        self.touched.add('hard-mask')

    @Gtk.Template.Callback()
    def on_tiff_compression_combobox_changed(self, combobox):
        self.settings.set_string('tiff-compression', self.get_item_from_combobox(combobox))
        self.touched.add('tiff-compression')

    @Gtk.Template.Callback()
    def on_jpeg_compression_jpeg_value_changed(self, scale):
        self.settings.set_int('jpeg-compression', scale.get_value())
        self.touched.add('jpeg-compression')

    @Gtk.Template.Callback()
    def on_jpeg_compression_jpeg_arith_spinbutton_value_changed(self, scale):
        self.settings.set_int('jpeg-compression-arith', scale.get_value())
        self.touched.add('jpeg-compression-arith')

    @Gtk.Template.Callback()
    def on_add_button_clicked(self, button):
        chooser = Gtk.FileChooserDialog(title=_("Open Photos"),
                                        transient_for=self,
                                        action=Gtk.FileChooserAction.OPEN,
                                        buttons=(_("Cancel"), Gtk.ResponseType.CANCEL,
                                                 _("OK"), Gtk.ResponseType.OK))
        self.add_filters(chooser)
        chooser.set_select_multiple(True)
        response = chooser.run()
        if response == Gtk.ResponseType.OK:
            files = chooser.get_filenames()
            for f in files:
                new_box = PhotoListBox(f)
                new_row = Gtk.ListBoxRow()
                new_row.set_selectable(False)
                new_row.add(new_box)
                new_row.set_visible(True)
                self.photos_list_box_row.add(new_row)
            chooser.destroy()
        else:
            chooser.destroy()

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
    def on_about_button_clicked(self, button):
        about = Gtk.AboutDialog()
        about.set_program_name("Enfuse GUI")
        about.set_version("0.4.0")
        about.set_authors(["Latesil"])
        about.set_logo_icon_name('com.gitlab.Latesil.enfuse-gui')
        about.set_copyright("GPLv3+")
        about.set_comments(_("A simple GUI for enfuse script"))
        about.set_website("https://gitlab.com/Latesil/enfuse-gui")
        about.set_website_label(_("Website"))
        about.set_wrap_license(True)
        about.set_license_type(Gtk.License.GPL_3_0)
        about.run()
        about.destroy()

    #_____________________________________________________________________

    def on_show_advanced_check_button_changed(self, settings, key, button):
        self.advanced_options_frame_.set_visible(settings.get_boolean(key))
        button.set_active(settings.get_boolean(key))

    def on_scale_changed(self, settings, key, button):
        button.set_value(settings.get_int(key))

    def on_radiobutton_changed(self, settings, key, button):
        button.set_active(settings.get_boolean(key))

    def on_double_scale_changed(self, settings, key, button):
        button.set_value(settings.get_double(key))

    def on_boolean_change(self, settings, key, button):
        button.set_active(settings.get_boolean(key))

    def on_photos_quantity_changed(self, settings, key, button):
        if settings.get_int(key) == 0:
            self.start_button.set_visible(False)
            self.photos_viewport.remove(self.photos_list_box_row)
            self.photos_viewport.add(self.basic_label)
            self.photos_list_box_row_exists = False
        else:
            if not self.photos_list_box_row_exists:
                self.start_button.set_visible(True)
                self.photos_viewport.remove(self.basic_label)
                self.photos_viewport.add(self.photos_list_box_row)
                self.photos_list_box_row_exists = True

    #______________________________________________________________________

    def get_item_from_combobox(self, box):
        tree_iter = box.get_active_iter()
        model = box.get_model()
        item = model[tree_iter][0]
        return item

    def create_basic_label(self):
        self.photos_viewport.remove(self.photos_list_box_row)
        self.photos_viewport.add(self.basic_label)

    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Pictures")
        filter_text.add_mime_type("image/jpeg")
        filter_text.add_mime_type("image/png")
        filter_text.add_mime_type("image/tiff")
        dialog.add_filter(filter_text)

    def reset_all(self):
        for s in self.settings.list_keys():
            self.settings.reset(s)

    def show_error_dialog(self, text):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.OK, text)
        dialog.run()
        dialog.destroy()


