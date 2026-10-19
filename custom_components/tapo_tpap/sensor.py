"""P115 energy and electrical telemetry."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import UnitOfElectricCurrent, UnitOfElectricPotential, UnitOfEnergy, UnitOfPower
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = (
    SensorEntityDescription(key="current_consumption", name="Power", native_unit_of_measurement=UnitOfPower.WATT,
                            device_class="power", state_class="measurement"),
    SensorEntityDescription(key="voltage", name="Voltage", native_unit_of_measurement=UnitOfElectricPotential.VOLT,
                            device_class="voltage", state_class="measurement"),
    SensorEntityDescription(key="current", name="Current", native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
                            device_class="current", state_class="measurement"),
    SensorEntityDescription(key="consumption_today", name="Energy today", native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
                            device_class="energy"),
    SensorEntityDescription(key="consumption_this_month", name="Energy this month", native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
                            device_class="energy"),
)

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(TapoSensor(coordinator, entry, description) for description in SENSORS)


class TapoSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entry, description):
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id)},
            name=entry.title,
            manufacturer="TP-Link",
            model="Tapo P115",
        )

    @property
    def native_value(self):
        return self.coordinator.data.get("features", {}).get(self.entity_description.key)
