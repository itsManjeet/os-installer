# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/encrypt.ui')
class EncryptPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'dialog-password-symbolic'

    switch = Gtk.Template.Child()

    pin_row = Gtk.Template.Child()
    info_revealer = Gtk.Template.Child()

    continue_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    def _set_continue_button(self, needs_pin, pin):
        can_continue = not needs_pin or len(pin) > 0
        self.continue_button.set_sensitive(can_continue)

    ### callbacks ###

    @Gtk.Template.Callback('encryption_row_clicked')
    def _encryption_row_clicked(self, row):
        self.switch.activate()

    @Gtk.Template.Callback('switch_flipped')
    def _switch_flipped(self, switch, state):
        self.pin_row.set_sensitive(state)
        self.info_revealer.set_reveal_child(state)

        if state:
            self.pin_row.grab_focus()
        self._set_continue_button(
            needs_pin=state, pin=self.pin_row.get_text())

    @Gtk.Template.Callback('pin_changed')
    def _pin_changed(self, editable):
        self._set_continue_button(
            needs_pin=self.switch.get_state(), pin=editable.get_text())

    @Gtk.Template.Callback('continue')
    def _continue(self, object):
        if self.continue_button.is_sensitive():
            global_state.advance(self)

    ### public methods ###

    def unload(self):
        use_encryption = self.switch.get_state()
        pin = self.pin_row.get_text()
        global_state.set_config('use_encryption', use_encryption)
        global_state.set_config('encryption_pin', pin)
