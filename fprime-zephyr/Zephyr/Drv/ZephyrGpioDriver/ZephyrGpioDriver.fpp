module Drv {
    @ Zephyr GPIO Driver
    passive component ZephyrGpioDriver {

        guarded input port gpioWrite: Drv.ZephyrGpioWrite
        
        guarded input port gpioRead: Drv.ZephyrGpioRead

    }
}