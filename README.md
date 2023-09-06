# Port of F' onto Zephyr

This is a minimal application running F' (v3.3.2) on Zephyr (v3.3.0). The example deployment is under `fprime/LedBlinker` and uses `nucleo_h723zg` board.

## Requirements

The development is dockerized, but the device fallthrough into the docker container was only tested on
Ubuntu. Our versions:
* Ubuntu 22.04 LTS
* Docker 20.10.23

## Initialization

The first step is to initialize the workspace folder (`zephyr-workspace`) where
the ``fprime-zephyr-app`` and all Zephyr modules will be cloned. Run the following
command:

```shell
# Setup and clone
$ mkdir zephyr-workspace && cd zephyr-workspace
$ git clone git@github.com:sobkulir/fprime-zephyr-app.git

# Run the image from the convenience script. It has reasonable defaults.
$ cd fprime-zephyr-app
$ ./run_dev.py
```

Inside the docker container:
```shell
$ west init -l .
$ west update
```

## Building and running
TODO: This section needs to be reworked.

If you don't have a board, build and run for qemu:
```shell
$ rm -rf build && west build -b qemu_cortex_m3 fprime/MyDeployment/
$ west build -t run
```

If you have a board, e.g., `nucleo_h723zg`:
```shell
$ rm -rf build && west build -b nucleo_h723zg fprime/MyDeployment/
$ sudo west flash
```

Building the F' way:
```shell
$ cd LedBlinker && fprime-util generate -DBOARD=nucleo_h723zg -DCMAKE_GENERATOR=Ninja
$ fprime-util build -j16
```

### Ground Station
Running `fprime-gds` over UART:
```shell
$ sudo fprime-gds --uart-device /dev/ttyUSB0 --uart-baud 115200 --dictionary build/MyDeployment/Top/MyDeploymentTopologyAppDictionary.xml -n --comm-adapter uart

```


## Maintanence

### Bumping F' version
To bump F' version, it requires some GIT magic and you'll likely run into some issues :)) You need your fork of fprime (here named `origin`) and another remote which is the original fprime repository (here `base`).

Checkout the new version, branch, and cherry-pick the commit that adds the static stack support:
```shell
# (one time setup) Add nasa/fprime repo to fetch from
$ cd fprime && git remote add base git@github.com:nasa/fprime.git
# Fetch and cherry pick (in fprime/)
$ git fetch base && git checkout <tag> && git checkout -b zephyr_port_<tag>
$ git cherry-pick dbfb5782 && git push
```

Afterwards, update the Dockerfile to have the corect version of the tools and follow next section to rebuild it:
```shell
# In docker/Dockerfile
pip3 install -r https://raw.githubusercontent.com/nasa/fprime/<tag>/requirements.txt
```

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
$ west build -b nucleo_h723zg samples/subsys/shell/fs/ -- -DDTC_OVERLAY_FILE=/zephyr-workspace/fprime-zephyr-app/fprime/MyDeployment/boards/nucleo_h723zg.overlay
```
