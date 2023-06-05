import sys

import gi

from main import Controller

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk, Gio


class MyApplication(Gtk.Application):

    controller = Controller()

    builder = Gtk.Builder()

    video = None

    main_window = None

    passwd_dialog = None

    def __init__(self):
        super().__init__(application_id="net.yarAllex.Mariyka")
        GLib.set_application_name('Mariyka')

    def do_activate(self):
        self.builder.add_from_file('main_window.ui')
        self.builder.add_from_file('password.ui')

        self.bStart = self.builder.get_object('bStart')
        self.bStart.connect('clicked', self.onStartClicked)
        self.bStart.set_sensitive(False)

        self.bStop = self.builder.get_object('bStop')
        self.bStop.connect('clicked', self.onStopClicked)
        self.bStop.set_sensitive(False)

        self.bChoose = self.builder.get_object('bChoose')
        self.bChoose.connect('clicked', self.onChooseClicked)

        self.video = self.builder.get_object('video')

        self.main_window = self.builder.get_object('main_window')
        self.main_window.set_application(self)
        self.main_window.present()

    def onStartClicked(self, button):
        print("Start btn")
        if self.controller.passwd == '':
            self.getPasswd()
        else:
            self.startCamera()


    def onStopClicked(self, button):
        print("Stop btn")
        self.controller.stop_stream()
        self.controller.release_cam()
        self.bStop.set_sensitive(False)
        self.bStart.set_sensitive(True)

    def onChooseClicked(self, button):
        print("Choose btn")
        dialog = Gtk.FileDialog()
        dialog.set_modal(True)
        dialog.open(parent=self.main_window, callback=self.onFinishFileDialog)
        dialog.get_initial_name()

    def onFinishFileDialog(self, dialog, result):
        file = dialog.open_finish(result)
        if file is not None:
            print(f"File path is {file.get_path()}")
            self.controller.setFilePath(file.get_path())
            eFilePath = self.builder.get_object('eFilePath')
            eFilePath.set_text(file.get_path())
            self.video.set_filename(file.get_path())
            self.bStart.set_sensitive(True)

    def getPasswd(self):
        if self.passwd_dialog is None:
            self.passwd_dialog = self.builder.get_object('password_dialog')
            self.passwd_dialog.set_transient_for(parent=self.main_window)

            self.bPasswdOk = self.builder.get_object('passwdOk')
            self.bPasswdOk.connect('clicked', self.onPasswdOk)

            self.bPasswdOk = self.builder.get_object('passwdCancel')
            self.bPasswdOk.connect('clicked', self.onPasswdCancel)

            passwdEntry = self.builder.get_object('passwdEntry')
            passwdEntry.connect('activate', self.onPasswdOk)

            print('Create dialog')

        self.passwd_dialog.present()

    def onPasswdOk(self, button):
        if self.controller.passwd == '':
            passwdEntry = self.builder.get_object('passwdEntry')
            password = passwdEntry.get_text()
            self.passwd_dialog.set_visible(False)
            self.controller.passwd = password

        self.startCamera()

    def startCamera(self):
        self.controller.create_cam()
        self.controller.run_stream()
        # self.video.get_media_stream().play()

        self.bStart.set_sensitive(False)
        self.bStop.set_sensitive(True)

    def onPasswdCancel(self, button):
        self.passwd_dialog.set_visible(False)


app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
