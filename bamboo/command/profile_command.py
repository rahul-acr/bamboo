from bamboo.sync.configuration import light_load_sync_profiles
from bamboo.utils.printing import print_success


def run(**_):
    profiles = light_load_sync_profiles()
    for profile in profiles:
        output = f'{profile.name:16} : {profile.source_device.name:10} -> {profile.target_device.name:10}'
        if profile.source_device.is_device_online() and profile.target_device.is_device_online():
            print_success(output)
        else:
            print(output)
