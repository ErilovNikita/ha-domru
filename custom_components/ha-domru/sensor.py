from __future__ import annotations
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from domru_client.types import AgreementInfo, Agreement

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Создание сенсоров Dom.ru для каждого договора как отдельного устройства."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    sensors = []
    for agreement in coordinator.data:
        sensors.append(DomruAgreementBalanceSensor(coordinator, agreement))
    
    async_add_entities(sensors, update_before_add=True)


class DomruAgreementBalanceSensor(CoordinatorEntity, SensorEntity):
    """Сенсор баланса для одного договора (одно устройство)."""

    def __init__(self, coordinator, agreement:Agreement):
        """Инициализация сенсора для договора."""
        super().__init__(coordinator)
        self.agreement = agreement
        self._attr_name = f"Баланс {agreement.number}"
        self._attr_unique_id = f"{agreement.number}_balance"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, agreement.number)},
            "name": agreement.address.full,
            "manufacturer": "Dom.ru",
            "model": "Договор",
        }
        self._balance: float | None = None

    async def async_update(self):
        """Асинхронное обновление баланса договора."""
        try:
            agreement_number = self.agreement.number
            client = self.coordinator.client

            # Выполняем вызов API в executor
            agreement_info:AgreementInfo = await self.coordinator.hass.async_add_executor_job(
                client.get_agreement_info, agreement_number
            )

            if agreement_info and agreement_info.payment:
                self._balance = agreement_info.payment.balance
            else:
                self._balance = None

        except Exception as e:
            _LOGGER.exception("Ошибка обновления баланса для договора %s: %s", self.agreement.number, e)
            self._balance = None

    @property
    def native_value(self):
        return self._balance

    @property
    def native_unit_of_measurement(self):
        return "₽"