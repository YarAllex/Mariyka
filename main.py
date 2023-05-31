import getpass
import subprocess
import time
from subprocess import Popen, PIPE


class Controller:
    filePath = ''

    WAITING_PERIOD = 15
    WAITING_TIMEOUT = 30

    CMD_CREATE_CAM = ['sudo', '-S', 'modprobe', 'v4l2loopback', 'exclusive_caps=1', 'card_label="Virtual Cam"']
    CMD_RELEASE_CAM = ['sudo', '-S', 'modprobe', 'v4l2loopback', '-r']
    CMD_START_FFMPEG_STREAM = ['ffmpeg', '-stream_loop', '-1', '-re', '-i', filePath, '-f', 'v4l2', '/dev/video2']

    ENTER_THE_SUDO_PASSWORD = 'Enter the sudo password: '
    RUN_STREAM = 'Run stream'
    CREATE_CAMERA = 'Create camera'
    PRESS_ENTER_TO_STOP = "Press enter to stop..."
    RELEASE_CAMERA = 'Release camera'
    LOOPBACK_IS_IN_USE = 'Module v4l2loopback is in use'
    PLEASE_WAIT = 'please wait...'
    ERROR_TIME_IS_OVER = 'Error: Time is over'

    stream = None

    def create_cam(self):
        pipe = subprocess.Popen(self.CMD_CREATE_CAM, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
        pipe.communicate(input=getpass.getpass(self.ENTER_THE_SUDO_PASSWORD))
        pipe.wait()
        del pipe
        print(self.CREATE_CAMERA)

    def release_cam(self):
        error = self.run_cmd(self.CMD_RELEASE_CAM)

        if error.__contains__(self.LOOPBACK_IS_IN_USE):
            success = self.waiting_camera(self.CMD_RELEASE_CAM, error)
        else:
            success = True

        if success:
            print(self.RELEASE_CAMERA)
        else:
            print(self.ERROR_TIME_IS_OVER)

    def waiting_camera(self, cmd, error):
        print(self.LOOPBACK_IS_IN_USE, self.PLEASE_WAIT)

        i = self.WAITING_PERIOD
        while error.__contains__(self.LOOPBACK_IS_IN_USE) and i > 0:
            print('...')
            time.sleep(self.WAITING_TIMEOUT / i)
            error = self.run_cmd(cmd)
            i -= 1
        print('')

        return i > 0

    def run_cmd(self, cmd):
        pipe = subprocess.Popen(cmd, stderr=PIPE, text=True)
        pipe.wait()
        error = pipe.stderr.readline()
        pipe.kill()
        del pipe
        return error

    def run_stream(self):
        self.stream = Popen(self.CMD_START_FFMPEG_STREAM, stderr=PIPE, stdout=PIPE, stdin=PIPE, universal_newlines=True)
        print(self.RUN_STREAM)

    def stop_stream(self):
        if self.stream is not None:
            self.stream.kill()

    def setFilePath(self, path):
        self.filePath = path
        # self.CMD_START_FFMPEG_STREAM.pop(5)
        self.CMD_START_FFMPEG_STREAM[5] = self.filePath
        # self.CMD_START_FFMPEG_STREAM.


def main():
    controller = Controller()
    controller.setFilePath('/home/yar/Videos/test/countdown.mp4')
    controller.create_cam()
    controller.run_stream()
    print("Path=", controller.CMD_START_FFMPEG_STREAM)
    print(input(controller.PRESS_ENTER_TO_STOP), end='')
    controller.stop_stream()
    controller.release_cam()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
