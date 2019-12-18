#!/usr/bin/python
import requests
import time
import settings as s
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def getPercentageChange(open, close):
    return format3dpCurrency(((close/open) * 100) - 100)

def textWrapper(color, payload):
    def RED():
        return bcolors.RED + payload + bcolors.ENDC
    def GREEN():
        return bcolors.GREEN + payload + bcolors.ENDC
    def BLUE():
        return bcolors.BLUE + payload + bcolors.ENDC
    def WARNING():
        return bcolors.WARNING + payload + bcolors.ENDC
    def BOLD():
        return bcolors.BOLD + payload + bcolors.ENDC
    def UNDERLINE():
        return bcolors.UNDERLINE + payload + bcolors.ENDC
    def HEADER():
        return bcolors.HEADER + payload + bcolors.ENDC

    wrap = {'RED': RED,
            'GREEN': GREEN,
            'BLUE': BLUE,
            'WARNING': WARNING,
            'BOLD': BOLD,
            'UNDERLINE': UNDERLINE,
            'HEADER': HEADER
    }

    return wrap[color]()

def format2dpCurrency(currency):
    return '{0:.2f}'.format(float(currency))

def format3dpCurrency(currency):
    return '{0:.3f}'.format(float(currency))

def float2str5precision(amount):
    precision = 5
    return "{:0.0{}f}".format(amount, precision)

def getCandleSec(open_time):
    return int(( int(time.time())*1000 - open_time ) / s.milsec_in_a_min *  100 ) 


def requests_retry_session(retries=10, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None ):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'