# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk, Adw


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/confirm_quit_popup.ui')
class ConfirmQuitPopup(Adw.Window):
    __gtype_name__ = 'ConfirmQuitPopup'

    stop_button = Gtk.Template.Child()
    continue_button = Gtk.Template.Child()

    def __init__(self, confirm_callback, **kwargs):
        super().__init__(**kwargs)

        self.confirm_callback = confirm_callback

    ### callbacks ###

    @Gtk.Template.Callback('stop_button_clicked')
    def _on_clicked_stop_button(self, button):
        self.confirm_callback()

    @Gtk.Template.Callback('continue_button_clicked')
    def _on_clicked_continue_button(self, button):
        self.close()
