module Drv {

  port ZephyrGpioWrite(
                  state: Fw.Logic
                ) -> Drv.ZephyrGpioStatus

}

module Drv {

  port ZephyrGpioRead(
                 ref state: Fw.Logic
               ) -> Drv.ZephyrGpioStatus

}

module Drv {

  enum ZephyrGpioStatus {
    GPIO_OK = 0 @< Transaction okay
    GPIO_IO_ERR = 1 @< I/O error when accessing an external GPIO chip
    GPIO_OTHER_ERR = 2 @< Other errors that don't fit
  }

}

