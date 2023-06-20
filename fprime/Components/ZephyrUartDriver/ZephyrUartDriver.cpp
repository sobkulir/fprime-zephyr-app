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

namespace Components {

namespace {

// Disgusting
void serial_cb(const struct device *dev, void *user_data)
{
    struct ZephyrUartDriver::IrqData *irq_data = reinterpret_cast<struct ZephyrUartDriver::IrqData *>(user_data);

	uint8_t c;

	if (!uart_irq_update(dev)) {
		return;
	}

	if (!uart_irq_rx_ready(dev)) {
		return;
	}

    irq_data->rx_buf_pos = 1;
	/* read until FIFO empty */
	while (uart_fifo_read(dev, &c, 1) == 1) {
		if (irq_data->rx_buf_pos < Q_MSG_SIZE) {
			irq_data->rx_buf[irq_data->rx_buf_pos++] = c;
		}
	}

    irq_data->rx_buf[0] = irq_data->rx_buf_pos - 1;
    if (irq_data->rx_buf_pos > 1) {
        int ret = k_msgq_put(irq_data->msgq, irq_data->rx_buf, K_NO_WAIT);
        if (ret < 0) {
            printk("UART receive queue full\n");
        }
    }
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
    k_msgq_init(&this->msgq, this->msgq_buffer, Q_MSG_SIZE, Q_MAX_MSGS);
    this->irq_data.msgq = &this->msgq;

    if (!device_is_ready(this->m_dev)) {
		return SETUP_DEVICE_NOT_READY;
	}

    int ret = uart_irq_callback_user_data_set(this->m_dev, serial_cb, &this->irq_data);
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
    U32 recv_size = 0;
    U8 *data = fwBuffer.getData();
    char buf[Q_MSG_SIZE];

    while (k_msgq_get(&this->msgq, &buf, K_NO_WAIT) == 0) {
        for (int i = 0; i < buf[0]; i++) {
            data[recv_size] = buf[i+1];
            recv_size++;
        }
    }

    fwBuffer.setSize(recv_size);
    return (recv_size > 0) ? Drv::PollStatus::POLL_OK : Drv::PollStatus::POLL_RETRY;
}

}  // end namespace Components
