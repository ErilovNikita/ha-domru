from __future__ import annotations
import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from domru_client.types import AgreementInfo, AgreementInfoPersonalAddress

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

    for agreement_number, agreement_info in coordinator.data.items():
        sensors.append(DomruAgreementBalanceSensor(coordinator, agreement_number))
        sensors.append(DomruAgreementTariffSensor(coordinator, agreement_number))

    async_add_entities(sensors, update_before_add=True)
    _LOGGER.debug("Создано %d сенсоров Dom.ru", len(sensors))


class DomruBaseSensor(CoordinatorEntity, SensorEntity):
    """Базовый класс для сенсоров Dom.ru с общим device_info."""

    def __init__(self, coordinator, agreement_number: str):
        agreement_info:AgreementInfo = coordinator.data.get(agreement_number)

        self.agreement_number = agreement_number
        address:AgreementInfoPersonalAddress  = agreement_info.personal.address
        building_part = f", стр. {address.building}" if address.building else ""

        self._attr_device_info = {
            "identifiers": {(DOMAIN, agreement_number)},
            "name": f"Договор {agreement_number}",
            "manufacturer": agreement_info.personal.fio,
            "model" : f"г. {address.city}, ул. {address.street}, д. {address.house}{building_part}, кв. {address.flat}"
        }
        
        super().__init__(coordinator)

class DomruAgreementBalanceSensor(DomruBaseSensor):
    """Сенсор баланса договора."""

    def __init__(self, coordinator, agreement_number: str):
        self._attr_unique_id = f"{DOMAIN}_{agreement_number}_balance"
        self._attr_name = "Баланс"
        self._attr_icon = "mdi:currency-rub"

        super().__init__(coordinator, agreement_number)

    @property
    def native_value(self):
        agreement_info:AgreementInfo = self.coordinator.data.get(self.agreement_number)
        if agreement_info and agreement_info.payment:
            return agreement_info.payment.balance
        return None

    @property
    def native_unit_of_measurement(self):
        return "₽"

class DomruAgreementTariffSensor(DomruBaseSensor):
    """Сенсор тарифа и платёжных данных."""

    def __init__(self, coordinator, agreement_number: str):
        self._attr_unique_id = f"{DOMAIN}_{agreement_number}_tariff"
        self._attr_name = "Тариф"
        self._attr_icon = "mdi:tag"
        self._attr_native_unit_of_measurement = None
        self._attr_state_class = None
        self._attr_device_class = None

        super().__init__(coordinator, agreement_number)

    @property
    def native_value(self):
        agreement_info:AgreementInfo = self.coordinator.data.get(self.agreement_number)
        if agreement_info and agreement_info.products:
            return agreement_info.products.tariff_name
        return "Неизвестно"

    @property
    def extra_state_attributes(self):
        agreement_info:AgreementInfo = self.coordinator.data.get(self.agreement_number)
        if agreement_info and agreement_info.payment and agreement_info.products:
            return {
                "tariff_price": getattr(agreement_info.products, "tariff_price", None),
                "pay_sum": getattr(agreement_info.payment, "pay_sum", None),
                "pay_charges_sum": getattr(agreement_info.payment, "pay_charges_sum", None),
                "pay_text_short": agreement_info.payment.pay_text_Short.replace('&nbsp;', '') if agreement_info.payment.pay_text_Short else None,
            }
        else:
            return {}