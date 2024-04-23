class FridaServerNotRunning(Exception):
    def __init__(self, device_serial: str):
        super().__init__(
            f"Frida server is not running on device with serial {device_serial}"
        )


class FridaDeviceNotFound(Exception):
    def __init__(self, device_serial: str):
        super().__init__(f"Device with serial {device_serial} not found")


class FridaProcessNotAttached(Exception):
    def __init__(self):
        super().__init__("No session attached. Please call attach() method first.")


class FridaTargetNotRunning(Exception):
    def __init__(self, target: [str, int]):
        if isinstance(target, int):
            super().__init__(f"Target with PID {target} is not running")
        else:
            super().__init__(f"Target {target} is not running")


class FridaPackageNotInstalled(Exception):
    def __init__(self, package_name: str):
        super().__init__(f"Package {package_name} is not installed")
