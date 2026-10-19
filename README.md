# Tapo P115 TPAP v2 — Home Assistant (HACS)

**Experimental integration**, maintained for Tapo P115 plugs using TPAP v2.
This is a separate Home Assistant integration named `tapo_tpap`, designed
to coexist with the built-in TP-Link Smart Home integration (`tplink`).

## Tested devices (19 October 2026)

| Test device | Hardware | Firmware | TPAP v2 read |
|---|---|---|---|
| P115 A | P115 EU 1.0 | 1.4.0 | PASS |
| P115 B | P115 EU 1.0 | 1.4.8 | PASS |

**Scope of testing:** read-only `kasa state` on Windows 11 using the
experimental [TPAP PR #1592](https://github.com/python-kasa/python-kasa/pull/1592).
The integration's power, voltage, current and energy sensors have subsequently
been observed working in Home Assistant. Relay switching has **not been tested
on live hardware**.

## Features

- Adds each P115 using an IP address and local authentication with the
  owner's Tapo account credentials (no direct Tapo cloud API calls).
- Entity per device: power W, voltage V, current A, energy today kWh,
  energy this month kWh, relay switch (disabled by default).
- Refresh interval: 15 seconds.
- Supports both known firmware versions using a private TPAP transport.
- No MQTT, separate LXC, or constantly running Windows computer required.

**IMPORTANT:** The relay switch, when enabled, cuts the plug's AC output.
For equipment such as air conditioners, use the appliance's own controls
rather than cutting its mains supply during operation.

## Dependency isolation

Home Assistant's official `tplink` integration imports the shared
`kasa` package. Overriding that shared package with an experimental
version is unsafe for existing HS100/HS110 devices.

This integration instead **vendors the upstream TPAP implementation under**
`custom_components.tapo_tpap._vendor.kasa`; imports inside the vendored
library are rewritten to that private namespace. The upstream implementation
is pinned to commit
`e7084472972f08f2e2235b342f3964aedbfaeb3b`, with original
GPL-3.0-or-later license notices retained.

The vendoring workflow commits the private library into this repository
so a normal HACS checkout includes the necessary code. Installing from
source **before** the vendored directory has been generated will fail.

## HACS installation (after successful verification)

> **Current state:** experimental beta. The isolated build has passed and basic
> P115 telemetry has been observed in Home Assistant. Relay write behavior
> remains unverified; leave relay switches disabled until individually tested.

1. In Home Assistant, open **HACS → ⋮ → Custom repositories**.
2. Enter `https://github.com/razvanu/python-kasa-tapo` and select **Integration**.
3. Download **Tapo TPAP v2 (P115)**, then restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration**.
5. Search for **Tapo TPAP v2 (Experimental)**.
6. Add your first P115 using the IP address shown in its Tapo app and your Tapo account credentials.
7. Repeat with the IP of your second P115; each plug gets a separate device.
8. Inspect sensors and device diagnostics before enabling relay switch entities.

The account password is kept in HA config entry storage, **never in GitHub**.
Use IP reservations in your router for both devices.

## Development and verification

- `custom_components/tapo_tpap/`: integration code.
- `tools/build_vendor_kasa.py`: isolated vendor source rewriter.
- `.github/workflows/validate-and-vendor.yml`: automated vendoring,
  syntax compile, private-import smoke test, preview ZIP.
- The exact TPAP upstream implementation is not yet merged into official
  `python-kasa`. When officially supported in Home Assistant, migrating to
  the built-in integration may be preferable.

### Known limitations

- Basic HA sensor entity values have been observed. Relay switching is
  unverified and should be tested with a non-critical load first.
- Device configuration currently checks IP syntax but does not confirm
  credentials until the first poll. Incorrect credentials cause retry.
- The sensor values for daily/monthly energy reset over time; they must not
  be configured as `total_increasing` energy statistics without reset-safe
  handling.
- Automatic firmware-upgrade control and advanced Tapo device settings are
  out of scope.

## Credits and license

The isolated dependency is adapted from
[python-kasa](https://github.com/python-kasa/python-kasa) and TPAP
implementation by [ZeliardM](https://github.com/ZeliardM/python-kasa).
The vendored source preserves its GPL-3.0-or-later license; see
`custom_components/tapo_tpap/_vendor/kasa/LICENSE`.
This repository's existing MIT license applies to original integration
code where separately applicable; redistribution of the combined package
must also comply with the vendored GPL terms.

**Project status:** early beta. Read-only Home Assistant sensor functionality observed; relay writes unverified.
