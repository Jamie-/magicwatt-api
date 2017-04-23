# IoT Power Monitoring #

IoT Energy Meter REST API - Sits in my mains power entrance box.

## What actually is it? ##
This is a little project of mine stemming from and using some code from [OpenEnergyMonitor](https://openenergymonitor.org/).
It uses a non-invasive AC current sensor which clamps around the live wire incoming to your house from the national grid.
This current sensor produces a varying current itself depending on how much electricty is drawn through that live cable it's clamped around.

What I've done is taken an [Adafruit Trinket](https://learn.adafruit.com/introducing-trinket/introduction) and attached it to a Raspberry Pi Zero using I2C.
Then I've created a REST API (using flask) in Python which pulls data from the sensor over I2C and produces a nice JSON output which can be used by other programs.
At some point in the future I plan to write something to poll the API every minute or so and record the data to a database so it can be beautifully graphed.

## Installation ##
### Simple ###
1. Write a copy of [Raspbian Lite](https://downloads.raspberrypi.org/raspbian_lite_latest "Download Raspbian Lite") to a micro SD card.
2. Pop the SD card in a Raspberry Pi Zero and power it on.
3. Install git - `sudo apt-get update; sudo apt-get install git`.
4. Clone this repository - `git clone https://github.com/Jamie-/magicwatt-api.git`
5. Run the install script - `./magicwatt-api/setup.sh`
6. Power off your Pi and wire up the circuitry described below.
7. Power on your Pi, wait a minute or so for it to boot.
8. Head over to `magicwatt:5000` in a browser and all going well you should get a list of URLs.

### Advanced ###
1. Clone this git repo.
2. Run `setup.sh` to configure your Pi.
3. Power off and wire up the circuitry described below.
4. Power on.
5. Drink coffee and visit `magicwatt:5000`.

## Circuitry ##
WIP - See OpenEnergyMonitor documentation for now and use the Trinket pin #4 (which is analog 2) for the Arduino pin mentioned in their guides.

## Adafruit Trinket ##
The Trinket will need to be programmed prior to use with code from my other repository for this project [here](https://github.com/Jamie-/magicwatt-trinket/).

This project works best with a 3.3V Trinket but a 5V Trinket will be okay - you'll just need a logic level shifter between it and the Raspberry Pi.
You can make one really easily with a pair of 10kΩ resistors and a 2N7000 MOSFET - have a look [here](http://www.hobbytronics.co.uk/mosfet-voltage-level-converter) for a diagram.
