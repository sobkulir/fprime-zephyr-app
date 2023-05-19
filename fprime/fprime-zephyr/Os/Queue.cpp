#include <Os/Queue.hpp>


namespace Os {

    Queue::Queue() {}

    Queue::QueueStatus Queue::createInternal(const Fw::StringBase &name, NATIVE_INT_TYPE depth, NATIVE_INT_TYPE msgSize) {
        return QUEUE_OK;
    }

    Queue::~Queue() {
        
    }

    Queue::QueueStatus Queue::send(const U8* buffer, NATIVE_INT_TYPE size, NATIVE_INT_TYPE priority, QueueBlocking block) {
        return QUEUE_OK;
    }

    Queue::QueueStatus Queue::receive(U8* buffer, NATIVE_INT_TYPE capacity, NATIVE_INT_TYPE &actualSize, NATIVE_INT_TYPE &priority, QueueBlocking block) {
        return QUEUE_OK;
    }

    NATIVE_INT_TYPE Queue::getNumMsgs() const {
        return static_cast<U32>(0);
    }

    NATIVE_INT_TYPE Queue::getMaxMsgs() const {
        //FW_ASSERT(0);
        return 0;
    }

    NATIVE_INT_TYPE Queue::getQueueSize() const {
        return static_cast<U32>(0);
    }

    NATIVE_INT_TYPE Queue::getMsgSize() const {
        return static_cast<U32>(0);
    }

}

