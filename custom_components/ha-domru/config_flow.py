from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN

# Импорт локальной версии domru-client
from domru_client import DomRuClient
from domru_client.exceptions import AuthenticationError, DataFetchError

_LOGGER = logging.getLogger(__name__)


class DomruConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config Flow для интеграции Dom.ru"""
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Шаг ввода номера телефона для авторизации."""
        if user_input is not None:
            phone = user_input["Phone"]

            try:
                # Создаём клиент синхронно через executor
                client: DomRuClient = await self.hass.async_add_executor_job(DomRuClient, phone)
            except Exception as e:
                _LOGGER.exception("Ошибка создания клиента DomRuClient: %s", e)
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_phone_schema(),
                    errors={"base": "cannot_connect"}
                )

            # Получаем список регионов
            try:
                regions = await self.hass.async_add_executor_job(client.get_region_list)
            except Exception as e:
                _LOGGER.exception("Ошибка получения списка регионов: %s", e)
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_phone_schema(),
                    errors={"base": "cannot_fetch_regions"}
                )

            self.context["client"] = client
            self.context["regions"] = regions
            return await self.async_step_region()

        return self.async_show_form(
            step_id="user",
            data_schema=self._get_phone_schema()
        )

    async def async_step_region(self, user_input: dict[str, Any] | None = None):
        """Шаг выбора региона регистрации личного кабинета."""
        client: DomRuClient = self.context["client"]
        regions = self.context["regions"]

        if user_input is not None:
            region_index = user_input["Region"]
            # Устанавливаем регион через executor
            await self.hass.async_add_executor_job(client.set_region, regions[region_index])
            return await self.async_step_otp()

        region_names = [r.name for r in regions]

        return self.async_show_form(
            step_id="region",
            data_schema=vol.Schema({
                vol.Required(
                    "Region",
                    description={"suggested_value": 0}
                ): vol.In({i: name for i, name in enumerate(region_names)})
            })
        )

    async def async_step_otp(self, user_input: dict[str, Any] | None = None):
        """Шаг ввода кода из SMS."""
        client: DomRuClient = self.context["client"]

        # Если ещё не инициировали start_authorization
        if "csrf_token" not in self.context:
            try:
                csrf_token, otp_url = await self.hass.async_add_executor_job(client.start_authorization)
                self.context["csrf_token"] = csrf_token
                self.context["otp_url"] = otp_url
            except Exception as e:
                _LOGGER.exception("Ошибка старта авторизации: %s", e)
                return self.async_show_form(
                    step_id="otp",
                    data_schema=self._get_otp_schema(),
                    errors={"base": "cannot_connect"}
                )

            # Показываем форму для ввода кода
            return self.async_show_form(
                step_id="otp",
                data_schema=self._get_otp_schema()
            )

        # Пользователь ввёл код
        if user_input is not None:
            otp_code = user_input["OTP"]
            try:
                await self.hass.async_add_executor_job(
                    client.finish_authorization,
                    self.context["csrf_token"],
                    self.context["otp_url"],
                    otp_code
                )
                auth_dict = {
                    "access_token": client.authorization.access_token,
                    "refresh_token": client.authorization.refresh_token,
                    "token_expiry": client.authorization.token_expiry
                }
            except AuthenticationError:
                return self.async_show_form(
                    step_id="otp",
                    data_schema=self._get_otp_schema(),
                    errors={"base": "Ошибка авторизации, неверный OTP код"}
                )
            except DataFetchError:
                return self.async_show_form(
                    step_id="otp",
                    data_schema=self._get_otp_schema(),
                    errors={"base": "Проверка OTP кода не удалась"}
                )
            except Exception as e:
                _LOGGER.exception("Ошибка завершения авторизации: %s", e)
                return self.async_show_form(
                    step_id="otp",
                    data_schema=self._get_otp_schema(),
                    errors={"base": "cannot_connect"}
                )

            # Успешная авторизация
            return self.async_create_entry(
                title=f"Учетная запись ({client.phone})",
                data={
                    "phone": client.phone,
                    "auth_tokens": auth_dict
                }
            )

        # Форма по умолчанию для ввода кода
        return self.async_show_form(
            step_id="otp",
            data_schema=self._get_otp_schema()
        )

    @staticmethod
    def _get_phone_schema():
        return vol.Schema({
            vol.Required(
                "Phone",
                description={"suggested_value": "+7"}
            ): str
        })

    @staticmethod
    def _get_otp_schema():
        return vol.Schema({
            vol.Required("OTP"): str
        })