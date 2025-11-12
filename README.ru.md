# ha-domru
> Интеграция Интернет-провайдера Дом.Ру для Home Assistant. Позволяющая видеть состояние лицевого счета по договорам из личного кабинета.

![Latest Release](https://img.shields.io/github/v/release/ErilovNikita/ha-domru?label=Latest%20Release)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-green.svg)](https://github.com/hacs/default)
[![HACS Validate](https://github.com/ErilovNikita/ha-domru/actions/workflows/hacs-validate.yml/badge.svg)](https://github.com/ErilovNikita/ha-domru/actions/workflows/hacs-validate.yml)

# Dom.ru Home Assistant Integration

[![English](https://img.shields.io/badge/Docs-English-green.svg)](README.md)
[![Russian](https://img.shields.io/badge/Docs-Russian-green.svg)](README.ru.md)

<p align="center" float="center" width="100%">
  <img src="https://github.com/home-assistant/brands/blob/master/custom_integrations/domru/icon.png?raw=true" width="20%" /> 
  &nbsp;
  &nbsp;
  &nbsp;
  &nbsp;
  &nbsp;
  &nbsp;
  <img src="https://github.com/home-assistant/brands/blob/master/core_integrations/_homeassistant/icon.png?raw=true" width="20%" />
</p>

Данная интеграция предоставляет возможность опрашивать личный кабинет Дом.Ру.

На текущий момент имеется возможность получать основную информацию по договорам, подключенным в ЛК: Номер договора, Баланс, Тариф, и т.д.

> [!WARNING]  
> Данная интеграция является НЕ официальной, и не пытается ей казаться. Данная интеграция разрабатывается исключительно в личных интересах, и использует только общедоступные endpoint'ы.

> [!IMPORTANT]  
> Интеграция использует SSO авторизацию. Использование возможно, только если у вас в личном кабинете настроена авторизация по Номеру телефона и СМС. 

> [!IMPORTANT]  
> Важно выбирать именно свой регион при настройке интеграции, это влияет на построение запросов

## Установка
### Автоматически
1. Через интерфейс HACS найдите `DomRU`
1. Установите интеграцию

### Вручную
Клонируйте репозиторий во временный каталог, затем переместите по пути `custom_components/domru`
``` sh
git clone https://github.com/ErilovNikita/ha-domru.git
mkdir -p /mnt/homeassistant/config/custom_components
mv ha-domru /config/custom_components
```

## Конфигурация
### Автоматически
[![​Open your Home Assistant instance and start setting up a new integration.​](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=domru)

### Вручную
1. Откройте `Настройки` -> `Интеграции`
1. Нажмите внизу справа страницы кнопку с плюсом
1. Введите в поле поиска `DomRU`
1. Выберите первый результат из списка
1. Нажмите кнопку `Продолжить`
1. Заполните данные для авторизации в личном кабинете
1. 🎉 Готово! 

## License
Данный проект лицензирован по лицензии Apache 2.0 — подробности см. в файле [LICENSE](ЛИЦЕНЗИЯ).