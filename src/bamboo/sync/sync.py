from os.path import join
import re
import time
from .device import Device


class SyncProfile:
    def __init__(self, name: str, source_device: Device, target_device: Device):
        self.name = name
        assert source_device != target_device
        self.source_device = source_device
        self.target_device = target_device
        self.sync_entries = []

    def create_sync_entry(self, **kwargs):
        sync_entry = SyncEntry(self, **kwargs)
        self.sync_entries.append(sync_entry)

    def entry_count(self) -> int:
        return len(self.sync_entries)

    def __str__(self) -> str:
        return f'Sync Profile [{self.name}] from {self.source_device.name} to {self.target_device.name}' \
               f' containing {self.entry_count()} entries'


class SyncEntry:
    def __init__(self, sync_profile: SyncProfile, **kwargs):
        self.name = kwargs['name']
        self.sync_profile = sync_profile
        self.source_path = join(sync_profile.source_device.mount_point, kwargs['source'])
        self.target_path = join(sync_profile.target_device.mount_point, kwargs['target'])

        self.filter_patterns = []
        if 'filter_regex' in kwargs:
            for regex in kwargs['filter_regex']:
                self.filter_patterns.append(re.compile(regex, re.IGNORECASE))

        self.retention_period = 0
        if 'retention_period' in kwargs:
            self.retention_period = kwargs['retention_period']

        self.threshold_ts = time.time() - self.retention_period * 24 * 3600

    def __str__(self) -> str:
        return f'Sync Entry {self.name} from [{self.source_path}] to [{self.target_path}] ' \
               f' under {self.sync_profile.name}' \
               f' retention period = {self.retention_period} days filters = {len(self.filter_patterns)} '
