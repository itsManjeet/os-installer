# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gtk

from .global_state import global_state
from .page import Page


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/done.ui')
class DonePage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image = 'success-symbolic'

    page_title = Gtk.Template.Child()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

    ### callbacks ###

    @Gtk.Template.Callback('restart_button_clicked')
    def _restart_button_clicked(self, button):
        global_state.advance(self, allow_return=False)

    ### public methods ###

    def load_once(self):
        global_state.send_notification(self.page_title.get_label(), '')
