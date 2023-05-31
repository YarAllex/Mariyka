import sys

import gi

from main import Controller

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gio


class MyApplication(Gtk.Application):

    controller = Controller()

    builder = Gtk.Builder()

    def __init__(self):
        super().__init__(application_id="net.yarAllex.Mariyka")
        GLib.set_application_name('Mariyka')

    def do_activate(self):
        self.builder.add_from_file('main_window.ui')

        bStart = self.builder.get_object('bStart')
        bStart.connect('clicked', self.onStartClicked)

        bStop = self.builder.get_object('bStop')
        bStop.connect('clicked', self.onStopClicked)

        bChoose = self.builder.get_object('bChoose')
        bChoose.connect('clicked', self.onChooseClicked)

        main_window = self.builder.get_object('main_window')
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
        dialog = Gtk.FileDialog()
        dialog.open(callback=self.onFinishFileDialog)
        dialog.get_initial_name()


    def onFinishFileDialog(self, dialog, result):
        file = dialog.open_finish(result)
        if file is not None:
            print(f"File path is {file.get_path()}")
            self.controller.setFilePath(file.get_path())
            eFilePath = self.builder.get_object('eFilePath')
            eFilePath.set_text(file.get_path())


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
