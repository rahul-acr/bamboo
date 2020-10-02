from os import stat
from os.path import isfile, join, exists

from bamboo.sync.sync import SyncEntry


class TransferLoad:
    def __init__(self, filename: str, sync_entry: SyncEntry):
        self.filename = filename
        self._sync_entry = sync_entry
        self._generate_paths()
        self._stat = stat(self.source_path)

    def _generate_paths(self):
        self.source_path = join(self._sync_entry.source_path, self.filename)
        self.target_path = join(self._sync_entry.target_path, self.filename)

    def is_eligible_for_backup(self) -> bool:
        if not isfile(self.source_path):
            return False
        if len(self._sync_entry.filter_patterns) == 0:
            return True
        for pattern in self._sync_entry.filter_patterns:
            if pattern.match(self.filename):
                return True
        return False

    def target_exists(self) -> bool:
        return exists(self.target_path)

    def modified_time(self) -> float:
        return self._stat.st_mtime

    def size_in_bytes(self) -> float:
        return self._stat.st_size
