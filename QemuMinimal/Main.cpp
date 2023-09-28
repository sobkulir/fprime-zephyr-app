// ======================================================================
// \title  Main.cpp
// \brief main program for the F' application. Currently only prints to serial.
//
// ======================================================================
// Used to access topology functions
#include <QemuMinimal/Top/QemuMinimalTopology.hpp>
#include <QemuMinimal/Top/QemuMinimalTopologyAc.hpp>
#include <zephyr/kernel.h>


int main()
{
    QemuMinimal::TopologyState inputs;
    printk("Setting up topology\n");
    QemuMinimal::setupTopology(inputs);
    printk("Topology running, entering simulatedCycle.\n");
    zephyrRateDriver.cycle(/*intervalUs=*/30 * USEC_PER_MSEC);

    // Should be never executed.
    while (1) ; 
    return 1;
}
