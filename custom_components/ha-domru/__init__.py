from __future__ import annotations
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from domru_client import DomRuClient
from domru_client.types import AuthTokens, Agreement, Region
from domru_client.exceptions import AuthenticationError, DataFetchError

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Настройка интеграции Dom.ru по записи конфигурации."""

    phone = entry.data["phone"]
    auth_dict = entry.data["auth_tokens"]
    region_dict = entry.data["region_dict"]

    region = Region(**region_dict)
    auth_tokens = AuthTokens(**auth_dict)

    _LOGGER.debug("Настройка интеграции Dom.ru для %s", phone)
    _LOGGER.debug("Auth tokens: %s", auth_tokens)

    # Создание клиента с нужным регионом
    client: DomRuClient = await hass.async_add_executor_job(DomRuClient, phone, auth_tokens)
    await hass.async_add_executor_job(client.set_region, region)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"client": client}

    # Создаём координатор обновления данных
    coordinator = DomruDataUpdateCoordinator(hass, client)
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id]["coordinator"] = coordinator

    # Загружаем платформы (сенсоры, возможно потом добавим switch, binary_sensor и т.д.)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Разгрузка интеграции."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class DomruDataUpdateCoordinator(DataUpdateCoordinator):
    """Координатор для периодического обновления данных Dom.ru."""

    def __init__(self, hass: HomeAssistant, client: DomRuClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Dom.ru Data Coordinator",
            update_interval=timedelta(minutes=10),
        )
        self.client = client

    async def _async_update_data(self):
        """Обновление данных с сервера Dom.ru."""
        try:
            # Обновление токена
            await self.hass.async_add_executor_job(self.client.refresh_access_token)

            agreements:list[Agreement] = await self.hass.async_add_executor_job(self.client.get_agreements)
            _LOGGER.debug("Получено %s договоров", str(len(agreements)))

            # Загружаем подробности по каждому договору
            detailed = {}
            for agreement in agreements:
                agreement_info = await self.hass.async_add_executor_job(
                    self.client.get_agreement_info,
                    agreement.number
                )
                detailed[agreement.number] = agreement_info
                _LOGGER.debug("Данные по договору %s обновлены", agreement.number)

            return detailed

        except (AuthenticationError, DataFetchError) as err:
            raise UpdateFailed(f"Ошибка при получении данных: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Неизвестная ошибка: {err}") from err