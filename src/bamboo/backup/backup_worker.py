from os import listdir
from os import remove
from os.path import exists
from shutil import move, copyfile
from typing import List

from backup.backup_load import BackupLoad
from sync.sync import SyncEntry


class BackupWorker:
    def __init__(self, sync_entry: SyncEntry):
        self._sync_entry = sync_entry
        self._sync_profile = self._sync_entry.sync_profile
        self._backup_loads: List[BackupLoad] = []
        self._purged = 0
        self._backed = 0
        self._transfer_size_in_bytes = 0
        self._source_info_collected = False
        self._backup_complete = False

    def collect_source_info(self):
        self._reset_backup_stats()
        assert self._sync_profile.source_device.is_device_online(), 'Connect the source device'

        for filename in listdir(self._sync_entry.source_path):
            backup_load = BackupLoad(filename, self._sync_entry)
            if backup_load.is_eligible_for_backup():
                self._backup_loads.append(backup_load)
                self._transfer_size_in_bytes += backup_load.size_in_bytes()

        self._source_info_collected = True
        self._backup_complete = False

    def backup(self, progress_callback):
        self._verify_backup_preconditions()
        transferred_bytes = 0
        for bl in self._backup_loads:
            target_path_exists = bl.target_exists()
            if bl.modified_time() > self._sync_entry.threshold_ts:
                if not target_path_exists:
                    self._copy_load(bl)
            elif target_path_exists:
                self._delete_load(bl)
            else:
                self._move_load(bl)
            transferred_bytes += bl.size_in_bytes()
            progress_callback(self._backed + self._purged, self.load_count(), transferred_bytes)

        self._backup_complete = True
        return self._backed, self._purged

    def load_count(self):
        return len(self._backup_loads)

    def load_size_in_bytes(self):
        return self._transfer_size_in_bytes

    def _verify_backup_preconditions(self):
        if not self._source_info_collected:
            raise RuntimeError('Source information is not collected yet')
        if self._backup_complete:
            raise RuntimeError('BackupWorker task is already complete')
        assert self._sync_profile.source_device.is_device_online(), 'Source device is not online'
        assert self._sync_profile.target_device.is_device_online(), 'Target device is not online'

    def _reset_backup_stats(self):
        self._backup_loads.clear()
        self._transfer_size_in_bytes = 0
        self._purged = self._backed = 0
        self._source_info_collected = self._backup_complete = False

    def _copy_load(self, backup_load: BackupLoad):
        if not exists(backup_load.target_path):
            copyfile(backup_load.source_path, backup_load.target_path)
        self._backed += 1

    def _delete_load(self, backup_load: BackupLoad):
        remove(backup_load.source_path)
        self._purged += 1

    def _move_load(self, backup_load: BackupLoad):
        move(backup_load.source_path, backup_load.target_path)
        self._backed += 1
