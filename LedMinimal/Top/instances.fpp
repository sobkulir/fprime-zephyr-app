module LedMinimal {

  # ----------------------------------------------------------------------
  # Defaults
  # ----------------------------------------------------------------------

  module Default {
    constant QUEUE_SIZE = 10
    constant STACK_SIZE = 12 * 1024
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

  # ----------------------------------------------------------------------
  # Queued component instances
  # ----------------------------------------------------------------------

  # instance $health: Svc.Health base id 0x2000 \
  #   queue size 25

  # ----------------------------------------------------------------------
  # Passive component instances
  # ----------------------------------------------------------------------

  @ Communications driver.
  instance commUartDriver: Drv.ZephyrUartDriver base id 0x4000

  instance downlink: Svc.Framer base id 0x4100

  instance rateGroup1: Svc.PassiveRateGroup base id 0x1000

  instance rateGroup2: Svc.PassiveRateGroup base id 0x1200

  instance rateGroup3: Svc.PassiveRateGroup base id 0x1300

  instance zephyrRateDriver: Drv.ZephyrRateDriver base id 0x1100

  instance rateGroupDriver: Svc.RateGroupDriver base id 0x4600

  instance staticMemory: Svc.StaticMemory base id 0x4700

  instance textLogger: Svc.PassiveTextLogger base id 0x4800

  instance uplink: Svc.Deframer base id 0x4900

  instance zephyrTime: Svc.Time base id 0x4500 \
    type "Svc::ZephyrTimeImpl" \
    at "../../fprime-zephyr/Drv/ZephyrTime/ZephyrTimeImpl.hpp"

  instance ledGpioDriver: Drv.ZephyrGpioDriver base id 0x5000
  instance led: Components.LedDriver base id 0x5100
}
