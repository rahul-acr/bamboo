from bamboo.errors.device_error import DeviceNotReadyError, DeviceError
from bamboo.sync.configuration import light_load_sync_profiles
from bamboo.sync.configuration import load_sync_profile
from bamboo.sync.sync import SyncEntry
from bamboo.transfer.transfer_worker import TransferWorker
from bamboo.utils.printing import print_success, print_warning
from bamboo.utils.size_utils import pretty_format_bytes

_show_prompt = True


def _transfer_entry(sync_entry: SyncEntry):
    print(f'Syncing:{sync_entry.name}')

    print_warning('Gathering info ...')
    worker = TransferWorker(sync_entry)
    worker.collect_source_info()

    if worker.load_count() == 0:
        print('No file found for backup. Skipping.')
        return
    if _show_prompt:
        _ = input(f'{worker.load_count()} files found '
                  f'{pretty_format_bytes(worker.load_size_in_bytes())} are to be transferred. continue ? (y) : ')
        if _ not in ['Y', 'y', '']:
            return

    print(f'{sync_entry.sync_profile.source_device.name}:{sync_entry.source_path} ->'
          f' {sync_entry.sync_profile.target_device.name}:{sync_entry.target_path} ')

    worker.backup(progress_callback=lambda current, total, transferred_bytes: print(
        "\rProgress : {0:d}/{1:d} \t Transferred {2:<16}".format(current, total,
                                                                 pretty_format_bytes(transferred_bytes)),
        end='', flush=True))

    print_success('\ncomplete!')


def _execute(profile_name):
    sync_profile = load_sync_profile(profile_name)

    if not sync_profile.source_device.is_device_online():
        raise DeviceNotReadyError(f'Please connect {sync_profile.source_device.name}')

    if not sync_profile.target_device.is_device_online():
        raise DeviceNotReadyError(f'Please connect {sync_profile.target_device.name}')

    for entry in sync_profile.sync_entries:
        _transfer_entry(entry)

    print_success(f'Sync for profile:{sync_profile.name} completed')


def _transfer_profiles(profiles):
    for profile in profiles:
        try:
            _execute(profile)
        except DeviceError as de:
            import sys
            sys.stderr.write(de.error_message)
            exit(1)


def run(**kwargs):
    profiles = kwargs['profiles']

    global _show_prompt
    _show_prompt = not kwargs.get('Y', False)

    if len(profiles) == 0 and kwargs.get('auto', False):
        all_profiles = light_load_sync_profiles()
        profiles = [p.name for p in all_profiles
                    if p.source_device.is_device_online() and p.target_device.is_device_online()]

    _transfer_profiles(profiles)
