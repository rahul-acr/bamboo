def bytes_to_mb(value_in_bytes):
    return (value_in_bytes / 1024) / 1024


def pretty_size_in_mb(value_in_bytes):
    return round(bytes_to_mb(value_in_bytes), 2)


def pretty_format_bytes(value_in_bytes):
    formats = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB']
    value = value_in_bytes
    divisions = 0
    while value > 1024:
        value /= 1024
        divisions += 1
    return f'{round(value, 2)} {formats[divisions]}'
