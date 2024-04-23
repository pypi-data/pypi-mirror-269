from functools import wraps

import frida
from frida.core import Device

from ares._frida._frida_exception import *


class FridaHooker:
    _device: frida.core.Device
    _session: frida.core.Session
    _attached_pid: int
    _running_script: list[frida.core.Script]

    @staticmethod
    def __check_session(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            if self._session is None:
                raise FridaProcessNotAttached()
            return func(self, *args, **kwargs)

        return inner

    @staticmethod
    def __get_frida_device(device_serial: str) -> [Device | None]:
        try:
            return frida.get_device(device_serial)
        except frida.ServerNotRunningError:
            return None

    def __init__(self, device_serial: str):
        self._device = self.__get_frida_device(device_serial)
        if self._device is None:
            raise FridaServerNotRunning(device_serial)

    def __del__(self):
        if self._running_script:
            for script in self._running_script:
                script.unload()
        if self._session is not None:
            self._session.detach()

    def __is_package_running(self, target: [str | int]) -> bool:
        return target in [process.pid if isinstance(target, int) else process.name
                          for process in self._device.enumerate_processes()]

    def __is_package_installed(self, package_name: str) -> bool:
        return package_name in [app.identifier for app in
                                self._device.enumerate_applications()]

    def __get_pid(self, target: [str | int]) -> int:
        if isinstance(target, int):
            return target
        return self._device.get_process(target).pid

    def attach(self, target: [str | int]) -> "FridaHooker":
        """
        :param target: The target to attach to.
        Can be either a string
            representing the process name or an integer
            representing the process ID.
        :return: An instance of FridaHooker
        that is attached to the specified target.

        """
        if not self.__is_package_running(target):
            raise FridaTargetNotRunning(target)
        target = self.__get_pid(target)
        if self._session is None:
            self._session = self._device.attach(target)
            self._attached_pid = target
        else:
            self._session.detach()
            self._session = self._device.attach(target)
            self._attached_pid = target
        return self

    def spawn(self, package_name: str, resume=True) -> "FridaHooker":
        if not self.__is_package_installed(package_name):
            raise FridaPackageNotInstalled(package_name)
        pid = self._device.spawn(package_name)
        self._session = self._device.attach(pid)
        self._attached_pid = pid
        if resume:
            self.resume()
        return self

    def resume(self) -> "FridaHooker":
        if self._attached_pid is not None:
            self._device.resume(self._attached_pid)
        return self

    @__check_session
    def run_script(self, script: str) -> "FridaHooker":
        # TODO: record script, check if script is running(use hash to identify script)
        self._running_script.append(self._session.create_script(script))
        return self
