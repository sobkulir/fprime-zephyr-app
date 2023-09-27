// ======================================================================
// \title  LedMinimalTopology.hpp
// \brief header file containing the topology instantiation definitions
//
// ======================================================================
#ifndef LedMinimal_LedMinimalTOPOLOGY_HPP
#define LedMinimal_LedMinimalTOPOLOGY_HPP
// Included for access to LedMinimal::TopologyState and LedMinimal::ConfigObjects::pingEntries. These definitions are required by the
// autocoder, but are also used in this hand-coded topology.
#include <LedMinimal/Top/LedMinimalTopologyDefs.hpp>

// Remove unnecessary LedMinimal:: qualifications
using namespace LedMinimal;
namespace LedMinimal {
/**
 * \brief initialize and run the F´ topology
 *
 * Initializes, configures, and runs the F´ topology. This is performed through a series of steps, some provided via
 * autocoded functions, and others provided via the functions implementation. These steps are:
 *
 *   1. Call the autocoded `initComponents()` function initializing each component via the `component.init` method
 *   2. Call the autocoded `setBaseIds()` function to set the base IDs (offset) for each component instance
 *   3. Call the autocoded `connectComponents()` function to wire-together the topology of components
 *   4. Configure components requiring custom configuration
 *   5. Call the autocoded `loadParameters()` function to cause each component to load initial parameter values
 *   6. Call the autocoded `startTasks()` function to start the active component tasks
 *   7. Start tasks not owned by active components
 *
 * Step 4 and step 7 are custom and supplied by the project. The ordering of steps 1, 2, 3, 5, and 6 are critical for
 * F´ topologies to function. Configuration (step 4) typically assumes a connect but not started topology and is thus
 * inserted between step 3 and 5. Step 7 may come before or after the active component initializations. Since these
 * custom tasks often start radio communication it is convenient to start them last.
 *
 * The state argument carries command line inputs used to setup the topology. For an explanation of the required type
 * LedMinimal::TopologyState see: LedMinimalTopologyDefs.hpp.
 *
 * \param state: object shuttling CLI arguments (hostname, port) needed to construct the topology
 */
void setupTopology(const TopologyState& state);

} // namespace LedMinimal
#endif
