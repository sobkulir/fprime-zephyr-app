// ======================================================================
// \title  ZephyrGpioDriver.cpp
// \author ethanchee
// \brief  cpp file for ZephyrGpioDriver component implementation class
// ======================================================================

#include <Zephyr/Drv/ZephyrGpioDriver/ZephyrGpioDriver.hpp>
#include <FpConfig.hpp>
#include <Fw/Types/Assert.hpp>

#include <zephyr/drivers/gpio.h>

namespace Drv
{

  // ----------------------------------------------------------------------
  // Construction, initialization, and destruction
  // ----------------------------------------------------------------------

  ZephyrGpioDriver ::
      ZephyrGpioDriver(
          const char *const compName) : ZephyrGpioDriverComponentBase(compName), m_pin(nullptr)
  {
  }

  ZephyrGpioDriver ::
      ~ZephyrGpioDriver()
  {
  }

  bool ZephyrGpioDriver::open(struct gpio_dt_spec *gpio, GpioDirection direction)
  {
    FW_ASSERT(this->m_pin == nullptr);
    FW_ASSERT(gpio != nullptr);

    this->m_pin = gpio;

    if (!gpio_is_ready_dt(this->m_pin))
    {
      return false;
    }

    if (gpio_pin_configure_dt(this->m_pin, (direction == GpioDirection::IN ? GPIO_INPUT : GPIO_OUTPUT)) < 0)
    {
      return false;
    }

    return true;
  }

  // ----------------------------------------------------------------------
  // Handler implementations for user-defined typed input ports
  // ----------------------------------------------------------------------

  Drv::ZephyrGpioStatus ZephyrGpioDriver ::
      gpioRead_handler(
          const NATIVE_INT_TYPE portNum,
          Fw::Logic &state)
  {
    FW_ASSERT(this->m_pin != nullptr);

    int value = gpio_pin_get_dt(this->m_pin);
    if (value == -EIO) {
      return Drv::ZephyrGpioStatus::GPIO_IO_ERR;
    } else if (value < 0) {
      return Drv::ZephyrGpioStatus::GPIO_OTHER_ERR;
    }

    FW_ASSERT(value == 0 || value == 1);
    state = (value == 1) ? Fw::Logic::HIGH : Fw::Logic::LOW;
    return Drv::ZephyrGpioStatus::GPIO_OK;
  }

  Drv::ZephyrGpioStatus ZephyrGpioDriver ::
      gpioWrite_handler(
          const NATIVE_INT_TYPE portNum,
          const Fw::Logic &state)
  {
    FW_ASSERT(this->m_pin != nullptr);

    int value = gpio_pin_set_dt(this->m_pin, (state == Fw::Logic::HIGH) ? 1 : 0);
    if (value == -EIO) {
      return Drv::ZephyrGpioStatus::GPIO_IO_ERR;
    } else if (value < 0) {
      return Drv::ZephyrGpioStatus::GPIO_OTHER_ERR;
    }

    return Drv::ZephyrGpioStatus::GPIO_OK;
  }

} // end namespace Drv
