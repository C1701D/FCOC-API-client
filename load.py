from typing import Optional, Dict, Any
import json
import logging
from threading import Thread
import os
import requests


plugin_name = os.path.basename(os.path.dirname(__file__))


logger = logging.getLogger(f'FCOC-API.{plugin_name}')


if not logger.hasHandlers():
    level = logging.INFO
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)


def send_API_update(type, url, data):
    if type == "CarrierJumpRequest":
        msg = requests.post(f"{url}/carrier-jump-request/", data)
        if msg.status_code == 200:
            logger.info(f'FCOC API update posted successfully. Type: {type}; Code: {msg.status_code}')
        else:
            logger.warning(f'FCOC API update was not posted successfully. Type: {type}; Code: {msg.status_code}')


def plugin_start3(plugin_dir: str) -> str:
    logger.info('FCOC API client loaded successfully.')
    return "FCOC-API"


def journal_entry(cmdr: str, is_beta: bool, system: str, station: str, entry: Dict[str, Any], state: Dict[str, Any]) -> Optional[str]:
    if entry['event'] == 'CarrierJumpRequest':
        url = "http://api.fcoc.space:8080"
        thread = Thread(target=send_API_update, args=("CarrierJumpRequest", url, json.dumps(entry)))
        thread.start()