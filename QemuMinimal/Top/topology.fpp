module QemuMinimal {

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
      uplinkFrame
    }

  topology QemuMinimal {

    # ----------------------------------------------------------------------
    # Instances used in the topology
    # ----------------------------------------------------------------------

    instance tlmSend
    instance cmdDisp
    # instance cmdSeq
    instance commUartDriver
    instance downlink
    instance eventLogger
    instance zephyrRateDriver
    instance rateGroupDriver
    instance rateGroup1
    instance rateGroup2
    instance rateGroup3
    instance staticMemory
    instance textLogger
    instance uplink
    instance zephyrTime
    # ----------------------------------------------------------------------
    # Pattern graph specifiers
    # ----------------------------------------------------------------------

    command connections instance cmdDisp

    event connections instance eventLogger

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

      downlink.framedAllocate -> staticMemory.bufferAllocate[Ports_StaticMemory.downlink]
      downlink.framedOut -> commUartDriver.send

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
      # rateGroup2.RateGroupMemberOut[1] -> cmdSeq.schedIn

       # Rate group 3
      rateGroupDriver.CycleOut[Ports_RateGroups.rateGroup3] -> rateGroup3.CycleIn
      rateGroup3.RateGroupMemberOut[0] -> tlmSend.Run
      rateGroup3.RateGroupMemberOut[1] -> commUartDriver.schedInTlm
    }

    connections Sequencer {
      # cmdSeq.comCmdOut -> cmdDisp.seqCmdBuff
      # cmdDisp.seqCmdStatus -> cmdSeq.cmdResponseIn
    }

    connections Uplink {

      commUartDriver.allocate -> staticMemory.bufferAllocate[Ports_StaticMemory.uplink]
      commUartDriver.$recv -> uplink.framedIn

      uplink.framedDeallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.uplink]

      uplink.comOut -> cmdDisp.seqCmdBuff
      cmdDisp.seqCmdStatus -> uplink.cmdResponseIn

      uplink.bufferAllocate -> staticMemory.bufferAllocate[Ports_StaticMemory.uplinkFrame]
      uplink.bufferDeallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.uplinkFrame]
    }


  }

}
