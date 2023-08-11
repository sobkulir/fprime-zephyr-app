// ======================================================================
// \title  Minimal.hpp
// \author user
// \brief  hpp file for Minimal component implementation class
// ======================================================================

#ifndef Minimal_HPP
#define Minimal_HPP

#include "Components/Minimal/MinimalComponentAc.hpp"
#include <Fw/Com/ComBuffer.hpp>

namespace Components {

  class Minimal:
    public MinimalComponentBase
  {

    public:

      // ----------------------------------------------------------------------
      // Construction, initialization, and destruction
      // ----------------------------------------------------------------------

      //! Construct object Minimal
      //!
      Minimal(
          const char *const compName /*!< The component name*/
      );

      //! Destroy object Minimal
      //!
      ~Minimal();

    PRIVATE:

      // ----------------------------------------------------------------------
      // Handler implementations for user-defined typed input ports
      // ----------------------------------------------------------------------

      void DUMMY_CMD_cmdHandler(FwOpcodeType opCode, U32 cmdSeq);


      void schedIn_handler(
          const NATIVE_INT_TYPE portNum,
          NATIVE_UINT_TYPE context
      );
    };

} // end namespace Components

#endif
