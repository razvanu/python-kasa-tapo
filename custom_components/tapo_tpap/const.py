"""Tapo TPAP v2 constants."""
from datetime import timedelta

DOMAIN = "tapo_tpap"
PLATFORMS = ["sensor", "switch"]
UPDATE_INTERVAL = timedelta(seconds=15)
CONF_HOST = "host"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
