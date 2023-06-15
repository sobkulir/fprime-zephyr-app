// ======================================================================
// \title  Main.cpp
// \brief main program for the F' application. Currently only prints to serial.
//
// ======================================================================
// Used to access topology functions
#include <MyDeployment/Top/MyDeploymentTopology.hpp>
#include <zephyr/kernel.h>

int main() {
    MyDeployment::TopologyState inputs;

    printk("Setting up topology\n");
    MyDeployment::setupTopology(inputs);
    printk("Topology running, entering simulatedCycle.\n");
    startSimulatedCycle(200);
    return 0;
}
