// ======================================================================
// \title  ZephyrUartDriver.cpp
// \author ethanchee
// \brief  cpp file for ZephyrUartDriver component implementation class
// ======================================================================


#include <Drv/ZephyrUartDriver/ZephyrUartDriver.hpp>
#include "Fw/Types/BasicTypes.hpp"
#include "Fw/Types/Assert.hpp"
#include <FpConfig.hpp>

namespace Drv {

    // ----------------------------------------------------------------------
    // Construction, initialization, and destruction
    // ----------------------------------------------------------------------

    ZephyrUartDriver ::
        ZephyrUartDriver(
            const char *const compName
        ) : ZephyrUartDriverComponentBase(compName)
    {

    }

    ZephyrUartDriver ::
        ~ZephyrUartDriver()
    {

    }

    int ZephyrUartDriver::configure(const struct device *dev, struct uart_config *uart_cfg) {
        FW_ASSERT(dev != nullptr);

        this->m_dev = dev;
        int ret;
        
        if (!device_is_ready(this->m_dev)) {
            return -1;
        }

        if (uart_cfg != nullptr) {
            ret = uart_configure(this->m_dev, uart_cfg);
            if (ret < 0) {
                return ret;
            }
        }

        ring_buf_init(&this->m_ring_buf, SERIAL_BUFFER_SIZE, this->m_ring_buf_data);
        this->m_serial_cb_data.ring_buf = &this->m_ring_buf;
        this->m_serial_cb_data.buf_overruns = 0;

        ret = uart_irq_callback_user_data_set(this->m_dev, serial_cb, &this->m_serial_cb_data);
        if (ret < 0) {
            return ret;
        }

        uart_irq_rx_enable(this->m_dev);
	    uart_irq_tx_disable(this->m_dev);

        if (this->isConnected_ready_OutputPort(0)) {
            this->ready_out(0);
        }

        return 0;
    }

    void ZephyrUartDriver::serial_cb(const struct device *dev, void *user_data)
    {
        struct serial_cb_data *cb_data = reinterpret_cast<struct serial_cb_data *>(user_data);

        if (!uart_irq_update(dev)) {
            return;
        }

        if (!uart_irq_rx_ready(dev)) {
            return;
        }

        U8 c;
        
        for (U32 i = 0; i < SERIAL_BUFFER_SIZE; ++i) {
            int ret = uart_fifo_read(dev, &c, 1);
            if (ret != 1) {
                break;
            }

            if (ring_buf_put(cb_data->ring_buf, &c, 1) != 1) {
                cb_data->buf_overruns++;
            }
        } 
    }

    // ----------------------------------------------------------------------
    // Handler implementations for user-defined typed input ports
    // ----------------------------------------------------------------------

    void ZephyrUartDriver ::
        schedIn_handler(
            const NATIVE_INT_TYPE portNum,
            NATIVE_UINT_TYPE context
        )
    {
        // Assert because schedIn should only be called once uart is configured.
        FW_ASSERT(this->m_dev != nullptr);

        Fw::Buffer recv_buffer = this->allocate_out(0, SERIAL_BUFFER_SIZE);
        FW_ASSERT(recv_buffer.getData() != nullptr);

        U32 recv_size = ring_buf_get(&this->m_ring_buf, recv_buffer.getData(), recv_buffer.getSize());
        recv_buffer.setSize(recv_size);

        recv_out(0, recv_buffer, Drv::RecvStatus::RECV_OK);
    }

    void ZephyrUartDriver ::
        schedInTlm_handler(
            const NATIVE_INT_TYPE portNum,
            NATIVE_UINT_TYPE context
        )
    {
        this->tlmWrite_BufferOverruns(this->m_serial_cb_data.buf_overruns);
    }

    Drv::SendStatus ZephyrUartDriver ::
        send_handler(
            const NATIVE_INT_TYPE portNum,
            Fw::Buffer &sendBuffer
        )
    {
        if (this->m_dev == nullptr) {
            return Drv::SendStatus::SEND_ERROR;
        }

        for (U32 i = 0; i < sendBuffer.getSize(); i++) {
            uart_poll_out(this->m_dev, sendBuffer.getData()[i]);
        }

        if (this->isConnected_deallocate_OutputPort(0)) {
            deallocate_out(0, sendBuffer);
        }
        return Drv::SendStatus::SEND_OK;
    }

} // end namespace Drv
