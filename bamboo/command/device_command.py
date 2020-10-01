from bamboo.sync.configuration import load_all_devices
from bamboo.utils.printing import print_success


def run(**_):
    devices = load_all_devices()
    online_devices = []
    offline_devices = []
    for device in devices:
        if device.is_device_online():
            online_devices.append(device)
        else:
            offline_devices.append(device)

    for device in online_devices:
        total, used, _ = device.usage()
        print_success(f'*{device.name} ({round(used/total, 2)})\t: {device.mount_point}')

    for device in offline_devices:
        print(f'{device.name}\t:{device.mount_point}')
