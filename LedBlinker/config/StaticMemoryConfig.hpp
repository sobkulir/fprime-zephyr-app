/*
 * StaticMemoryCfg.hpp:
 *
 * Configuration settings for the static memory component.
 */

#ifndef SVC_STATIC_MEMORY_CFG_HPP_
#define SVC_STATIC_MEMORY_CFG_HPP_

namespace Svc {
    enum StaticMemoryConfig {
        // Default is 2048B, LedBlinker only uses static buffers for buffers
        STATIC_MEMORY_ALLOCATION_SIZE = 1024
    };
}

#endif

