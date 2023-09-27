module Components {
    @ Led driver for Nucleo stm32h723 board
    passive component LedDriver {

        ##############################################################################
        #### Uncomment the following examples to start customizing your component ####
        ##############################################################################

        @ Toggles the LED to the opposite state
        sync command LED_TOGGLE

        @ Toggles the LED to on state
        sync command LED_ON

        @ Toggles the LED to off state
        sync command LED_OFF

        @ Telemetry channel counting total number of LED transitions
        telemetry TransitionCount: U32

        @ Port sending calls to the GPIO driver
        output port gpioSet: Drv.ZephyrGpioWrite

        @ Event logged when the LED turns on or off
        event LedState(on_off: bool) \
            severity activity low \
            format "LED is {}"

        @ Failed to set the LED state
        event LedError(desiredState: bool, currentState: bool, error: I32) \
            severity warning high \
            format "LED failed to change state to {} from {} with error {}" \
            throttle 5

        # @ Default state of the LED (on/off)
        # param defaultState: bool default false

        ###############################################################################
        # Standard AC Ports: Required for Channels, Events, Commands, and Parameters  #
        ###############################################################################
        @ Port for requesting the current time
        time get port timeCaller

        @ Port for sending command registrations
        command reg port cmdRegOut

        @ Port for receiving commands
        command recv port cmdIn

        @ Port for sending command responses
        command resp port cmdResponseOut

        @ Port for sending textual representation of events
        text event port logTextOut

        @ Port for sending events to downlink
        event port logOut

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        # @ A port for getting parameter values
        # param get port ParamGet

        # @Port to set the value of a parameter
        # param set port prmSetOut
    }
}