class TerminalColors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_color(color, value):
    print(f'{color}{value}{TerminalColors.ENDC}')


def print_error(value):
    print_color(TerminalColors.FAIL, value)


def print_success(value):
    print_color(TerminalColors.OK_GREEN, value)


def print_bold(value):
    print_color(TerminalColors.BOLD, value)


def print_warning(value):
    print_color(TerminalColors.WARNING, value)