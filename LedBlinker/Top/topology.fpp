module LedBlinker {

  # ----------------------------------------------------------------------
  # Symbolic constants for port numbers
  # ----------------------------------------------------------------------

    enum Ports_RateGroups {
      rateGroup1
      rateGroup2
      rateGroup3
    }

    enum Ports_StaticMemory {
      downlink
      uplink
    }

  topology LedBlinker {

    # ----------------------------------------------------------------------
    # Instances used in the topology
    # ----------------------------------------------------------------------

    instance tlmSend
    instance cmdDisp
    instance cmdSeq
    instance commUartDriver
    instance downlink
    instance eventLogger
    instance zephyrRateDriver
    instance rateGroupDriver
    instance rateGroup1
    instance rateGroup2
    instance rateGroup3
    instance staticMemory
    instance fileUplink
    instance fileUplinkBufferManager
    instance fileDownlink
    instance fileManager
    instance textLogger
    instance prmDb
    instance uplink
    instance zephyrTime
    instance ledGpioDriver
    instance led
    # ----------------------------------------------------------------------
    # Pattern graph specifiers
    # ----------------------------------------------------------------------

    command connections instance cmdDisp

    event connections instance eventLogger

    param connections instance prmDb

    telemetry connections instance tlmSend

    text event connections instance textLogger

    time connections instance zephyrTime

    # health connections instance $health

    # ----------------------------------------------------------------------
    # Direct graph specifiers
    # ----------------------------------------------------------------------

    connections Downlink {
      tlmSend.PktSend -> downlink.comIn
      eventLogger.PktSend -> downlink.comIn
      fileDownlink.bufferSendOut -> downlink.bufferIn

      downlink.framedAllocate -> staticMemory.bufferAllocate[Ports_StaticMemory.downlink]
      downlink.framedOut -> commUartDriver.send
      downlink.bufferDeallocate -> fileDownlink.bufferReturn

      commUartDriver.deallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.downlink]

    }

    connections FaultProtection {
      # eventLogger.FatalAnnounce -> fatalHandler.FatalReceive
    }

    connections RateGroups {
      zephyrRateDriver.CycleOut -> rateGroupDriver.CycleIn
      
      # Rate group 1
      rateGroupDriver.CycleOut[Ports_RateGroups.rateGroup1] -> rateGroup1.CycleIn
      rateGroup1.RateGroupMemberOut[0] -> commUartDriver.schedIn

      # Rate group 2
      rateGroupDriver.CycleOut[Ports_RateGroups.rateGroup2] -> rateGroup2.CycleIn
      rateGroup2.RateGroupMemberOut[1] -> cmdSeq.schedIn

       # Rate group 3
      rateGroupDriver.CycleOut[Ports_RateGroups.rateGroup3] -> rateGroup3.CycleIn
      rateGroup3.RateGroupMemberOut[0] -> tlmSend.Run
      rateGroup3.RateGroupMemberOut[1] -> fileDownlink.Run
      rateGroup3.RateGroupMemberOut[2] -> fileUplinkBufferManager.schedIn
      rateGroup3.RateGroupMemberOut[3] -> commUartDriver.schedInTlm
    }

    connections Sequencer {
      cmdSeq.comCmdOut -> cmdDisp.seqCmdBuff
      cmdDisp.seqCmdStatus -> cmdSeq.cmdResponseIn
    }

    connections Uplink {

      commUartDriver.allocate -> staticMemory.bufferAllocate[Ports_StaticMemory.uplink]
      commUartDriver.$recv -> uplink.framedIn

      uplink.framedDeallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.uplink]

      uplink.comOut -> cmdDisp.seqCmdBuff
      cmdDisp.seqCmdStatus -> uplink.cmdResponseIn

      uplink.bufferAllocate -> fileUplinkBufferManager.bufferGetCallee
      uplink.bufferOut -> fileUplink.bufferSendIn
      uplink.bufferDeallocate -> fileUplinkBufferManager.bufferSendIn
      fileUplink.bufferSendOut -> fileUplinkBufferManager.bufferSendIn
    }

    connections LedBlinker {
      # Add here connections to user-defined components
      led.gpioSet -> ledGpioDriver.gpioWrite
    }

  }

}
