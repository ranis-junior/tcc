from reader.serial_reader import SerialReader


class GpioReader(SerialReader):
    def available(self) -> bool:
        pass

    def read_line(self) -> str:
        pass

    def read(self, size: int = 1024) -> bytes:
        pass

    def is_alive(self) -> bool:
        pass

    def open(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
