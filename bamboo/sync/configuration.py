from os.path import join, exists
import json
from bamboo.sync.sync import SyncProfile
from bamboo.sync.device import Device
from pathlib import Path
from os import listdir
import sys


_CONFIGURATION_HOME = join(str(Path.home()), '.config/bamboo/')
_DEVICES_ROOT = join(_CONFIGURATION_HOME, 'devices')
_SYNC_CONFIG_ROOT = join(_CONFIGURATION_HOME, 'profiles')


def _assert_configuration_exist():
    if not exists(_CONFIGURATION_HOME):
        sys.stderr.write(f'Bamboo configuration not found. Please create one in {_CONFIGURATION_HOME} ')
        exit(1)


def _load_device_from_filename(filename: str):
    device_config_path = join(_DEVICES_ROOT, filename)
    with open(device_config_path) as fp:
        json_data = json.load(fp)
        return Device(filename[:-5], json_data['mount_point'])


def _load_device(device_name: str):
    return _load_device_from_filename(device_name + '.json')


def load_all_devices():
    _assert_configuration_exist()
    devices = []
    for file in listdir(_DEVICES_ROOT):
        devices.append(_load_device_from_filename(file))
    return devices


def light_load_sync_profiles():
    _assert_configuration_exist()
    profiles = []
    for profile_filename in listdir(_SYNC_CONFIG_ROOT):
        with open(join(_SYNC_CONFIG_ROOT, profile_filename)) as fp:
            sync_config_json = json.load(fp)
        source_device = _load_device(sync_config_json['source_device'])
        target_device = _load_device(sync_config_json['target_device'])
        profile = SyncProfile(profile_filename[:-5], source_device, target_device)
        profiles.append(profile)
    return profiles


def load_sync_profile(sync_config_name: str) -> SyncProfile:
    _assert_configuration_exist()
    with open(join(_SYNC_CONFIG_ROOT, sync_config_name + '.json')) as fp:
        sync_config_json = json.load(fp)

    source_device = _load_device(sync_config_json['source_device'])
    target_device = _load_device(sync_config_json['target_device'])

    sync = SyncProfile(sync_config_name, source_device, target_device)
    for sce in sync_config_json['sync_entries']:
        sync.create_sync_entry(**sce)

    return sync
