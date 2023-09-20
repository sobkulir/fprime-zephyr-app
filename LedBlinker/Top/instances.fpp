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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::cmdSeq),
    ConfigObjects::cmdSeq::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::cmdDisp),
    ConfigObjects::cmdDisp::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::eventLogger),
    ConfigObjects::eventLogger::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::tlmSend),
    ConfigObjects::tlmSend::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::prmDb),
    ConfigObjects::prmDb::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::fileUplink),
    ConfigObjects::fileUplink::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::fileDownlink),
    ConfigObjects::fileDownlink::stack    
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
    Os::Task::TASK_DEFAULT, // Default CPU
    static_cast<NATIVE_UINT_TYPE>(TaskIds::fileManager),
    ConfigObjects::fileManager::stack    
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

  instance zephyrTime: Components.ZephyrTime base id 0x4500
  
}
