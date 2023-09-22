module LedBlinker {

  # ----------------------------------------------------------------------
  # Defaults
  # ----------------------------------------------------------------------

  module Default {
    constant QUEUE_SIZE = 10
    constant STACK_SIZE = 22 * 1024
  }

  # ----------------------------------------------------------------------
  # Active component instances
  # ----------------------------------------------------------------------

  # Main thread in Zephyr has priority 0. Lower numbers are higher priority.
  #
  # The definition of active components is so elaborate because we need to
  # pass in the static stack (other OSes typically allocate the stack on
  # heap).
  # Hack: Pointer to the stack is passed through the cpuAffinity, since
  #       we don't need the cpuAffinity as we only have single core.
instance cmdSeq: Svc.CmdSequencer base id 0x0600 \
  queue size Default.QUEUE_SIZE \
  stack size Default.STACK_SIZE \
  priority 4 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::cmdSeq);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  cmdSeq.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::cmdSeq),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::cmdSeq::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::cmdSeq::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::cmdSeq)
  );
  """
}

  instance cmdDisp: Svc.CommandDispatcher base id 0x0500 \
    queue size 20 \
    stack size Default.STACK_SIZE \
    priority 4 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::cmdDisp);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  cmdDisp.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::cmdDisp),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::cmdDisp::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::cmdDisp::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::cmdDisp)
  );
  """
}

  instance eventLogger: Svc.ActiveLogger base id 0x0B00 \
    queue size Default.QUEUE_SIZE \
    stack size Default.STACK_SIZE \
    priority 4 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::eventLogger);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  eventLogger.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::eventLogger),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::eventLogger::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::eventLogger::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::eventLogger)
  );
  """
}

  instance tlmSend: Svc.TlmChan base id 0x0C00 \
    queue size Default.QUEUE_SIZE \
    stack size Default.STACK_SIZE \
    priority 4 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::tlmSend);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  tlmSend.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::tlmSend),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::tlmSend::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::tlmSend::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::tlmSend)
  );
  """
}

  instance prmDb: Svc.PrmDb base id 0x0D00 \
    queue size Default.QUEUE_SIZE \
    stack size Default.STACK_SIZE \
    priority 10 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::prmDb);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  prmDb.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::prmDb),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::prmDb::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::prmDb::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::prmDb)
  );
  """
}

  instance fileUplink: Svc.FileUplink base id 0x0900 \
    queue size Default.QUEUE_SIZE \
    stack size Default.STACK_SIZE \
    priority 10 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::fileUplink);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  fileUplink.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::fileUplink),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::fileUplink::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::fileUplink::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::fileUplink)
  );
  """
}

  instance fileDownlink: Svc.FileDownlink base id 0x0700 \
    queue size Default.QUEUE_SIZE \
    stack size Default.STACK_SIZE \
    priority 10 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::fileDownlink);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  fileDownlink.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::fileDownlink),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::fileDownlink::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::fileDownlink::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::fileDownlink)
  );
  """
}

  instance fileManager: Svc.FileManager base id 0x0800 \
    queue size Default.QUEUE_SIZE \
    stack size 40  * 1024 \
    priority 10 \
{
  phase Fpp.ToCpp.Phases.configObjects """
  K_THREAD_STACK_DEFINE(stack, StackSizes::fileManager);
  """

  phase Fpp.ToCpp.Phases.startTasks """
  fileManager.start(
    static_cast<NATIVE_UINT_TYPE>(Priorities::fileManager),
    static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(ConfigObjects::fileManager::stack)),
    /*cpuAffinity=*/reinterpret_cast<NATIVE_UINT_TYPE>(ConfigObjects::fileManager::stack), // This is a hack.
    static_cast<NATIVE_UINT_TYPE>(TaskIds::fileManager)
  );
  """
}

  # ----------------------------------------------------------------------
  # Queued component instances
  # ----------------------------------------------------------------------

  # instance $health: Svc.Health base id 0x2000 \
  #   queue size 25

  # ----------------------------------------------------------------------
  # Passive component instances
  # ----------------------------------------------------------------------

  @ Communications driver.
  instance commUartDriver: Zephyr.ZephyrUartDriver base id 0x4000

  instance downlink: Svc.Framer base id 0x4100

  instance rateGroup1: Svc.PassiveRateGroup base id 0x1000

  instance rateGroup2: Svc.PassiveRateGroup base id 0x1200

  instance rateGroup3: Svc.PassiveRateGroup base id 0x1300

  instance zephyrRateDriver: Zephyr.ZephyrRateDriver base id 0x1100

  instance rateGroupDriver: Svc.RateGroupDriver base id 0x4600

  instance staticMemory: Svc.StaticMemory base id 0x4700

  instance textLogger: Svc.PassiveTextLogger base id 0x4800

  instance fileUplinkBufferManager: Svc.BufferManager base id 0x4400

  instance uplink: Svc.Deframer base id 0x4900

  instance helloWorld: Components.HelloWorld base id 0x0F00

  instance zephyrTime: Svc.Time base id 0x4500 \
    type "Svc::ZephyrTimeImpl" \
    at "../../fprime-zephyr/Zephyr/Drv/ZephyrTime/ZephyrTimeImpl.hpp"

  instance ledGpioDriver: Drv.ZephyrGpioDriver base id 0x5000
  instance led: Components.LedDriver base id 0x5100
}
