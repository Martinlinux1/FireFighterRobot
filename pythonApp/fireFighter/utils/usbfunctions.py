import fcntl
import os
from subprocess import Popen, PIPE

USB_DEV_FS_RESET = 21780


class USBFunctions:
    @staticmethod
    def reset_usb(driver):
        try:
            lsusb_out = Popen("lsusb | grep -i %s" % driver, shell=True, bufsize=64, stdin=PIPE, stdout=PIPE,
                              close_fds=True). \
                stdout.read().strip().split()
            bus = lsusb_out[1]
            device = lsusb_out[3][:-1]

            f = open("/dev/bus/usb/%s/%s" % (bus, device), 'w', os.O_WRONLY)
            fcntl.ioctl(f, USB_DEV_FS_RESET, 0)
        except Exception as msg:
            print("failed to reset device:", msg)
