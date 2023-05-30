import getpass
import subprocess
import time
from subprocess import Popen, PIPE

WAITING_PERIOD = 15
WAITING_TIMEOUT = 30

CMD_CREATE_CAM = ['sudo', '-S', 'modprobe', 'v4l2loopback', 'exclusive_caps=1', 'card_label="Virtual Cam"']
CMD_RELEASE_CAM = ['sudo', '-S', 'modprobe', 'v4l2loopback', '-r']
CMD_START_FFMPEG_STREAM = ['ffmpeg', '-stream_loop', '-1', '-re', '-i', '/home/yar/Videos/test/countdown.mp4', '-f', 'v4l2', '/dev/video2']

ENTER_THE_SUDO_PASSWORD = 'Enter the sudo password: '
RUN_STREAM = 'Run stream'
CREATE_CAMERA = 'Create camera'
PRESS_ENTER_TO_STOP = "Press enter to stop..."
RELEASE_CAMERA = 'Release camera'
LOOPBACK_IS_IN_USE = 'Module v4l2loopback is in use'
PLEASE_WAIT = 'please wait...'
ERROR_TIME_IS_OVER = 'Error: Time is over'

global stream


def create_cam():
    pipe = subprocess.Popen(CMD_CREATE_CAM, stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    pipe.communicate(input=getpass.getpass(ENTER_THE_SUDO_PASSWORD))
    pipe.wait()
    del pipe
    print(CREATE_CAMERA)


def release_cam():
    error = run_cmd(CMD_RELEASE_CAM)

    if error.__contains__(LOOPBACK_IS_IN_USE):
        success = waiting_camera(CMD_RELEASE_CAM, error)
    else:
        success = True

    if success:
        print(RELEASE_CAMERA)
    else:
        print(ERROR_TIME_IS_OVER)


def waiting_camera(cmd, error):
    print(LOOPBACK_IS_IN_USE, PLEASE_WAIT)

    i = WAITING_PERIOD
    while error.__contains__(LOOPBACK_IS_IN_USE) and i > 0:
        print('...')
        time.sleep(WAITING_TIMEOUT / i)
        error = run_cmd(cmd)
        i -= 1
    print('')

    return i > 0


def run_cmd(cmd):
    pipe = subprocess.Popen(cmd, stderr=PIPE, text=True)
    pipe.wait()
    error = pipe.stderr.readline()
    pipe.kill()
    del pipe
    return error


def run_stream():
    global stream
    stream = Popen(CMD_START_FFMPEG_STREAM, stderr=PIPE, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print(RUN_STREAM)


def stop_stream():
    print(input(PRESS_ENTER_TO_STOP), end='')
    if stream is not None:
        stream.kill()


def main():
    create_cam()
    run_stream()
    stop_stream()
    release_cam()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
