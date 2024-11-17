#api_calls.py

from datetime import date
import requests
import json
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)
def mortgage_rate()->list:
    mortgage_rate_url = 'https://api.api-ninjas.com/v1/mortgagerate'
    response = requests.get(
        mortgage_rate_url,
        headers={'X-Api-Key': 'MORTAGAGE_RATE'}
        )
    if response.status_code == requests.codes.ok:
        json.loads(response.text)[0]['data']
        frm30 = json.loads(response.text)[0]['data']['frm_30']
        frm15 = json.loads(response.text)[0]['data']['frm_15']
        logger.info(frm30, frm15)
    else:
        logger.error("Error:", response.status_code, response.text)
    
    return [ frm15, frm30 ]
