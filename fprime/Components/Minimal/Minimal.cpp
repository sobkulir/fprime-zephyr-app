// ======================================================================
// \title  Minimal.cpp
// \author user
// \brief  cpp file for Minimal component implementation class
// ======================================================================


#include <Components/Minimal/Minimal.hpp>
#include <FpConfig.hpp>
#include <Fw/Com/ComBuffer.hpp>
#include <zephyr/kernel.h>

#include <cstdio>

namespace Components {

  // ----------------------------------------------------------------------
  // Construction, initialization, and destruction
  // ----------------------------------------------------------------------

  Minimal ::
    Minimal(
        const char *const compName
    ) : MinimalComponentBase(compName)
  {
  }

  Minimal ::
    ~Minimal()
  {

  }

  // ----------------------------------------------------------------------
  // Handler implementations for user-defined typed input ports
  // ----------------------------------------------------------------------

  void Minimal ::
    schedIn_handler(NATIVE_INT_TYPE portNum, NATIVE_UINT_TYPE context)
  {
      printk("Hovnoo\n");
  }

  void Minimal::DUMMY_CMD_cmdHandler(FwOpcodeType opCode, U32 cmdSeq) {
    // Log event for NO_OP here.
    this->cmdResponse_out(opCode,cmdSeq,Fw::CmdResponse::OK);
  }
} // end namespace Components
