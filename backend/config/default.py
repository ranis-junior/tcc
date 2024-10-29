import os
from reader.usb_reader import UsbReader
from reader.gpio_reader import GpioReader
from reader.serial_reader import SerialReader

config = {
    'usb': UsbReader,
    'gpio': GpioReader,
}


class Config:
    port = os.getenv('port')
    baudrate = os.getenv('baudrate')
    gpio_port = os.getenv('gpio_port', None)
    sqlalchemy_database_url = os.getenv('sqlalchemy_database_url')
    connection_type: SerialReader = config.get(os.getenv('connection_type', None))

    @staticmethod
    def init_app(app):
        pass
