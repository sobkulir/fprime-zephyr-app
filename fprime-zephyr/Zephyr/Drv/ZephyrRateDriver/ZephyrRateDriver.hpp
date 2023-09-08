// ======================================================================
// \title  ZephyrRateDriver.hpp
// \author ethanchee
// \brief  hpp file for ZephyrRateDriver component implementation class
// ======================================================================

#ifndef ZephyrRateDriver_HPP
#define ZephyrRateDriver_HPP

#include "Zephyr/Drv/ZephyrRateDriver/ZephyrRateDriverComponentAc.hpp"
#include <Svc/Cycle/TimerVal.hpp>
#include <zephyr/kernel.h>

namespace Zephyr {

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
         * Configure this component with the interval time in microseconds.
         * \param U32 intervalUs: interval to ping in microseconds
         */
        void configure(U32 intervalUs);

        /**
         * Starts the endless internal cycle of the driver.
         */
        void cycle();


        //!< Interval of the driver
        U32 m_intervalUs;

    PRIVATE:

        //!< Last time of run
        Svc::TimerVal m_last;
        static ZephyrRateDriver* s_driver;
        struct k_timer s_itimer;

    };

} // end namespace Zephyr

#endif
