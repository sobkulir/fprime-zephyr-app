// ======================================================================
// \title  ZephyrUartDriver.hpp
// \author ethanchee
// \brief  hpp file for ZephyrUartDriver component implementation class
// ======================================================================

#ifndef ZephyrUartDriver_HPP
#define ZephyrUartDriver_HPP

#include "Drv/ZephyrUartDriver/ZephyrUartDriverComponentAc.hpp"

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/sys/ring_buffer.h>

// Important: The schedIn is assumed to be called at 500Hz for the RING_BUF_SIZE.

namespace Drv {

  class ZephyrUartDriver :
    public ZephyrUartDriverComponentBase
  {

    // At 115200 baud rate, we get at most 115200 / (8 * 1024) ~= 14kB/s.
    // The buffer-flushing is called at 500Hz, so in theory the buffer needs to be
    // 14kB / 500Hz at least 28B. We set it to 128B to be safe. 
    static constexpr NATIVE_INT_TYPE SERIAL_BUFFER_SIZE = 128;

    public:

        // ----------------------------------------------------------------------
        // Construction, initialization, and destruction
        // ----------------------------------------------------------------------

        //! Construct object ZephyrUartDriver
        //!
        ZephyrUartDriver(
            const char *const compName /*!< The component name*/
        );

        //! Destroy object ZephyrUartDriver
        //!
        ~ZephyrUartDriver();

        //! Configures the UART device. The argument `uart_cfg` is optional so that underlying drivers
        //! which can't be configured at runtime are still supported.
        //! \return 0 on success, negative on failure
        int configure(const struct device *dev, struct uart_config *uart_cfg);

    PRIVATE:

        struct serial_cb_data {
            struct ring_buf *ring_buf;
            U32 buf_overruns;
        };

        static void serial_cb(const struct device *dev, void *user_data);

        // ----------------------------------------------------------------------
        // Handler implementations for user-defined typed input ports
        // ----------------------------------------------------------------------

        //! Handler implementation for schedIn
        //!
        void schedIn_handler(
            const NATIVE_INT_TYPE portNum, /*!< The port number*/
            NATIVE_UINT_TYPE context /*!< 
        The call order
        */
        );

                //! Handler implementation for schedIn
        //!
        void schedInTlm_handler(
            const NATIVE_INT_TYPE portNum, /*!< The port number*/
            NATIVE_UINT_TYPE context /*!< 
        The call order
        */
        );


        //! Handler implementation for send
        //!
        Drv::SendStatus send_handler(
            const NATIVE_INT_TYPE portNum, /*!< The port number*/
            Fw::Buffer &sendBuffer 
        );

        const struct device *m_dev;

        U8 m_ring_buf_data[SERIAL_BUFFER_SIZE];
        struct ring_buf m_ring_buf;

        struct serial_cb_data m_serial_cb_data;
    };

} // end namespace Drv

#endif
