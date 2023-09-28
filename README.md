# Port of F' onto Zephyr

This is a minimal application running F' (v3.3.2) on Zephyr (v3.3.0). The target device is `nucleo_h723zg`, however there's also a tiny Qemu deployment under `QemuMinimal` which doesn't require a board and can be used as a base for porting onto a custom board.

## Requirements
### Hardware

There are two example deployments for `nucleo_h723zg` board:
1. `LedMinimal` which requires `USART2` to be connected to communicate with "ground" (laptop)
2. `LedBlinker` which allows file uplink/downlink and hence requires [MRAM (MR2XH40)](https://wiki.berkayisik.com/projects/software/zephyr/mram), as found on our expansion board

**Two serials connected to the laptop are needed**
The "main" serial, connected via the USB cable used for flashing the board, is used for debug printing.
And while in theory I could have globbed the "space packets" over this serial, since Nucleo board has pinouts for another serial, I decided to use another one to make the design simpler. Therefore, you'll need a "serial to USB" adapter, for example Marotronics sells them for 1,29 € a piece [ [link](https://www.marotronics.de/RS232-USB-Adapter-IC-PL2303HX-33V-5V-TTL-serial-level-for-Arduino) ]. You'll also need some jump wires. If you can't source this stuff then ping me, I have some extras!

TODO a picture.

Then connect the adapter as follows:
| What | Pin Nucleo |
| --- | --- |
| Serial +5V | CN8 9 |
| Serial GND | CN7 8 (or any other GND) |
| Serial RX | CN9 6 |
| Serial TX | CN9 4 |

*Note 1: In the actual design, this communication will be over CAN. Maximum payload of CAN FD is 64B so packets will have to be fragmented and defragmented. Here, serial is used to work around this for now.*

*Note 2: There is a standard for multiplexing serials over USB called USB CDC-ACM to avoid the extra "serial to USB" hardware, but I couldn't make it work on our board. [ [USB CDC-ACM composite sample](https://docs.zephyrproject.org/latest/samples/subsys/usb/cdc_acm_composite/README.html), [Issue #57499](https://github.com/zephyrproject-rtos/zephyr/issues/57499), [Issue #59828](https://github.com/zephyrproject-rtos/zephyr/issues/59828) ]*

### Software

The development environment is dockerized, i.e., Zephyr and F Prime are installed there. The device fallthrough into the docker container was only tested on Ubuntu. The following versions were used:
* Ubuntu 22.04 LTS
* Docker 20.10.23

## Initialization

The first step is to initialize the workspace folder (`zephyr-workspace`) where
the ``fprime-zephyr-app`` and all Zephyr modules will be cloned. Run the following:

```shell
# Setup and clone
$ mkdir zephyr-workspace && cd zephyr-workspace
$ git clone git@github.com:sobkulir/fprime-zephyr-app.git

# Run a Docker image from the convenience script. It has reasonable defaults.
$ cd fprime-zephyr-app
$ ./run_dev.py
```

Inside the docker container:
```shell
$ west init -l .
$ west update
```

## Building and flashing
If you don't have a `nucleo_h723zg` board, you can run the Qemu example, for that see README in the `QemuMinimal`.

Otherwise, both `LedMinimal` and `LedBlinker` can be build and flashed as follows (example for `LedMinimal`):
```shell
$ cd LedMinimal && fprime-util generate -DBOARD=nucleo_h723zg -DCMAKE_GENERATOR=Ninja
$ sudo west flash --build-dir build-fprime-automatic-zephyr
```

*Note: Ninja is used instead of Makefile (default for F Prime), because, at least on the tested system, it was significantly faster.*

Running `fprime-gds` over UART (maybe you'll need to change the device name):
```shell
$ sudo fprime-gds --uart-device /dev/ttyUSB0 --uart-baud 115200 --dictionary build-artifacts/zephyr/LedMinimal/dict/LedMinimalTopologyAppDictionary.xml -n --comm-adapter uart
```

Now, open `localhost:5000` in the browser and you should be able to control the LED.

To open debug serial e.g. with Minicom:
```shell
$ minicom --device /dev/ttyACM0
```

## Future work
1. Create testing environments. 

## Maintanence

### Updating Dockerfile
After changing the Dockerfile, build it:

```shell
$ cd docker && docker build -t <image_name> .
```

Then to use this image change `run_dev.py` to use the new image name or run `./run_dev.py <image_name>`.

### Helpers

Deleting Autocoder generated files

```shell
$ ls -d fprime/Autocoders/Python/src/fprime_ac/generators/templates/**/**.py | sed '/.*__init__.py/d' | xargs -I{} rm -r "{}"
```

Build fs shell

```shell
$ west build -b nucleo_h723zg samples/subsys/shell/fs/ -- -DDTC_OVERLAY_FILE=/zephyr-workspace/fprime-zephyr-app/LedBlinker/boards/nucleo_h723zg.overlay
```
