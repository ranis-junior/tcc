from abc import ABC, abstractmethod


class SerialReader(ABC):
    @abstractmethod
    def read_line(self) -> str:
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def read(self, size: int = 1024) -> bytes:
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def is_alive(self) -> bool:
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def available(self) -> bool:
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def open(self):
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def close(self):
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def __enter__(self):
        raise NotImplementedError('Abstract method should be implemented.')

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError('Abstract method should be implemented.')
