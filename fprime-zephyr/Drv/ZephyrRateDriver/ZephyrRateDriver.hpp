// ======================================================================
// \title  ZephyrRateDriver.hpp
// \author ethanchee
// \brief  hpp file for ZephyrRateDriver component implementation class
// ======================================================================

#ifndef ZephyrRateDriver_HPP
#define ZephyrRateDriver_HPP

#include "Drv/ZephyrRateDriver/ZephyrRateDriverComponentAc.hpp"

namespace Drv {

  class ZephyrRateDriver :
    public ZephyrRateDriverComponentBase
  {

    public:

        // ----------------------------------------------------------------------
        // Construction, initialization, and destruction
        // ----------------------------------------------------------------------

        //! Construct object ZephyrRateDriver
        //!
        ZephyrRateDriver(
            const char *const compName /*!< The component name*/
        );

        //! Destroy object ZephyrRateDriver
        //!
        ~ZephyrRateDriver();

        /**
         * Starts the endless internal cycle of the driver.
         * 
         * \param U32 intervalUs: interval to ping in microseconds
         */
        void cycle(const U32 intervalUs);

    };

} // end namespace Drv

#endif
