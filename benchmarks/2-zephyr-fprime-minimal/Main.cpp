// ======================================================================
// \title  Main.cpp
// \brief main program for the F' application. Currently only prints to serial.
//
// ======================================================================
// Used to access topology functions
#include <benchmarks/2-zephyr-fprime-minimal/Top/MyDeploymentTopology.hpp>
#include <zephyr/kernel.h>

#include <zephyr/device.h>

int main()
{
    MyDeployment::TopologyState inputs;
    MyDeployment::setupTopology(inputs);
    // startSimulatedCycle(100);
    return 0;
}
