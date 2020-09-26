import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bamboo', description='Bamboo backup')
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('device')
    subparsers.add_parser('profile')

    backup_parser = subparsers.add_parser('backup')
    backup_parser.add_argument('profiles', nargs='+')
    backup_parser.add_argument('-Y', action='store_true')

    subparsers.add_parser('about')

    args = parser.parse_args()

    command = args.command

    if command == 'device':
        from bamboo.command.device_command import run
    elif command == 'profile':
        from bamboo.command.profile_command import run
    elif command == 'backup':
        from bamboo.command.backup_command import run
    elif command == 'about':
        from bamboo.command.about_command import run
    else:
        parser.error('Invalid usage')

    run(**args.__dict__)
