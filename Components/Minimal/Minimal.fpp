module Components {
    @ Example Component for F Prime FSW framework.
    passive component Minimal {

        @ A count of the number of greetings issued
        telemetry GreetingCount: U32

        sync input port schedIn: Svc.Sched

        @ LED command
        sync command DUMMY_CMD \
            opcode 0

        @ Port for sending telemetry channels to downlink
        telemetry port tlmOut

        @ A port for getting the time
        time get port Time

        @ Command receive port
        command recv port CmdDisp

        @ Command registration port
        command reg port CmdReg

        @ Command response port
        command resp port CmdStatus
    }
}