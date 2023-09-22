/**
 * \file
 * \author T. Canham
 * \brief Implementation of malloc based allocator
 *
 * \copyright
 * Copyright 2009-2016, by the California Institute of Technology.
 * ALL RIGHTS RESERVED.  United States Government Sponsorship
 * acknowledged.
 *
 */

#include <Zephyr/Fw/ZephyrMallocAllocator/ZephyrMallocAllocator.hpp>
#include <zephyr/kernel.h>

namespace Fw {

    ZephyrMallocAllocator::ZephyrMallocAllocator() {
    }

    ZephyrMallocAllocator::~ZephyrMallocAllocator() {
    }

    void *ZephyrMallocAllocator::allocate(const NATIVE_UINT_TYPE identifier, NATIVE_UINT_TYPE &size, bool& recoverable) {
        // don't use identifier
        // heap memory is never recoverable
        recoverable = false;
        void *mem = k_malloc(size);
        if (nullptr == mem) {
            size = 0; // set to zero if can't get memory
        }
        return mem;
    }

    void ZephyrMallocAllocator::deallocate(const NATIVE_UINT_TYPE identifier, void* ptr) {
        k_free(ptr);
    }

} /* namespace Fw */
