// ======================================================================
// \title  Main.cpp
// \brief main program for the F' application. Currently only prints to serial.
//
// ======================================================================
// Used to access topology functions
#include <LedMinimal/Top/LedMinimalTopology.hpp>
#include <LedMinimal/Top/LedMinimalTopologyAc.hpp>
#include <zephyr/kernel.h>


int main()
{
    LedMinimal::TopologyState inputs;
    printk("Setting up topology\n");
    LedMinimal::setupTopology(inputs);
    printk("Topology running, entering simulatedCycle.\n");
    zephyrRateDriver.cycle(/*intervalUs=*/1 * USEC_PER_MSEC);

    // Should be never executed.
    while (1) ; 
    return 1;
}
