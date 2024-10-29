from builtins import bytes

from reader.serial_reader import SerialReader
from serial import Serial


class UsbReader(SerialReader):
    def __init__(self, port: str, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = Serial(self.port, baudrate=self.baudrate)
        self.alive = False

    def open(self):
        if self.alive:
            raise IOError('Serial already open')
        self.serial.open()
        self.serial.reset_input_buffer()
        self.alive = True

    def read_line(self) -> str | None:
        if not self.is_alive():
            raise IOError('Serial not open')
        if self.serial.in_waiting > 0:
            return self.serial.readline().decode("utf-8")
        return None

    def available(self) -> bool:
        return self.serial.in_waiting > 0

    def read(self, size: int = 1024) -> bytes:
        if not self.is_alive():
            raise IOError('Serial not open')
        if self.serial.in_waiting > 0:
            return self.serial.read(size)
        return bytes(0)

    def is_alive(self) -> bool:
        return not self.serial.closed and self.alive

    def close(self):
        if not self.alive:
            raise IOError('Serial already closed')
        self.serial.close()
        self.alive = False

    def __enter__(self):
        if not self.serial.is_open:
            self.open()
        self.alive = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.serial and self.alive:
            self.serial.close()
            self.alive = False
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_val}")
            print(f"Traceback: {exc_tb}")
        return False
