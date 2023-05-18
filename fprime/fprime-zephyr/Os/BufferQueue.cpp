#include <FpConfig.hpp>

#include <Os/Pthreads/BufferQueue.hpp>

namespace Os {

    bool BufferQueue::initialize(NATIVE_UINT_TYPE depth, NATIVE_UINT_TYPE msgSize) {
        return true;
    }

    bool BufferQueue::enqueue(const U8* buffer, NATIVE_UINT_TYPE size, NATIVE_INT_TYPE priority) {
        return true;
    }
    bool BufferQueue::dequeue(U8* buffer, NATIVE_UINT_TYPE& size, NATIVE_INT_TYPE &priority) {
        return true;
    }

    void BufferQueue::finalize() {}

}
