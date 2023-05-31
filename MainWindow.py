import sys

import gi

from main import Controller

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk


class MyApplication(Gtk.Application):

    controller = Controller()
    def __init__(self):
        super().__init__(application_id="net.yarAllex.Mariyka")
        GLib.set_application_name('Mariyka')

    def do_activate(self):
        builder = Gtk.Builder()
        builder.add_from_file('main_window.ui')

        bStart = builder.get_object('bStart')
        bStart.connect('clicked', self.onStartClicked)

        bStop = builder.get_object('bStop')
        bStop.connect('clicked', self.onStopClicked)

        bChoose = builder.get_object('bChoose')
        bChoose.connect('clicked', self.onChooseClicked)

        main_window = builder.get_object('main_window')
        main_window.set_application(self)
        main_window.present()

    def onStartClicked(self, button):
        print("Start btn")
        self.controller.create_cam()
        self.controller.run_stream()

    def onStopClicked(self, button):
        print("Stop btn")
        self.controller.stop_stream()
        self.controller.release_cam()

    def onChooseClicked(self, button):
        print("Choose btn")



app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
