// ======================================================================
// \title  Main.cpp
// \brief main program for the F' application. Currently only prints to serial.
//
// ======================================================================
// Used to access topology functions
#include <MyDeployment/Top/MyDeploymentTopology.hpp>
#include <zephyr/kernel.h>

int main() {
    // Object for communicating state to the reference topology
    MyDeployment::TopologyState inputs;
    inputs.hostname = "";
    inputs.port = 3;

    printk("Setting up topology\n");
    MyDeployment::setupTopology(inputs);
    printk("Setting up topology -- Done\n");
    return 0;
}
