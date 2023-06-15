#include <Os/Mutex.hpp>
#include <Fw/Types/Assert.hpp>

#include <zephyr/kernel.h>

namespace Os {
    template <>
    MutexImpl<struct k_mutex>::MutexImpl() {
        NATIVE_INT_TYPE ret = k_mutex_init(&this->m_handle);
        FW_ASSERT(ret == 0, ret);

    }

    template <>
    MutexImpl<struct k_mutex>::~MutexImpl() {
    }

    template <>
    void MutexImpl<struct k_mutex>::lock() {
        NATIVE_INT_TYPE ret = k_mutex_lock(&this->m_handle, K_FOREVER);
        FW_ASSERT(ret == 0, ret);
    }

    template <>
    void MutexImpl<struct k_mutex>::unLock() {
        NATIVE_INT_TYPE ret = k_mutex_unlock(&this->m_handle);
        FW_ASSERT(ret == 0, ret);
    }

}
