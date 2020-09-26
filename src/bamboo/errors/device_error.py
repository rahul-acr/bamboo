class DeviceError(RuntimeError):
    def __init__(self, error_message: str):
        self.error_message = error_message


class DeviceNotReadyError(DeviceError):
    def __init__(self, error_message: str):
        super().__init__(error_message)
