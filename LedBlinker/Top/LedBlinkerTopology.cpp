// ======================================================================
// \title  LedBlinkerTopology.cpp
// \brief cpp file containing the topology instantiation code
//
// ======================================================================
// Provides access to autocoded functions
#include <LedBlinker/Top/LedBlinkerTopologyAc.hpp>
#include <LedBlinker/Top/LedBlinkerPacketsAc.hpp>
#include <config/FppConstantsAc.hpp>

// Necessary project-specified types
#include <Os/Log.hpp>
#include <Svc/FramingProtocol/FprimeProtocol.hpp>
#include <Svc/BufferManager/BufferManager.hpp>
#include <Zephyr/Drv/ZephyrGpioDriver/ZephyrGpioDriver.hpp>
#include <Zephyr/Fw/ZephyrMallocAllocator/ZephyrMallocAllocator.hpp>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/drivers/gpio.h>

#define UART_DEVICE_NODE DT_NODELABEL(usart2)
const struct device *const uart = DEVICE_DT_GET(UART_DEVICE_NODE);

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)
static struct gpio_dt_spec led_gpio = GPIO_DT_SPEC_GET(LED0_NODE, gpios);


// Allows easy reference to objects in FPP/autocoder required namespaces
using namespace LedBlinker;

// Instantiate a system logger that will handle Fw::Logger::logMsg calls
Os::Log logger;

// The reference topology uses a malloc-based allocator for components that need to allocate memory during the
// initialization phase.
Fw::ZephyrMallocAllocator mallocator;

// The reference topology uses the F´ packet protocol when communicating with the ground and therefore uses the F´
// framing and deframing implementations.
Svc::FprimeFraming framing;
Svc::FprimeDeframing deframing;

// The reference topology divides the incoming clock signal (1Hz) into sub-signals: 1Hz, 1/2Hz, and 1/4Hz
NATIVE_INT_TYPE rateGroupDivisors[Svc::RateGroupDriver::DIVIDER_SIZE] = {1, 100, 500};

// Rate groups may supply a context token to each of the attached children whose purpose is set by the project. The
// reference topology sets each token to zero as these contexts are unused in this project.
NATIVE_INT_TYPE rateGroup1Context[FppConstant_PassiveRateGroupOutputPorts::PassiveRateGroupOutputPorts] = {};
NATIVE_INT_TYPE rateGroup2Context[FppConstant_PassiveRateGroupOutputPorts::PassiveRateGroupOutputPorts] = {};
NATIVE_INT_TYPE rateGroup3Context[FppConstant_PassiveRateGroupOutputPorts::PassiveRateGroupOutputPorts] = {};

// // A number of constants are needed for construction of the topology. These are specified here.
enum TopologyConstants {
    CMD_SEQ_BUFFER_SIZE = 3 * 1024,
    FILE_DOWNLINK_TIMEOUT = 1000,
    FILE_DOWNLINK_COOLDOWN = 1000,
    FILE_DOWNLINK_CYCLE_TIME = 500,
    FILE_DOWNLINK_FILE_QUEUE_DEPTH = 10,
    // HEALTH_WATCHDOG_CODE = 0x123,
    // COMM_PRIORITY = 100,
    UPLINK_BUFFER_MANAGER_STORE_SIZE = 1000,
    UPLINK_BUFFER_MANAGER_QUEUE_SIZE = 5,
    UPLINK_BUFFER_MANAGER_ID = 200
};

// // Ping entries are autocoded, however; this code is not properly exported. Thus, it is copied here.
// Svc::Health::PingEntry pingEntries[] = {
//     {PingEntries::blockDrv::WARN, PingEntries::blockDrv::FATAL, "blockDrv"},
//     {PingEntries::tlmSend::WARN, PingEntries::tlmSend::FATAL, "chanTlm"},
//     {PingEntries::cmdDisp::WARN, PingEntries::cmdDisp::FATAL, "cmdDisp"},
//     {PingEntries::cmdSeq::WARN, PingEntries::cmdSeq::FATAL, "cmdSeq"},
//     {PingEntries::eventLogger::WARN, PingEntries::eventLogger::FATAL, "eventLogger"},
//     {PingEntries::fileDownlink::WARN, PingEntries::fileDownlink::FATAL, "fileDownlink"},
//     {PingEntries::fileManager::WARN, PingEntries::fileManager::FATAL, "fileManager"},
//     {PingEntries::fileUplink::WARN, PingEntries::fileUplink::FATAL, "fileUplink"},
//     {PingEntries::prmDb::WARN, PingEntries::prmDb::FATAL, "prmDb"},
//     {PingEntries::rateGroup1::WARN, PingEntries::rateGroup1::FATAL, "rateGroup1"},
//     {PingEntries::rateGroup2::WARN, PingEntries::rateGroup2::FATAL, "rateGroup2"},
//     {PingEntries::rateGroup3::WARN, PingEntries::rateGroup3::FATAL, "rateGroup3"},
// };

/**
 * \brief configure/setup components in project-specific way
 *
 * This is a *helper* function which configures/sets up each component requiring project specific input. This includes
 * allocating resources, passing-in arguments, etc. This function may be inlined into the topology setup function if
 * desired, but is extracted here for clarity.
 */
void configureTopology() {
    // Rate group driver needs a divisor list
    rateGroupDriver.configure(rateGroupDivisors, FW_NUM_ARRAY_ELEMENTS(rateGroupDivisors));
    cmdSeq.allocateBuffer(0, mallocator, CMD_SEQ_BUFFER_SIZE);

    // Rate groups require context arrays.
    rateGroup1.configure(rateGroup1Context, FW_NUM_ARRAY_ELEMENTS(rateGroup1Context));
    rateGroup2.configure(rateGroup2Context, FW_NUM_ARRAY_ELEMENTS(rateGroup2Context));
    rateGroup3.configure(rateGroup3Context, FW_NUM_ARRAY_ELEMENTS(rateGroup3Context));

    // Health is supplied a set of ping entires.
    // health.setPingEntries(pingEntries, FW_NUM_ARRAY_ELEMENTS(pingEntries), HEALTH_WATCHDOG_CODE);

    // Parameter database is configured with a database file name, and that file must be initially read.
    prmDb.configure("/seq/PrmDb.dat");
    prmDb.readParamFile();

    // Framer and Deframer components need to be passed a protocol handler
    downlink.setup(framing);
    uplink.setup(deframing);

    // Buffer managers need a configured set of buckets and an allocator used to allocate memory for those buckets.
    Svc::BufferManager::BufferBins upBuffMgrBins;
    memset(&upBuffMgrBins, 0, sizeof(upBuffMgrBins));
    upBuffMgrBins.bins[0].bufferSize = UPLINK_BUFFER_MANAGER_STORE_SIZE;
    upBuffMgrBins.bins[0].numBuffers = UPLINK_BUFFER_MANAGER_QUEUE_SIZE;
    fileUplinkBufferManager.setup(UPLINK_BUFFER_MANAGER_ID, 0, mallocator, upBuffMgrBins);
    // File downlink requires some project-derived properties.
    fileDownlink.configure(FILE_DOWNLINK_TIMEOUT, FILE_DOWNLINK_COOLDOWN, FILE_DOWNLINK_CYCLE_TIME,
                           FILE_DOWNLINK_FILE_QUEUE_DEPTH);

    bool led_gpio_opened = ledGpioDriver.open(&led_gpio, Drv::ZephyrGpioDriver::GpioDirection::OUT);
    FW_ASSERT(led_gpio_opened);

    // Note: Uncomment when using Svc:TlmPacketizer
    // tlmSend.setPacketList(LedBlinkerPacketsPkts, LedBlinkerPacketsIgnore, 1);
}

// Public functions for use in main program are namespaced with deployment name LedBlinker
namespace LedBlinker {
void setupTopology(const TopologyState& state) {
    printk("sizeof('Fw::Object'): %d\n", sizeof(Fw::ObjBase));
    printk("sizeof('Fw::PassiveComponentBase'): %d\n", sizeof(Fw::PassiveComponentBase));
    // printk("sizeof('Components::DummyCompComponentBase'): %d\n", sizeof(Components::DummyCompComponentBase));
    printk("sizeof('Fw::InputCmdPort'): %d\n", sizeof(Fw::InputCmdPort));
    printk("sizeof('Svc::InputSchedPort'): %d\n", sizeof(Svc::InputSchedPort));
    printk("sizeof('Fw::OutputCmdRegPort'): %d\n", sizeof(Fw::OutputCmdRegPort));
    printk("sizeof('Fw::OutputCmdResponsePort'): %d\n", sizeof(Fw::OutputCmdResponsePort));
    printk("sizeof('Fw::OutputLogPort'): %d\n", sizeof(Fw::OutputLogPort));
    printk("sizeof('Fw::OutputTimePort'): %d\n", sizeof(Fw::OutputTimePort));
    printk("sizeof('Fw::OutputTlmPort'): %d\n", sizeof(Fw::OutputTlmPort));
    // printk("sizeof('Components::DummyComp'): %d\n", sizeof(Components::DummyComp));
    printk("sizeof('Svc::TlmChanComponentBase'): %d\n", sizeof(Svc::TlmChanComponentBase));
    printk("sizeof('Svc::CmdSequencerComponentBase'): %d\n", sizeof(Svc::CmdSequencerComponentBase));
    printk("sizeof('Fw::ActiveComponentBase'): %d\n", sizeof(Fw::ActiveComponentBase));
    printk("sizeof('Os::Task'): %d\n", sizeof(Os::Task));


    // Autocoded initialization. Function provided by autocoder.
    initComponents(state);
    // Autocoded id setup. Function provided by autocoder.
    setBaseIds();
    // Autocoded connection wiring. Function provided by autocoder.
    connectComponents();
    // Autocoded command registration. Function provided by autocoder.
    regCommands();
    // Project-specific component configuration. Function provided above. May be inlined, if desired.
    configureTopology();
    // Autocoded parameter loading. Function provided by autocoder.
    loadParameters();
    // Autocoded task kick-off (active components). Function provided by autocoder.
    startTasks(state);

    commUartDriver.configure(uart, 115200);
    FW_ASSERT(led.configureDefaultState());

}

};  // namespace LedBlinker
