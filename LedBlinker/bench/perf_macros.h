#pragma once

#include <FpConfig.hpp>
#include <zephyr/kernel.h>
#include <zephyr/kernel/thread.h>

// Usage example:
// int send_data(uint8_t *data, int len) {
//     PERF_SETUP(uart_write)
    
//     PERF_MEASURE_START(uart_write)
//     for (int i = 0; i < len; ++i) {
//         uart_write(uart_dev, data, 1);
//     }
//     PERF_MEASURE_END(uart_write)

//     // Print result every 5 seconds on a 550MHz CPU.
//     PERF_PRINT(uart_write, 5 * 550 * 1000 * 1000)
// }


#if PERF_ENABLED == 0
#define PERF_SETUP(name)
#define PERF_MEASURE_START(name)
#define PERF_MEASURE_END(name)
#define PERF_PRINT(name, cycles_timeout)

#else

#define PERF_SETUP(name) static k_tid_t name##_perf_tid = k_current_get(); \
    static uint64_t name##_perf_total_used_cycles_started = 0; \
    static k_thread_runtime_stats_t name##_perf_rt_stats_all; \
    static uint64_t name##_used_cycles = 0; \
    static k_thread_runtime_stats_t name##_tid_usage; \
    uint64_t name##_measure_start_cycles = 0; \
    int name##_perf_ret = k_thread_runtime_stats_all_get(& name##_perf_rt_stats_all); \
    FW_ASSERT(name##_perf_ret == 0); \
    if (name##_perf_total_used_cycles_started == 0) { \
        name##_perf_total_used_cycles_started = name##_perf_rt_stats_all.execution_cycles; \
    }

#define PERF_MEASURE_START(name) name##_perf_ret = k_thread_runtime_stats_get(name##_perf_tid, &name##_tid_usage); \
    FW_ASSERT(name##_perf_ret == 0); \
    name##_measure_start_cycles = name##_tid_usage.execution_cycles;

#define PERF_MEASURE_END(name) name##_perf_ret = k_thread_runtime_stats_get(name##_perf_tid, & name##_tid_usage); \
    FW_ASSERT(name##_perf_ret == 0); \
    name##_used_cycles += name##_tid_usage.execution_cycles - name##_measure_start_cycles;

#define PERF_PRINT(name, cycles_timeout) \
    name##_perf_ret = k_thread_runtime_stats_all_get(&name##_perf_rt_stats_all); \
    FW_ASSERT(name##_perf_ret == 0); \
    if (name##_perf_rt_stats_all.execution_cycles - name##_perf_total_used_cycles_started > cycles_timeout) { \
        printk("Bench " #name " result: %.2f, Raw: %llu\n / %llu", 100 * (double) name##_used_cycles / (name##_perf_rt_stats_all.execution_cycles - name##_perf_total_used_cycles_started), name##_used_cycles, (name##_perf_rt_stats_all.execution_cycles - name##_perf_total_used_cycles_started)); \
        name##_used_cycles = 0; \
        name##_perf_total_used_cycles_started = name##_perf_rt_stats_all.execution_cycles; \
    }

#endif