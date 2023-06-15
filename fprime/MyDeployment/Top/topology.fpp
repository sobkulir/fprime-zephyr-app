module MyDeployment {

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

  topology MyDeployment {

    # ----------------------------------------------------------------------
    # Instances used in the topology
    # ----------------------------------------------------------------------

    instance tlmSend
    instance cmdDisp
    instance comm
    instance downlink
    instance eventLogger
    instance rateGroup1
    instance rateGroup2
    instance rateGroupDriver
    instance staticMemory
    instance textLogger
    instance uplink
    instance helloWorld
    instance zephyrTimer

    # ----------------------------------------------------------------------
    # Pattern graph specifiers
    # ----------------------------------------------------------------------

    command connections instance cmdDisp

    event connections instance eventLogger

    # param connections instance prmDb

    telemetry connections instance tlmSend

    text event connections instance textLogger

    # time connections instance linuxTime

    # health connections instance $health

    # ----------------------------------------------------------------------
    # Direct graph specifiers
    # ----------------------------------------------------------------------

    connections Downlink {
      tlmSend.PktSend -> downlink.comIn
      eventLogger.PktSend -> downlink.comIn
      # # fileDownlink.bufferSendOut -> downlink.bufferIn

      downlink.framedAllocate -> staticMemory.bufferAllocate[Ports_StaticMemory.downlink]
      downlink.framedOut -> comm.send
      # # downlink.bufferDeallocate -> fileDownlink.bufferReturn

      comm.deallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.downlink]

    }

    connections FaultProtection {
      # eventLogger.FatalAnnounce -> fatalHandler.FatalReceive
    }

    connections RateGroups {
      zephyrTimer.CycleOut -> rateGroupDriver.CycleIn
      
      # Rate group 1
      rateGroupDriver.CycleOut[Ports_RateGroups.rateGroup1] -> rateGroup1.CycleIn
      rateGroup1.RateGroupMemberOut[0] -> tlmSend.Run
      rateGroup1.RateGroupMemberOut[1] -> uplink.schedIn

      # Rate group 2
      rateGroupDriver.CycleOut[Ports_RateGroups.rateGroup2] -> rateGroup2.CycleIn
      rateGroup2.RateGroupMemberOut[0] -> helloWorld.schedIn
    }

    connections Uplink {

      comm.allocate -> staticMemory.bufferAllocate[Ports_StaticMemory.uplink]
      comm.$recv -> uplink.framedIn

      uplink.framedDeallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.uplink]
      uplink.framedPoll -> comm.poll

      uplink.comOut -> cmdDisp.seqCmdBuff
      cmdDisp.seqCmdStatus -> uplink.cmdResponseIn

      uplink.bufferAllocate -> staticMemory.bufferAllocate[Ports_StaticMemory.uplinkFrame]
      uplink.bufferDeallocate -> staticMemory.bufferDeallocate[Ports_StaticMemory.uplinkFrame]
    }

    connections MyDeployment {
      # Add here connections to user-defined components
      
    }

  }

}
