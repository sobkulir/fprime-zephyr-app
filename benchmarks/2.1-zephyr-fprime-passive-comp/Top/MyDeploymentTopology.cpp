// ======================================================================
// \title  MyDeploymentTopology.cpp
// \brief cpp file containing the topology instantiation code
//
// ======================================================================
// Provides access to autocoded functions
#include <benchmarks/2.1-zephyr-fprime-passive-comp/Top/MyDeploymentTopologyAc.hpp>
#include <benchmarks/2.1-zephyr-fprime-passive-comp/Top/MyDeploymentPacketsAc.hpp>

// Necessary project-specified types
#include <Fw/Types/MallocAllocator.hpp>
#include <Os/Log.hpp>
#include <Svc/FramingProtocol/FprimeProtocol.hpp>
#include <Svc/BufferManager/BufferManager.hpp>

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>


// Allows easy reference to objects in FPP/autocoder required namespaces
using namespace MyDeployment;

// // A number of constants are needed for construction of the topology. These are specified here.
enum TopologyConstants {
    CMD_SEQ_BUFFER_SIZE = 3 * 1024,
    // FILE_DOWNLINK_TIMEOUT = 1000,
    // FILE_DOWNLINK_COOLDOWN = 1000,
    // FILE_DOWNLINK_CYCLE_TIME = 1000,
    // FILE_DOWNLINK_FILE_QUEUE_DEPTH = 10,
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
    // rateGroupDriver.configure(rateGroupDivisors, FW_NUM_ARRAY_ELEMENTS(rateGroupDivisors));
    // cmdSeq.allocateBuffer(0, mallocator, CMD_SEQ_BUFFER_SIZE);

    // // Rate groups require context arrays.
    // rateGroup1.configure(rateGroup1Context, FW_NUM_ARRAY_ELEMENTS(rateGroup1Context));
    // rateGroup2.configure(rateGroup2Context, FW_NUM_ARRAY_ELEMENTS(rateGroup2Context));

    // // Health is supplied a set of ping entires.
    // // health.setPingEntries(pingEntries, FW_NUM_ARRAY_ELEMENTS(pingEntries), HEALTH_WATCHDOG_CODE);

    // // Framer and Deframer components need to be passed a protocol handler
    // downlink.setup(framing);
    // uplink.setup(deframing);

    // // Buffer managers need a configured set of buckets and an allocator used to allocate memory for those buckets.
    // Svc::BufferManager::BufferBins upBuffMgrBins;
    // memset(&upBuffMgrBins, 0, sizeof(upBuffMgrBins));
    // upBuffMgrBins.bins[0].bufferSize = UPLINK_BUFFER_MANAGER_STORE_SIZE;
    // upBuffMgrBins.bins[0].numBuffers = UPLINK_BUFFER_MANAGER_QUEUE_SIZE;
    // fileUplinkBufferManager.setup(UPLINK_BUFFER_MANAGER_ID, 0, mallocator, upBuffMgrBins);

    // comm.setup(
    //     uart,
    //     /*readTaskPriority=*/40,
    //     static_cast<NATIVE_UINT_TYPE>(K_THREAD_STACK_SIZEOF(uartDriverReadTaskStack)),
    //     uartDriverReadTaskStack);
    // Note: Uncomment when using Svc:TlmPacketizer
    // tlmSend.setPacketList(MyDeploymentPacketsPkts, MyDeploymentPacketsIgnore, 1);
}

// Public functions for use in main program are namespaced with deployment name MyDeployment
namespace MyDeployment {
void setupTopology(const TopologyState& state) {
    // Autocoded initialization. Function provided by autocoder.
    initComponents(state);
    // Autocoded id setup. Function provided by autocoder.
    setBaseIds();
    // Autocoded connection wiring. Function provided by autocoder.
    connectComponents();
    // Autocoded command registration. Function provided by autocoder.
    // regCommands();
    // Project-specific component configuration. Function provided above. May be inlined, if desired.
    configureTopology();
    // Autocoded parameter loading. Function provided by autocoder.
    // loadParameters();
    // Autocoded task kick-off (active components). Function provided by autocoder.
    startTasks(state);
}

// void startSimulatedCycle(U32 milliseconds) {
//     while (true) {
//         MyDeployment::zephyrTimer.tick();
//         k_sleep(K_MSEC(milliseconds));

//     }
// }

};  // namespace MyDeployment
