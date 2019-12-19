# RATP Metro Schedules Display (next train indicator)

A set of python scripts to display near real-time RATP Metro station departure data on SSD1322-based 256x64 SPI OLED screens. Uses the open-source [Unofficial RATP API](https://github.com/pgrimaud/horaires-ratp-api). This project has been developed and simplified based on the work of [others](#credits).

   * [Installation](#installation)
   * [Configuration](#configuration)
   * [Hardware](#hardware)
   * [Credits](#credits)

## Installation

Just clone this repository, then copy it to a RaspberryPi using SSH or any other means. Tested with RaspberryPi Zero W.

## Configuration

Placing yourself in the root of the repository:

1. `cp config.sample.json config.json`
2. Fill the `config.json` file with the following variables:

| Key                              | Example Value
|----------------------------------|----------
|`departureStation`  | `La Defense` ([examples](https://github.com/pgrimaud/horaires-ratp-api#exemples-de-requ%C3%AAtes)) display name of the departure station
|`departureStationSlug`  | `la+defense` ([examples](https://github.com/pgrimaud/horaires-ratp-api#exemples-de-requ%C3%AAtes)) url slug for API call to unofficial API
|`refreshTime` | `120` seconds between data refresh
|`color` | `yellow` [optional] if you find a display with color and want to customize...

## Hardware

This project (without modification) requires the use of a SSD1322-based 256x64 SPI display, an OLED in yellow for the authentic look. I have used a [display from AliExpress](https://www.aliexpress.com/item/32988174566.html) successfully.

The connections for the display to the Raspberry Pi GPIO header are as follows, but **it would be a good idea to check the connections with the datasheet of your particilar display before powering on** as there's no guarantee yours will match the pinout of mine.

| Display | Connection | Raspberry Pi
|---|---|---
| 1 | Ground | 6 (Ground) |
| 2 | V+ (3.3V) | 1 (3v3 Power) |
| 4 | `D0/SCLK` | 23 (`BCM11 SCLK`) |
| 5 | `D1/SDIN` | 19 (`BCM10 MOSI`) |
| 14 | `DC` (data/command select) | 18 (`BCM24`) |
| 15 | `RST` (reset) | 22 (`BCM25`) |
| 16 | `CS` (chip select) | 24 (`BCM8 CE0`)

![](assets/pi-display-connections_bb.png)

**NB: In order to use the display with the 4-wire SPI protocol, you need to desolder the `R6` shunt resistor and solder it on the `R5` pads as indicated on the data table on the back of the OLED screen PCB**

## Case

There are .stl 3D models for a case available in the assets directory.

## Credits

A big thanks to [Chris Hutchinson](https://github.com/chrishutchinson/) who originally started this project and inspired me to develop it further. [Blake](https://github.com/ghostseven) made some further improvements and this project was forked from [there](https://github.com/ghostseven/UK-Train-Departure-Display).

The fonts used were painstakingly put together by `DanielHartUK` and can be found on GitHub at https://github.com/DanielHartUK/Dot-Matrix-Typeface - A huge thanks for making that resource available!
