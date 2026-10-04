# Solakon ONE Home Assistant Integration

A complete Home Assistant custom integration for Solakon ONE devices using Modbus TCP communication.

> ⚠️ **IMPORTANT**: This is a Home Assistant **Integration**, not an Add-on.
> - Do NOT add this as an Add-on repository
> - Install it through HACS as an Integration (see instructions below)

## Changelog

### Latest Version
**New Features:**
- ✨ **Device Control Entities**: Control your Solakon ONE device directly from Home Assistant
  - EPS Output Mode control (Disable/EPS/UPS)
  - Remote Control Mode with 9 operating modes
  - Battery SoC limits (Minimum/Maximum/OnGrid)
  - Remote Active/Reactive Power control
  - Remote timeout settings
- 📊 **New Sensors**: Added control status sensors to monitor current device settings
  - EPS Output Mode status
  - Battery SoC limit settings
  - Remote control status and commands
  - Network status
- 🔧 **Improved Energy Dashboard Integration**: Comprehensive documentation for battery integration workaround
- 📖 **Documentation Updates**: Accurate Energy Dashboard integration guide with step-by-step battery setup

**Bug Fixes:**
- Fixed misleading documentation about Grid Import/Export sensors (not currently supported)
- Corrected Energy Dashboard integration instructions

### Previous Versions
- Initial release with basic monitoring capabilities

## Features

### Monitoring
- Real-time monitoring of all inverter parameters
- PV string monitoring (voltage, current, power)
- Battery management (SOC, power, voltage, current, temperature)
- Energy statistics (total and daily generation)
- Temperature monitoring
- Alarm and status monitoring
- Power factor and grid frequency monitoring

### Device Control
- **EPS Output Control**: Switch between Disable, EPS Mode, and UPS Mode
- **Remote Control Mode**: 9 different operating modes including:
  - INV Discharge/Charge (PV Priority or AC First)
  - Battery Discharge/Charge
  - Grid Discharge/Charge
- **Battery SoC Management**: Set minimum and maximum state of charge limits
- **Remote Power Control**: Set active and reactive power commands
- **Timeout Management**: Configure remote control timeout settings

### Integration
- Full UI configuration support
- Configurable update intervals
- Energy Dashboard compatible (solar production works out-of-the-box)
- Battery integration works directly with native energy sensors

## Monitored Sensors

### Power Sensors
- PV Power (total from all strings)
- Active Power
- Reactive Power
- Load Power
- Battery Power

### Voltage & Current
- PV1/PV2/PV3/PV4 Voltage & Current
- Grid Phase Voltages (R/S/T)
- Battery Voltage & Current
- Load Voltage & Current

### Energy Statistics
- Total Energy Generated
- Daily Energy Generation

### Battery Information
- Battery Power
- Battery Voltage
- Battery Current
- Battery State of Charge (SOC)

### System Information
- Internal Temperature
- Power Factor
- Grid Frequency
- Network Status

### Control Status Sensors
These sensors display the current values of controllable parameters:
- EPS Output Mode (current mode: Disable/EPS/UPS)
- Minimum/Maximum/OnGrid SoC Settings
- Remote Control Status
- Remote Active/Reactive Power Commands
- Remote Timeout Settings

## Installation

### Prerequisites
- Home Assistant 2024.1.0 or newer
- HACS (Home Assistant Community Store) installed
- Your Solakon ONE device connected to your network with Modbus TCP enabled

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on **"Integrations"** (NOT Add-ons!)
3. Click the **three dots menu** in the top right → **"Custom repositories"**
4. Add this repository URL: `https://github.com/solakon-de/solakon-one-homeassistant`
5. Select category: **"Integration"** (⚠️ NOT "Add-on"!)
6. Click **"Add"**
7. Close the custom repositories dialog
8. Click **"+ Explore & Download Repositories"**
9. Search for **"Solakon ONE"** and install it
10. **Restart Home Assistant**
11. Go to **Settings → Devices & Services**
12. Click **"+ Add Integration"**
13. Search for **"Solakon ONE"** and configure it

### Manual Installation

1. Copy the `custom_components/solakon_one` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the integration via Settings → Devices & Services

## Configuration

### Via UI (Recommended)

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Solakon ONE"
4. Enter configuration:
   - **Host**: IP address of your Solakon ONE device
   - **Port**: Modbus TCP port (default: 502)
   - **Device Name**: Friendly name for your device
   - **Modbus Device ID**: Usually 1 (range: 1-247)
   - **Update Interval**: How often to poll (1-300 seconds)

### Changing the IP Address or Port

If your Solakon ONE gets a new IP address, you do not need to delete and re-add
the integration:

1. Go to Settings → Devices & Services
2. Find the **Solakon ONE** entry, click the three dots menu → **"Reconfigure"**
3. Enter the new **Host**, **Port**, or **Modbus Device ID**
4. Submit — Home Assistant verifies the device is reachable and reloads the integration

All entities keep their entity IDs, custom names, and recorded history.

### Network Requirements

- Ensure your Solakon ONE device is connected to your network
- Modbus TCP must be enabled on the device
- Default Modbus TCP port is 502
- Device must be accessible from Home Assistant

## Device Control

The integration provides control entities to manage your Solakon ONE device directly from Home Assistant.

### Select Entities

**EPS Output Control**
- Switch between operating modes:
  - `Disable`: EPS output disabled
  - `EPS Mode`: Emergency Power Supply mode
  - `UPS Mode`: Uninterruptible Power Supply mode

**Remote Control Mode**
- Control device operation with 9 modes:
  - `Disabled`: Remote control off
  - `INV Discharge (PV Priority)`: Inverter discharge with PV priority
  - `INV Charge (PV Priority)`: Inverter charge with PV priority
  - `Battery Discharge`: Direct battery discharge
  - `Battery Charge`: Direct battery charge
  - `Grid Discharge`: Grid-powered discharge
  - `Grid Charge`: Grid-powered charge
  - `INV Discharge (AC First)`: Inverter discharge with AC priority
  - `INV Charge (AC First)`: Inverter charge with AC priority

### Number Entities

**Battery SoC Management**
- `Minimum state of charge`: Set minimum battery state of charge (0-100%)
- `Maximum state of charge`: Set maximum battery state of charge (0-100%)
- `Minimum state of charge (on-grid)`: Set minimum SoC when grid-connected (0-100%)

**Remote Power Control**
- `Remote control power`: Set active power command (-100kW to +100kW)
  - Negative values = charging/import
  - Positive values = discharging/export
- `Remote control reactive power`: Set reactive power command (-100kVAR to +100kVAR)
- `Remote control timeout`: Set timeout for remote control commands (0-3600 seconds). The sensor `Remote timeout countdown` shows the remaining time.
- `Force mode power`: Power for force charge or force discharge (0-1200W)
- `Grid export power limit`: Maximum power that is exported to the grid (0-1200W)

### Remote Control: Order of Steps

Remote control only stays active while a timeout above 0 is set. Set the entities in this order:

1. `Remote control timeout` to a value above 0, e.g. 60 seconds. With a timeout of 0 the device switches the mode back to `Disabled` right away.
2. `Remote control mode` to the desired mode.
3. `Remote control power` to the desired power. A power value written before the mode and timeout are set is reset to 0.

Example: discharge 200W with PV priority.

```yaml
actions:
  - action: number.set_value
    target:
      entity_id: number.solakon_one_remote_control_timeout
    data:
      value: 60
  - action: select.select_option
    target:
      entity_id: select.solakon_one_remote_control_mode
    data:
      option: "1"
  - action: number.set_value
    target:
      entity_id: number.solakon_one_remote_control_power
    data:
      value: 200
```

If Home Assistant runs in German, the entity IDs are German, e.g. `number.solakon_one_fernsteuerung_zeituberschreitung`. See [Entity Names (English / German)](#entity-names-english--german).

> ⚠️ **Warning**: Modifying these settings can affect your system's operation. Make sure you understand what each setting does before changing it. Some settings may require the device to be in specific modes to take effect.

## Troubleshooting

### Connection Issues

1. Verify network connectivity:
   ```bash
   ping <device-ip>
   ```

2. Test Modbus connection:
   ```bash
   telnet <device-ip> 502
   ```

3. Check Home Assistant logs:
   ```
   Settings → System → Logs → Search for "solakon"
   ```

### Common Issues

- **Cannot connect**: Verify IP address and port are correct — if the device's IP changed, use *Reconfigure* (see [Changing the IP Address or Port](#changing-the-ip-address-or-port))
- **No data**: Check Modbus device ID (usually 1)
- **Intermittent data**: Increase update interval if network is slow
- **Missing sensors**: Some sensors only appear if hardware is present (e.g., battery sensors)

## Energy Dashboard Integration

### Solar Production (Works Out-of-the-Box)

To add solar production to your Energy Dashboard:

1. Go to Settings → Dashboards → Energy
2. Under **Solar production**, select "PV Energy" and "PV Power"

### Battery Integration (Works Directly)

The integration provides native `Battery charge energy` and `Battery discharge energy` sensors, so no helpers are needed for the Energy Dashboard:

1. Go to Settings → Dashboards → Energy
2. Under **Battery systems**, click "Add battery system".
3. Configure:
   - **Energy going in to the battery**: Select the `Battery charge energy` sensor.
   - **Energy going out of the battery**: Select the `Battery discharge energy` sensor.

#### Optional: Real Time Power Display

If you also want live power values on the battery card, create two template power sensors first.

Go to Settings → Devices & Services → Helpers → Create Helper → Template → Template a sensor

Create two template sensors with the following settings:

**Battery Discharge Power:**
- Name: `Battery Discharge Power`
- State template: `{{ max(0, states('sensor.solakon_one_battery_power') | float(default=0)) }}`
- Unit of measurement: `W`
- Device class: `Power`
- State class: `Measurement`

**Battery Charge Power:**
- Name: `Battery Charge Power`
- State template: `{{ max(0, 0 - states('sensor.solakon_one_battery_power') | float(default=0)) }}`
- Unit of measurement: `W`
- Device class: `Power`
- State class: `Measurement`

#### Assign the Power Sensors

Back on the battery system card, you can assign the template sensors created above for real time information:
   - **Power going in to the battery**: Select the `Battery Charge Power` template sensor.
   - **Power going out of the battery**: Select the `Battery Discharge Power` template sensor.

### Grid Import/Export (Not Currently Supported)

Grid import and export sensors are not currently available in this integration. The sensors `AC output energy` (register 39621) and `AC input energy` (register 39625) count the energy at the AC connection of the device, not at the grid connection of the house: output is everything the device delivered (PV and battery), input is everything it charged from AC. They are not suitable as grid import/export in the Energy Dashboard. Real grid values require a meter or CT.

### Solakon PowerTracker IR Integration

You can integrate the Solakon PowerTracker IR via Home Assistant's REST sensor. Add the following to your `configuration.yaml`:

```yaml
rest:
  - resource: "http://<TRACKER_IP>/api/v1/status"
    scan_interval: 1
    sensor:
      - name: "Solakon PowerTracker IR"
        value_template: "{{ value_json.extracted.instantaneous_power_w }}"
```

Replace `<TRACKER_IP>` with the IP address of your PowerTracker IR.

> **Note**: After adding this configuration, reload the REST integration via Developer Tools → YAML → REST. A full Home Assistant restart is not required.

## Automation Examples

### Battery Power Monitoring
```yaml
automation:
  - alias: "Battery Discharging Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.solakon_one_battery_power
        above: 5000  # Alert when discharging more than 5kW
    action:
      - service: notify.mobile_app
        data:
          message: "Battery is discharging at high rate!"
```

### Control Battery SoC Based on Time
```yaml
automation:
  - alias: "Set Battery Limits for Night"
    trigger:
      - platform: time
        at: "22:00:00"
    action:
      - service: number.set_value
        target:
          entity_id: number.solakon_one_minimum_soc_control
        data:
          value: 20
      - service: number.set_value
        target:
          entity_id: number.solakon_one_maximum_soc_control
        data:
          value: 100
```

### Switch to EPS Mode on Grid Failure
```yaml
automation:
  - alias: "Enable EPS Mode on Grid Loss"
    trigger:
      - platform: state
        entity_id: sensor.solakon_one_network_status
        to: "0"  # Adjust based on your grid status values
    action:
      - service: select.select_option
        target:
          entity_id: select.solakon_one_eps_output_control
        data:
          option: "EPS Mode"
```

## Device Control via Entities

Device control is implemented using Home Assistant entities (Select and Number entities). Use these entities in your dashboards and automations:

**Available Control Entities** (entity IDs with Home Assistant in English):
- `select.solakon_one_output`: EPS/UPS mode selection
- `select.solakon_one_remote_control_mode`: Remote control mode selection
- `select.solakon_one_force_mode`: Force mode selection
- `number.solakon_one_minimum_state_of_charge`: Minimum battery SoC
- `number.solakon_one_maximum_state_of_charge`: Maximum battery SoC
- `number.solakon_one_minimum_state_of_charge_on_grid`: Minimum SoC when grid-connected
- `number.solakon_one_remote_control_power`: Active power command
- `number.solakon_one_remote_control_reactive_power`: Reactive power command
- `number.solakon_one_remote_control_timeout`: Remote control timeout
- `number.solakon_one_force_mode_power`: Force mode power
- `number.solakon_one_force_mode_duration`: Force mode duration
- `number.solakon_one_grid_export_power_limit`: Grid export power limit

**Future Services (Planned):**
- `solakon_one.set_time_of_use`: Configure TOU schedules

## Entity Names (English / German)

Home Assistant derives the entity ID from the device name and the entity name in the language that was active when the device was added. The table lists both variants for a device named `Solakon ONE`; a second device gets the suffix `_2`. Entity IDs of existing installations do not change when a name changes. Renamed so far: `Ambient temperature` → `BMS temperature`, `Grid export energy` → `AC output energy`, `Grid import energy` → `AC input energy`, and in German `Fernsteuerung Zeitüberschreitung` (sensor) → `Fernsteuerung Restzeit`; older installations keep IDs like `sensor.solakon_one_grid_export_energy`. Regenerate the table with `PYTHONPATH=. uv run python scripts/entity_table.py`.

<!-- entity-table:start -->
| Platform | Key | English entity ID | German entity ID |
|---|---|---|---|
| binary_sensor | `battery_charging` | `binary_sensor.solakon_one_charging` | `binary_sensor.solakon_one_ladestatus` |
| binary_sensor | `grid_status` | `binary_sensor.solakon_one_grid` | `binary_sensor.solakon_one_netz` |
| number | `battery_max_charge_current` | `number.solakon_one_maximum_charge_current` | `number.solakon_one_maximaler_ladestrom` |
| number | `battery_max_discharge_current` | `number.solakon_one_maximum_discharge_current` | `number.solakon_one_maximaler_entladestrom` |
| number | `grid_export_power_limit` | `number.solakon_one_grid_export_power_limit` | `number.solakon_one_netz_ausgangsleistungsgrenze` |
| number | `maximum_soc` | `number.solakon_one_maximum_state_of_charge` | `number.solakon_one_maximaler_ladestand` |
| number | `minimum_soc` | `number.solakon_one_minimum_state_of_charge` | `number.solakon_one_minimaler_ladestand` |
| number | `minimum_soc_ongrid` | `number.solakon_one_minimum_state_of_charge_on_grid` | `number.solakon_one_minimaler_ladestand_netzbetrieb` |
| number | `remote_active_power` | `number.solakon_one_remote_control_power` | `number.solakon_one_fernsteuerung_leistung` |
| number | `remote_reactive_power` | `number.solakon_one_remote_control_reactive_power` | `number.solakon_one_fernsteuerung_blindleistung` |
| number | `remote_timeout_set` | `number.solakon_one_remote_control_timeout` | `number.solakon_one_fernsteuerung_zeituberschreitung` |
| select | `eps_output` | `select.solakon_one_output` | `select.solakon_one_steckdose` |
| sensor | `active_power` | `sensor.solakon_one_active_power` | `sensor.solakon_one_leistung` |
| sensor | `battery1_current` | `sensor.solakon_one_battery_current` | `sensor.solakon_one_batterie_strom` |
| sensor | `battery1_voltage` | `sensor.solakon_one_battery_voltage` | `sensor.solakon_one_batterie_spannung` |
| sensor | `battery_power` | `sensor.solakon_one_battery_power` | `sensor.solakon_one_batterie_leistung` |
| sensor | `battery_soc` | `sensor.solakon_one_battery_state_of_charge` | `sensor.solakon_one_batterie_ladestand` |
| sensor | `battery_total_charge_energy` | `sensor.solakon_one_battery_charge_energy` | `sensor.solakon_one_batterie_ladeenergie` |
| sensor | `battery_total_discharge_energy` | `sensor.solakon_one_battery_discharge_energy` | `sensor.solakon_one_batterie_entladeenergie` |
| sensor | `bms1_ambient_temp` | `sensor.solakon_one_bms_temperature` | `sensor.solakon_one_bms_temperatur` |
| sensor | `bms1_design_energy` | `sensor.solakon_one_battery_capacity` | `sensor.solakon_one_batteriekapazitat` |
| sensor | `bms1_max_cell_voltage` | `sensor.solakon_one_battery_max_cell_voltage` | `sensor.solakon_one_batterie_max_zellspannung` |
| sensor | `bms1_max_temp` | `sensor.solakon_one_battery_max_temperature` | `sensor.solakon_one_batterie_max_temperatur` |
| sensor | `bms1_min_cell_voltage` | `sensor.solakon_one_battery_min_cell_voltage` | `sensor.solakon_one_batterie_min_zellspannung` |
| sensor | `bms1_min_temp` | `sensor.solakon_one_battery_min_temperature` | `sensor.solakon_one_batterie_min_temperatur` |
| sensor | `bms1_soh` | `sensor.solakon_one_battery_state_of_health` | `sensor.solakon_one_batterie_gesundheitszustand` |
| sensor | `bms1_version` | `sensor.solakon_one_bms_version` | `sensor.solakon_one_bms_version` |
| sensor | `cumulative_generation` | `sensor.solakon_one_total_energy` | `sensor.solakon_one_energie` |
| sensor | `daily_generation` | `sensor.solakon_one_daily_energy` | `sensor.solakon_one_tagliche_energie` |
| sensor | `eps_current` | `sensor.solakon_one_eps_current` | `sensor.solakon_one_steckdose_strom` |
| sensor | `eps_power` | `sensor.solakon_one_eps_power` | `sensor.solakon_one_steckdose_leistung` |
| sensor | `eps_voltage` | `sensor.solakon_one_eps_voltage` | `sensor.solakon_one_steckdose_spannung` |
| sensor | `grid_frequency` | `sensor.solakon_one_grid_frequency` | `sensor.solakon_one_netzfrequenz` |
| sensor | `grid_r_voltage` | `sensor.solakon_one_grid_voltage` | `sensor.solakon_one_netzspannung` |
| sensor | `grid_standard_code` | `sensor.solakon_one_grid_standard` | `sensor.solakon_one_netzstandard` |
| sensor | `grid_total_export_energy` | `sensor.solakon_one_ac_output_energy` | `sensor.solakon_one_ac_ausgangsenergie` |
| sensor | `grid_total_import_energy` | `sensor.solakon_one_ac_input_energy` | `sensor.solakon_one_ac_eingangsenergie` |
| sensor | `internal_temp` | `sensor.solakon_one_inverter_temperature` | `sensor.solakon_one_wechselrichter_temperatur` |
| sensor | `inverter_r_frequency` | `sensor.solakon_one_inverter_frequency` | `sensor.solakon_one_wechselrichter_frequenz` |
| sensor | `inverter_version` | `sensor.solakon_one_inverter_version` | `sensor.solakon_one_wechselrichter_version` |
| sensor | `max_active_power` | `sensor.solakon_one_grid_maximum_export_power_limit` | `sensor.solakon_one_netz_maximale_ausgangsleistungsgrenze` |
| sensor | `network_status` | `sensor.solakon_one_network` | `sensor.solakon_one_netzwerk` |
| sensor | `operating_mode` | `sensor.solakon_one_operating_mode` | `sensor.solakon_one_betriebsart` |
| sensor | `power_factor` | `sensor.solakon_one_power_factor` | `sensor.solakon_one_leistungsfaktor` |
| sensor | `pv1_current` | `sensor.solakon_one_string_1_current` | `sensor.solakon_one_string_1_strom` |
| sensor | `pv1_power` | `sensor.solakon_one_string_1_power` | `sensor.solakon_one_string_1_leistung` |
| sensor | `pv1_voltage` | `sensor.solakon_one_string_1_voltage` | `sensor.solakon_one_string_1_spannung` |
| sensor | `pv2_current` | `sensor.solakon_one_string_2_current` | `sensor.solakon_one_string_2_strom` |
| sensor | `pv2_power` | `sensor.solakon_one_string_2_power` | `sensor.solakon_one_string_2_leistung` |
| sensor | `pv2_voltage` | `sensor.solakon_one_string_2_voltage` | `sensor.solakon_one_string_2_spannung` |
| sensor | `pv3_current` | `sensor.solakon_one_string_3_current` | `sensor.solakon_one_string_3_strom` |
| sensor | `pv3_power` | `sensor.solakon_one_string_3_power` | `sensor.solakon_one_string_3_leistung` |
| sensor | `pv3_voltage` | `sensor.solakon_one_string_3_voltage` | `sensor.solakon_one_string_3_spannung` |
| sensor | `pv4_current` | `sensor.solakon_one_string_4_current` | `sensor.solakon_one_string_4_strom` |
| sensor | `pv4_power` | `sensor.solakon_one_string_4_power` | `sensor.solakon_one_string_4_leistung` |
| sensor | `pv4_voltage` | `sensor.solakon_one_string_4_voltage` | `sensor.solakon_one_string_4_spannung` |
| sensor | `pv_total_energy` | `sensor.solakon_one_pv_energy` | `sensor.solakon_one_pv_energie` |
| sensor | `pv_version` | `sensor.solakon_one_pv_version` | `sensor.solakon_one_pv_version` |
| sensor | `reactive_power` | `sensor.solakon_one_reactive_power` | `sensor.solakon_one_blindleistung` |
| sensor | `remote_control` | `sensor.solakon_one_remote_control` | `sensor.solakon_one_fernsteuerung` |
| sensor | `remote_timeout_countdown` | `sensor.solakon_one_remote_timeout_countdown` | `sensor.solakon_one_fernsteuerung_restzeit` |
| sensor | `total_pv_power` | `sensor.solakon_one_pv_power` | `sensor.solakon_one_pv_leistung` |
<!-- entity-table:end -->

## Support

For issues or questions:
- Report issues on [GitHub](https://github.com/solakon-de/solakon-one-homeassistant/issues)

## License

This integration is provided as-is under the MIT License.
