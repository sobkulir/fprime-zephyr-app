module Zephyr {

  @ An interrupt based driver for Arduino rate groups.
  passive component ZephyrRateDriver {

    @ The cycle outputs. Meant to be connected to rate group driver
    output port CycleOut: [1] Svc.Cycle

  }

}
