from bamboo.sync.configuration import load_all_devices
from bamboo.utils.printing import print_success


def run(**_):
    devices = load_all_devices()
    for device in devices:
        if device.is_device_online():
            print_success(f'{device.name:16} : {device.mount_point}')
        else:
            print(f'{device.name:16} : {device.mount_point}')
