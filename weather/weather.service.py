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

_UDP_IP = "192.168.201.21"
_UDP_PORT = 7001
_UDP_MESSAGE = ""
_URL = f"https://api.open-meteo.com/v1/forecast?latitude=32.711&longitude=-117.155&current=temperature_2m&temperature_unit=fahrenheit"

if __name__=='__main__':
    _logger.debug("Monitoring weather...")

    while True:
        response = requests.get(_URL)
        weather_data = json.loads(response.text)
        _UDP_MESSAGE = weather_data["current"]["temperature_2m"]                 
        _logger.debug(f"Current outside temp:{_UDP_MESSAGE}")

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        sock.sendto(_UDP_MESSAGE.encode(), (_UDP_IP, _UDP_PORT))
        sock.close()
            
        time.sleep(900)
        
_logger.debug("Weather monitor closing...")