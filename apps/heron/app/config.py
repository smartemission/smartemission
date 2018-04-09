import os
import logging

DEFAULT_PROXY_REFERERS = 'localhost,smartemission.nl,geonovum.nl,heron-mc.org'
DEFAULT_PROXY_HOSTS = 'map5.nl,knmi.nl,nationaalgeoregister.nl,nlextract.nl,rivm.nl,smartemission.nl'

# local config, change on server for real config
config = {
    'proxy_referers': os.getenv('HERON_PROXY_REFERERS', DEFAULT_PROXY_REFERERS),
    'proxy_hosts': os.getenv('HERON_PROXY_HOSTS', DEFAULT_PROXY_HOSTS),
    'loglevel': int(os.getenv('HERON_LOG_LEVEL', logging.DEBUG))
}
