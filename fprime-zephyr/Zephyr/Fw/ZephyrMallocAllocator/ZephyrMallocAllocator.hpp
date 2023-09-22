
#ifndef TYPES_ZEPHYRMALLOCALLOCATOR_HPP_
#define TYPES_ZEPHYRMALLOCALLOCATOR_HPP_

#include <Fw/Types/MemAllocator.hpp>

namespace Fw {

    /*!
     *
     * This class is an implementation of the MemAllocator base class.
     * It uses the zephyr main heap as the memory source.
     *
     * Since it is heap space, the identifier is unused, and memory is never recoverable.
     *
     */

    class ZephyrMallocAllocator: public MemAllocator {
        public:
            ZephyrMallocAllocator();
            virtual ~ZephyrMallocAllocator();
            //! Allocate memory
            /*!
             * \param identifier the memory segment identifier (not used)
             * \param size the requested size (not changed)
             * \param recoverable - flag to indicate the memory could be recoverable (always set to false)
             * \return the pointer to memory. Zero if unable to allocate.
             */
            void *allocate(
                    const NATIVE_UINT_TYPE identifier,
                    NATIVE_UINT_TYPE &size,
                    bool& recoverable);
            //! Deallocate memory
            /*!
             * \param identifier the memory segment identifier (not used)
             * \param ptr the pointer to memory returned by allocate()
             */
            void deallocate(
                    const NATIVE_UINT_TYPE identifier,
                    void* ptr);
    };

} /* namespace Fw */

#endif /* TYPES_ZEPHYRMALLOCALLOCATOR_HPP_ */
