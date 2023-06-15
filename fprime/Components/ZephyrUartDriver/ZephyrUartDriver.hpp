
#ifndef ZephyrUartDriver_HPP
#define ZephyrUartDriver_HPP

#include "Drv/ByteStreamDriverModel/ByteStreamDriverModelComponentAc.hpp"

#include <zephyr/kernel.h>
#include <zephyr/device.h>

#define Q_MSG_SIZE 4
#define Q_MAX_MSGS 400

namespace Components {

class ZephyrUartDriver : public Drv::ByteStreamDriverModelComponentBase {
  public:
    enum SetupStatus {
        SETUP_OK, //!<  Setup was successful
        SETUP_DEVICE_NOT_READY, //!<  Device is not ready
    };
    
    struct IrqData {
      char rx_buf[Q_MSG_SIZE];
      int rx_buf_pos;
      struct k_msgq *msgq;
    };

    // ----------------------------------------------------------------------
    // Construction, initialization, and destruction
    // ----------------------------------------------------------------------

    /**
     * \brief construct the ZephyrUartDriver component.
     * \param compName: name of this component
     */
    ZephyrUartDriver(const char* const compName);


    /**
     * \brief Initialize this component
     * \param instance: instance number of this component
     */
    void init(const NATIVE_INT_TYPE instance = 0);

    SetupStatus setup(const struct device *uart);

    /**
     * \brief Destroy the component
     */
    ~ZephyrUartDriver();

  PRIVATE:

    // ----------------------------------------------------------------------
    // Handler implementations for user-defined typed input ports
    // ----------------------------------------------------------------------

    /**
     * \brief Send data out of the ZephyrUart
     *
     * Passing data to this handler sends them out over UART.
     * 
     * \param portNum: fprime port number of the incoming port call
     * \param fwBuffer: buffer containing data to be sent
     * \return SEND_OK on success, SEND_RETRY when critical data should be retried and SEND_ERROR upon error
     */
    Drv::SendStatus send_handler(const NATIVE_INT_TYPE portNum, Fw::Buffer& fwBuffer);

    /**
     * \brief Polls out the data from the driver.
     */
    Drv::PollStatus poll_handler(const NATIVE_INT_TYPE portNum, Fw::Buffer& fwBuffer);

    const struct device *m_dev;
    alignas(4) char msgq_buffer[Q_MAX_MSGS * Q_MSG_SIZE];
    struct k_msgq msgq;
    IrqData irq_data;

};

}  // end namespace Drv

#endif // end ZephyrUartDriver
