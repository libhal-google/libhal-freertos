#ifndef FREERTOS_CONFIG_H
#define FREERTOS_CONFIG_H

#define configUSE_PREEMPTION 1
#define configUSE_IDLE_HOOK 0
#define configUSE_TICK_HOOK 0
/// @brief Value is ignored and is determined at runtime
#define configCPU_CLOCK_HZ ((unsigned long)100000000)
/// @brief Value is ignored and set at runtime
#define configTICK_RATE_HZ ((TickType_t)1000)

#define configMAX_PRIORITIES (5)
#define configMINIMAL_STACK_SIZE ((unsigned short)500)
#define configTOTAL_HEAP_SIZE ((size_t)(0))
#define configMAX_TASK_NAME_LEN (16)
#define configUSE_TRACE_FACILITY 1
#define configUSE_16_BIT_TICKS 0
#define configIDLE_SHOULD_YIELD 1
#define configUSE_MUTEXES 1
#define configSUPPORT_STATIC_ALLOCATION 1

/* Co-routine definitions. */
#define configUSE_CO_ROUTINES 1
#define configMAX_CO_ROUTINE_PRIORITIES (2)

/* Software timer definitions. */
#define configUSE_TIMERS 0
#define configTIMER_TASK_PRIORITY (2)
#define configTIMER_QUEUE_LENGTH 10
#define configTIMER_TASK_STACK_DEPTH (configMINIMAL_STACK_SIZE * 2)

// Include everything because the linker will handle eliminating code that is
// unused.
#define INCLUDE_vTaskPrioritySet 1
#define INCLUDE_uxTaskPriorityGet 1
#define INCLUDE_vTaskDelete 1
#define INCLUDE_vTaskCleanUpResources 1
#define INCLUDE_vTaskSuspend 1
#define INCLUDE_vTaskDelayUntil 1
#define INCLUDE_vTaskDelay 1
#define INCLUDE_uxTaskGetStackHighWaterMark 1
#define INCLUDE_xTaskGetSchedulerState 1

// Default PRIO BITS to 3 which is the default for Cortex-M processors
#define configPRIO_BITS 3 /* The lowest priority. */

/* The maximum priority an interrupt that uses an interrupt safe FreeRTOS API
function can have.  In the case of STM32F103RB Cortex-M3 this is priority 5
(which is actually represented internally by the value 192 as the Cortex-M3 uses
a sub-priority of 3). */
#define configMAX_SYSCALL_INTERRUPT_PRIORITY 5

/* The lowest interrupt priority. */
#define configLOWEST_INTERRUPT_PRIORITY 15

/* The highest user interrupt priority. */
#define configKERNEL_INTERRUPT_PRIORITY (configLOWEST_INTERRUPT_PRIORITY - 1)

/* Definitions that map the FreeRTOS port interrupt handlers to their CMSIS
standard names. */
#define vPortSVCHandler SVC_Handler
#define xPortPendSVHandler PendSV_Handler
#define xPortSysTickHandler SysTick_Handler

#endif /* FREERTOS_CONFIG_H */
