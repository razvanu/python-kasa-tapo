"""Config flow for the experimental Tapo P115 component."""
from __future__ import annotations

import ipaddress
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME

from .const import DOMAIN


class TapoTPAPConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """One config entry per smart plug."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                host = str(ipaddress.IPv4Address(user_input[CONF_HOST]))
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()
                # Do not attempt a connection during entry creation: on an HA
                # installation with stock kasa, TPAP support is unavailable.
                return self.async_create_entry(
                    title=f"Tapo P115 ({host})",
                    data={**user_input, CONF_HOST: host},
                )
            except ValueError:
                errors["base"] = "invalid_host"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )
