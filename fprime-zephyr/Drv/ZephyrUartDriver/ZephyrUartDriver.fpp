module Drv {

  passive component ZephyrUartDriver {

    @ Polling for receiving data
    sync input port schedIn: Svc.Sched

    @ Polling for sending telemetry
    sync input port schedInTlm: Svc.Sched

    @ Indicates the driver has connected to the UART device
    output port ready: Drv.ByteStreamReady

    @Allocate new buffer
    output port allocate: Fw.BufferGet

    @return the allocated buffer
    output port deallocate: Fw.BufferSend

    @ Takes data to transmit out the UART device
    guarded input port send: Drv.ByteStreamSend

    @ Takes data to transmit out the UART device
    output port $recv: Drv.ByteStreamRecv


    @ Telemetry channel counting total number of LED transitions
    telemetry BufferOverruns: U32 update on change \
      high {
        red 1
      }

    ###############################################################################
    # Standard AC Ports: Required for Channels, Events, Commands, and Parameters  #
    ###############################################################################
    @ Port for requesting the current time
    time get port timeCaller

    @ Port for sending telemetry channels to downlink
    telemetry port tlmOut
  }
}
