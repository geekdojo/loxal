import logging
import logging.handlers
import json
import requests
import socket
import time

_logger = logging.getLogger('doorbell')
_logger.setLevel(logging.DEBUG)
_handler = logging.handlers.SysLogHandler(address = '/dev/log')
_logger.addHandler(_handler)

_URL = f"https://api.open-meteo.com/v1/forecast?latitude=32.711&longitude=-117.155&current=temperature_2m,relative_humidity_2m,wind_speed_10m,rain,cloud_cover&wind_speed_unit=mph&temperature_unit=fahrenheit&precipitation_unit=inch"

_UDP_IP = "192.168.201.21"
_UDP_PORT_TEMPERATURE = 7001

def sendUdp(msg, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(msg.encode(), (_UDP_IP, port))
    sock.close()

if __name__=='__main__':
    _logger.debug("Monitoring weather...")

    while True:
        try:
            response = requests.get(_URL)
            weather_data = json.loads(response.text)
            temperature = str(weather_data["current"]["temperature_2m"])
            humidity = str(weather_data["current"]["relative_humidity_2m"])
            wind_speed = str(weather_data["current"]["wind_speed_10m"])
            rain = str(weather_data["current"]["rain"])
            sendUdp(temperature, _UDP_PORT_TEMPERATURE)
            _logger.debug(f"Current outside temp:{temperature}")
        except Exception as e:
            _logger.error(f"Error fetching weather data: {e}")
            time.sleep(900)
            continue

        time.sleep(900)

        
_logger.debug("Weather monitor closing...")