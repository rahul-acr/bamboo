from bamboo.backup.backup_worker import BackupWorker
from bamboo.errors.device_error import DeviceNotReadyError, DeviceError
from bamboo.sync.configuration import load_sync_profile
from bamboo.sync.sync import Device
from bamboo.sync.sync import SyncEntry
from bamboo.utils.printing import print_error, print_success, print_warning
from bamboo.utils.size_utils import pretty_format_bytes


def _backup_entry(sync_entry: SyncEntry, prompt):
    print(f'Syncing:{sync_entry.name}')

    print_warning('Gathering info ...')
    worker = BackupWorker(sync_entry)
    worker.collect_source_info()

    if worker.load_count() == 0:
        print('No file found for backup. Skipping.')
        return
    if prompt:
        _ = input(f'{worker.load_count()} files found '
                  f'{pretty_format_bytes(worker.load_size_in_bytes())} are to be transferred. continue ? (y) : ')
        if _ not in ['Y', 'y', '']:
            return

    print(f'{sync_entry.sync_profile.source_device.name}:{sync_entry.source_path} ->'
          f' {sync_entry.sync_profile.target_device.name}:{sync_entry.target_path} ')

    worker.backup(progress_callback=lambda current, total, transferred_bytes: print(
        "\rProgress : {0:d}/{1:d} \t Transferred {2:<16}".format(current, total, pretty_format_bytes(transferred_bytes)),
        end='', flush=True))

    print_success('\ncomplete!')


def _print_device_usage(device: Device):
    total, used, free = device.usage()
    print(f'{device.name} usage : {pretty_format_bytes(free)} / {pretty_format_bytes(total)}'
          f' ({round((used * 100) / total, 2)} %)')


def _execute(profile_name, prompt):
    sync_profile = load_sync_profile(profile_name)

    if not sync_profile.source_device.is_device_online():
        raise DeviceNotReadyError(f'Please connect {sync_profile.source_device.name}')

    _print_device_usage(sync_profile.source_device)

    if not sync_profile.target_device.is_device_online():
        raise DeviceNotReadyError(f'Please connect {sync_profile.target_device.name}')

    _print_device_usage(sync_profile.target_device)

    try:
        for entry in sync_profile.sync_entries:
            _backup_entry(entry, prompt)
    except AssertionError as ae:
        print(ae.args[0])
        exit(1)

    print_success(f'Sync for profile:{sync_profile.name} completed')


def run(**kwargs):
    profiles = kwargs['profiles']
    prompt = not kwargs.get('Y', False)

    for profile in profiles:
        try:
            _execute(profile, prompt)
        except DeviceError as de:
            print_error(de.error_message)
            exit(1)
