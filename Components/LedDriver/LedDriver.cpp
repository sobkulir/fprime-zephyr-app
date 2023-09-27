// ======================================================================
// \title  LedDriver.cpp
// \author user
// \brief  cpp file for LedDriver component implementation class
// ======================================================================


#include <Components/LedDriver/LedDriver.hpp>
#include <FpConfig.hpp>

namespace Components {

  // ----------------------------------------------------------------------
  // Construction, initialization, and destruction
  // ----------------------------------------------------------------------

  LedDriver ::
    LedDriver(
        const char *const compName
    ) : LedDriverComponentBase(compName), transitionCount(0), state(false)
  {

  }

  LedDriver ::
    ~LedDriver()
  {

  }

  bool LedDriver :: configureDefaultState(void)
  {
    // Uncomment if there's a parameter database. I commented it out to work with
    // LedMinimal, which doesn't have non-volatile memory so prmDb can't be used.

    // Read back the parameter value
    // Fw::ParamValid paramValidity;
    // bool defaultState = this->paramGet_defaultState(paramValidity);

    // if (Fw::ParamValid::INVALID == paramValidity) {
    //   return false;
    // }

    // this->state = defaultState;
    
    // FW_ASSERT(this->isConnected_gpioSet_OutputPort(0));
    Drv::ZephyrGpioStatus status = this->gpioSet_out(0, this->state ? Fw::Logic::HIGH : Fw::Logic::LOW);
    return (status == Drv::ZephyrGpioStatus::GPIO_OK);
  }

  // ----------------------------------------------------------------------
  // Command handler implementations
  // ----------------------------------------------------------------------

  void LedDriver ::
    LED_TOGGLE_cmdHandler(
        const FwOpcodeType opCode,
        const U32 cmdSeq
    )
  {
    bool isSuccess = this->setLedState(!this->state);
    this->cmdResponse_out(opCode,cmdSeq, (isSuccess) ? Fw::CmdResponse::OK : Fw::CmdResponse::EXECUTION_ERROR);
  }

  void LedDriver ::
    LED_ON_cmdHandler(
        const FwOpcodeType opCode,
        const U32 cmdSeq
    )
  {
    bool isSuccess = this->setLedState(/*desiredState=*/true);
    this->cmdResponse_out(opCode,cmdSeq, (isSuccess) ? Fw::CmdResponse::OK : Fw::CmdResponse::EXECUTION_ERROR);
  }

  void LedDriver ::
    LED_OFF_cmdHandler(
        const FwOpcodeType opCode,
        const U32 cmdSeq
    )
  {
    bool isSuccess = this->setLedState(/*desiredState=*/false);
    this->cmdResponse_out(opCode,cmdSeq, (isSuccess) ? Fw::CmdResponse::OK : Fw::CmdResponse::EXECUTION_ERROR);
  }

  // ----------------------------------------------------------------------
  // Helper methods
  // ----------------------------------------------------------------------


  bool LedDriver ::
    setLedState(bool desiredState) {
      Drv::ZephyrGpioStatus status = this->gpioSet_out(0, desiredState ? Fw::Logic::HIGH : Fw::Logic::LOW);
      
      if (status != Drv::ZephyrGpioStatus::GPIO_OK) {
        this->log_WARNING_HI_LedError(desiredState, this->state, status);
        return false;
      }

      if (this->state != desiredState) {
        this->state = desiredState;
        this->log_ACTIVITY_LO_LedState(this->state);
        this->tlmWrite_TransitionCount(++this->transitionCount);
      }
      return true;
    }


} // end namespace Components
