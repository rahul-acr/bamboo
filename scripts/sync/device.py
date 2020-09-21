from os.path import exists
import shutil


# Add free space feature
class Device:
    def __init__(self, name: str, mount_point: str):
        self.name = name
        self.mount_point = mount_point

    def is_device_online(self) -> bool:
        return exists(self.mount_point)

    def __str__(self) -> str:
        return f'{self.name} mounted on {self.mount_point}'

    def usage(self):
        return shutil.disk_usage(self.mount_point)