// ======================================================================
// \title  TcpClientComponentImpl.cpp
// \author mstarch
// \brief  cpp file for TcpClientComponentImpl component implementation class
//
// \copyright
// Copyright 2009-2020, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================

#include <Components/ZephyrUartDriver/ZephyrUartDriver.hpp>
#include <FpConfig.hpp>
#include "Fw/Types/Assert.hpp"

#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <zephyr/sys/ring_buffer.h>

#include <cassert>

namespace Components {

namespace {

// Disgusting
void serial_cb(const struct device *dev, void *user_data)
{
    struct ring_buf *ring_buf = reinterpret_cast<struct ring_buf *>(user_data);

	if (!uart_irq_update(dev)) {
		return;
	}

	if (!uart_irq_rx_ready(dev)) {
		return;
	}

    uint8_t *buf = nullptr;
    int buf_size = ring_buf_put_claim(ring_buf, &buf, RING_BUF_SIZE);

	/* read until FIFO empty */
	int read_size = uart_fifo_read(dev, buf, buf_size);
    assert(read_size <= buf_size && "UART read size exceeds buffer size");
    
    if (read_size < 0) {
        // TODO: Handle properly.
        printk("UART read error: %d\n", read_size);
        return;
    }
    // potential overrun
    else if (read_size == buf_size) {
        // TODO: Handle properly. Maybe we need to try and drain the read.
        printk("potential UART read overrun\n");
    }

    int ret = ring_buf_put_finish(ring_buf, read_size);
    // Should never fail because we `read_size <= buf_size`.
    assert(ret == 0 && "UART ring buffer put finish failed");
}

}

// ----------------------------------------------------------------------
// Construction, initialization, and destruction
// ----------------------------------------------------------------------

ZephyrUartDriver::ZephyrUartDriver(const char* const compName)
    : ByteStreamDriverModelComponentBase(compName) {}

void ZephyrUartDriver::init(const NATIVE_INT_TYPE instance) {
    ByteStreamDriverModelComponentBase::init(instance);
}

ZephyrUartDriver::SetupStatus ZephyrUartDriver::setup(const struct device *uart) {
    this->m_dev = uart;
    ring_buf_init(&this->ring_buf, RING_BUF_SIZE, this->ring_buf_data);
    
    if (!device_is_ready(this->m_dev)) {
		return SETUP_DEVICE_NOT_READY;
	}

    int ret = uart_irq_callback_user_data_set(this->m_dev, serial_cb, &this->ring_buf);
    FW_ASSERT(ret == 0, ret);

	uart_irq_rx_enable(this->m_dev);
	uart_irq_tx_disable(this->m_dev);

    return SETUP_OK;
}


ZephyrUartDriver::~ZephyrUartDriver() {}


// ----------------------------------------------------------------------
// Handler implementations for user-defined typed input ports
// ----------------------------------------------------------------------

Drv::SendStatus ZephyrUartDriver::send_handler(const NATIVE_INT_TYPE portNum, Fw::Buffer& fwBuffer) {
    U8 *data = fwBuffer.getData();
    for (U32 i = 0; i < fwBuffer.getSize(); i++) {
        uart_poll_out(this->m_dev, data[i]);
    }

    if (this->isConnected_deallocate_OutputPort(0)) {
        deallocate_out(0, fwBuffer);
    }
    return Drv::SendStatus::SEND_OK;
}

Drv::PollStatus ZephyrUartDriver::poll_handler(const NATIVE_INT_TYPE portNum, Fw::Buffer& fwBuffer) {

    U8 *data = fwBuffer.getData();

    uint32_t recv_size = ring_buf_get(&ring_buf, data, fwBuffer.getSize());
    fwBuffer.setSize(recv_size);
    return (recv_size > 0) ? Drv::PollStatus::POLL_OK : Drv::PollStatus::POLL_RETRY;
}

}  // end namespace Components
