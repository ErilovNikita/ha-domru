# ha-domru
> Dom.Ru internet provider integration for Home Assistant. Allows you to view your account balance for contracts from your personal account.

![Latest Release](https://img.shields.io/github/v/release/ErilovNikita/ha-domru?label=Latest%20Release)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![hacs_badge](https://img.shields.io/badge/HACS-Default-green.svg)](https://github.com/custom-components/hacs)
[![HACS Validate](https://github.com/ErilovNikita/ha-domru/actions/workflows/hacs-validate.yml/badge.svg)](https://github.com/ErilovNikita/ha-domru/actions/workflows/hacs-validate.yml)

[![English](https://img.shields.io/badge/Docs-English-green.svg)](README.md)
[![Russian](https://img.shields.io/badge/Docs-Russian-green.svg)](README.ru.md)

<p align="center" float="center" width="100%">
  <img src="https://github.com/home-assistant/brands/blob/master/custom_integrations/domru/icon.png?raw=true" width="30%" /> 
  &nbsp;
  &nbsp;
  &nbsp;
  &nbsp;
  &nbsp;
  &nbsp;
  <img src="https://github.com/home-assistant/brands/blob/master/core_integrations/_homeassistant/icon.png?raw=true" width="30%" />
</p>

This integration allows you to query your Dom.Ru personal account.

Currently, you can obtain basic information on contracts connected to your personal account: Agreement Number, Balance, Tariff, etc.

> [!WARNING]  
> This integration is NOT official, and does not pretend to be. This integration is being developed solely for personal use and uses only publicly available endpoints.

> [!IMPORTANT]  
> The integration uses SSO authentication. It can only be used if you have phone number and SMS authentication configured in your personal account.

> [!IMPORTANT]  
> You need to select your region when setting up the integration, this affects the construction of queries

## Installation
### Automatically
1. In the HACS interface, search for `DomRU`
1. Install the integration
   
### Manually
Clone the repository to a temporary directory, then move it to the path `custom_components/domru`
``` sh
git clone https://github.com/ErilovNikita/ha-domru.git
mkdir -p /mnt/homeassistant/config/custom_components
mv ha-domru /config/custom_components
```

## Configuration
### Automatically
[![​Open your Home Assistant instance and start setting up a new integration.​](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=domru)

### Manually
1. Open `Settings` -> `Integrations`
1. Click the plus button in the bottom right corner of the page.
1. Enter `DomRU` in the search field.
1. Select the first result from the list.
1. Click `Continue`.
1. Fill in your login information for your personal account.
1. 🎉 Done!

