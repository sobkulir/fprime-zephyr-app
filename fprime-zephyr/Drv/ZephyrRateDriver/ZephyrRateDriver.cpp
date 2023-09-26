// ======================================================================
// \title  ZephyrRateDriver.cpp
// \author ethanchee
// \brief  cpp file for ZephyrRateDriver component implementation class
// ======================================================================

#include <Drv/ZephyrRateDriver/ZephyrRateDriver.hpp>
#include <FpConfig.hpp>
#include <Fw/Logger/Logger.hpp>
#include <Fw/Types/Assert.hpp>

#include <zephyr/kernel.h>

namespace Drv
{

    // ----------------------------------------------------------------------
    // Construction, initialization, and destruction
    // ----------------------------------------------------------------------

    ZephyrRateDriver ::
        ZephyrRateDriver(
            const char *const compName) : ZephyrRateDriverComponentBase(compName)
    {
    }

    ZephyrRateDriver ::
        ~ZephyrRateDriver()
    {
    }

    void ZephyrRateDriver::cycle(const U32 intervalUs)
    {
        // Consider implementing this using k_timer APIs instead for higher precision,
        // depending on your MCU.

        Fw::Logger::logMsg("Starting base rate group clock with period of %" PRIu32 " microseconds\n", intervalUs);

        // Ideally, we would use HW cycles, but our platform (STM32H723), doesn't support
        // 64-bit cycle counter. Kernel tick-rate is configurable via
        // CONFIG_SYS_CLOCK_TICKS_PER_SEC (default 10KHz).
        I64 intervalTicks = k_us_to_ticks_floor64(intervalUs);
        I64 epochStartTicks = k_uptime_ticks();
        FW_ASSERT(epochStartTicks >= 0, epochStartTicks);

        I64 totalCycles = 0;

        while (true)
        {
            Svc::TimerVal now;
            now.take();
            if (this->isConnected_CycleOut_OutputPort(0))
            {
                this->CycleOut_out(0, now);
            }

            I64 nowTicks = k_uptime_ticks();
            FW_ASSERT(nowTicks >= 0, nowTicks);

            I64 curCycle = (nowTicks - epochStartTicks) / intervalTicks;
            
            // Asserts on a cycle slip.
            // Note: Depending on the app, it might be a better idea to log it as tellemetry instead.
            FW_ASSERT(totalCycles == curCycle, curCycle - totalCycles);
            totalCycles = curCycle + 1;

            I64 waitTicks = epochStartTicks + (curCycle + 1) * intervalTicks - nowTicks;
            I32 sleep_ret = k_sleep(K_TICKS(waitTicks));
            // Assert no one else can wake up the main thread.
            FW_ASSERT(sleep_ret == 0, sleep_ret);
        }
    }


} // end namespace Drv
