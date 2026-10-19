"""P115 power relay. For air conditioners, use the appliance's own controls instead."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TapoRelay(coordinator, entry)])


class TapoRelay(CoordinatorEntity, SwitchEntity):
    """Relays are disabled by default to prevent accidental AC mains cutoff."""

    _attr_name = "Outlet relay"
    _attr_icon = "mdi:power-plug"

    def __init__(self, coordinator, entry):
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.unique_id}_relay"
        self._attr_entity_registry_enabled_default = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.title,
            manufacturer="TP-Link",
            model="Tapo P115",
        )

    @property
    def is_on(self):
        return self.coordinator.data.get("is_on")

    async def async_turn_on(self, **kwargs):
        await self.coordinator.async_set_relay(True)

    async def async_turn_off(self, **kwargs):
        await self.coordinator.async_set_relay(False)
