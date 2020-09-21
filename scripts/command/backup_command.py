from backup.backup_worker import BackupWorker
from errors.device_error import DeviceNotReadyError, DeviceError
from sync.configuration import load_sync_profile
from sync.sync import Device
from sync.sync import SyncEntry
from utils.printing import print_error, print_success, print_warning
from utils.size_utils import pretty_format_bytes


def print_progress(current, total, transferred_bytes):
    print(
        "\rProgress : {0:d}/{1:d} \t Transferred {2:s}".format(current, total, pretty_format_bytes(transferred_bytes)),
        end='', flush=True)


def backup_entry(sync_entry: SyncEntry):
    print(f'Syncing:{sync_entry.name}')

    print_warning('Gathering info ...')
    worker = BackupWorker(sync_entry)
    worker.collect_source_info()

    if worker.load_count() == 0:
        print('No file found for backup. Skipping.')
        return
    _ = input(f'{worker.load_count()} files found '
              f'{pretty_format_bytes(worker.load_size_in_bytes())} are to be transferred. continue ? (y) : ')
    if _ not in ['Y', 'y', '']:
        return

    worker.backup(progress_callback=print_progress)
    print_success('\ncomplete!')


def print_device_usage(device: Device):
    total, used, free = device.usage()
    print(f'{device.name} usage : {pretty_format_bytes(free)} / {pretty_format_bytes(total)}'
          f' ({round((used * 100) / total, 2)} %)')


def execute(profile_name):
    sync_profile = load_sync_profile(profile_name)

    # Print usage information
    if not sync_profile.source_device.is_device_online():
        raise DeviceNotReadyError(f'Please connect {sync_profile.source_device.name}')

    print_device_usage(sync_profile.source_device)

    if not sync_profile.target_device.is_device_online():
        raise DeviceNotReadyError(f'Please connect {sync_profile.target_device.name}')

    print_device_usage(sync_profile.target_device)

    try:
        for entry in sync_profile.sync_entries:
            backup_entry(entry)
    except AssertionError as ae:
        print(ae.args[0])
        exit(1)

    print_success(f'Sync for profile:{sync_profile.name} completed')


def run(**kwargs):
    profiles = kwargs['profiles']

    for profile in profiles:
        try:
            execute(profile)
        except DeviceError as de:
            print_error(de.error_message)
            exit(1)
