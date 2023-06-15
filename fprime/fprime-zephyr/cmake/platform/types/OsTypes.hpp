
#ifndef OS_TYPES_H
#define OS_TYPES_H

#include <Fw/Types/BasicTypes.hpp>
#include <zephyr/kernel.h>

namespace Os {
    template <typename T>
    class MutexImpl;
    using Mutex = MutexImpl<struct k_mutex>;
}

#endif  // OS_TYPES_H