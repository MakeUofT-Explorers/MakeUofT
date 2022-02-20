import serial
import pynmea2

class GPS:
    def __init__(self, port="dev/serial0"):
        self.port = serial.Serial(self.port, baudrate = 9600, timeout = 0.5)

    def position(self):
        NMEA_sentence = self.port.readline()
        lat, lat_dir, lon, lon_dir, altitude, altitude_units = self._parse_sentence(NMEA_sentence)
        return lat, lat_dir, lon, lon_dir, altitude, altitude_units

    @staticmethod
    def _parse_sentence(NMEA_sentence):
        if NMEA_sentence.find("GGA") > 0:
            msg = pynmea2.parse(NMEA_sentence)
            return msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units

