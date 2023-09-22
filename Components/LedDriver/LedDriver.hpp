// ======================================================================
// \title  LedDriver.hpp
// \author user
// \brief  hpp file for LedDriver component implementation class
// ======================================================================

#ifndef LedDriver_HPP
#define LedDriver_HPP

#include "Components/LedDriver/LedDriverComponentAc.hpp"

namespace Components {

  class LedDriver :
    public LedDriverComponentBase
  {

    public:

      // ----------------------------------------------------------------------
      // Construction, initialization, and destruction
      // ----------------------------------------------------------------------

      //! Construct object LedDriver
      //!
      LedDriver(
          const char *const compName /*!< The component name*/
      );

      //! Destroy object LedDriver
      //!
      ~LedDriver();

      //! Sets the LED to the default state read from the parameter.
      //! Returns true iff function succeded.
      bool configureDefaultState(void);

    PRIVATE:

      // ----------------------------------------------------------------------
      // Command handler implementations
      // ----------------------------------------------------------------------

      //! Implementation for LED_TOGGLE command handler
      //! Toggles the LED to the opposite state
      void LED_TOGGLE_cmdHandler(
          const FwOpcodeType opCode, /*!< The opcode*/
          const U32 cmdSeq /*!< The command sequence number*/
      );

      //! Implementation for LED_ON command handler
      //! Toggles the LED to on state
      void LED_ON_cmdHandler(
          const FwOpcodeType opCode, /*!< The opcode*/
          const U32 cmdSeq /*!< The command sequence number*/
      );

      //! Implementation for LED_OFF command handler
      //! Toggles the LED to off state
      void LED_OFF_cmdHandler(
          const FwOpcodeType opCode, /*!< The opcode*/
          const U32 cmdSeq /*!< The command sequence number*/
      );

    PRIVATE:
      // ----------------------------------------------------------------------
      // Helper methods
      // ----------------------------------------------------------------------

      //! Sets the LED to the desired state
      //! \return bool: True iff the LED was set to the desired state
      bool setLedState(bool desiredState);

    PRIVATE:

      // ----------------------------------------------------------------------
      // Variables
      // ----------------------------------------------------------------------

      //! Number of times the LED has transitioned from on to off or vice versa
      U64 transitionCount;

      //! Current state of the LED (true = on, false = off)
      bool state;
    };

} // end namespace Components

#endif
