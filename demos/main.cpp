// Copyright 2023 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <FreeRTOS.h>
#include <task.h>

#include "hardware_map.hpp"
#include <libhal-util/steady_clock.hpp>

int main()
{
  using namespace std::literals;

  auto processor_status = initialize_processor();

  if (!processor_status) {
    hal::halt();
  }

  auto platform_status = initialize_platform();

  if (!platform_status) {
    hal::halt();
  }

  static auto hardware_map = platform_status.value();
  auto is_finished = application(hardware_map);

  if (!is_finished) {
    hardware_map.reset();
  } else {
    hal::halt();
  }

  return 0;
}

namespace boost {
void throw_exception([[maybe_unused]] std::exception const& e)
{
  hal::halt();
}
}  // namespace boost

extern "C"
{
  /* configSUPPORT_STATIC_ALLOCATION is set to 1, so the application must
  provide an implementation of vApplicationGetIdleTaskMemory() to provide the
  memory that is used by the Idle task. */
  void vApplicationGetIdleTaskMemory(StaticTask_t** ppxIdleTaskTCBBuffer,
                                     StackType_t** ppxIdleTaskStackBuffer,
                                     uint32_t* pulIdleTaskStackSize)
  {
    /* If the buffers to be provided to the Idle task are declared inside this
    function then they must be declared static - otherwise they will be
    allocated on the stack and so not exists after this function exits. */
    static StaticTask_t xIdleTaskTCB;
    static StackType_t uxIdleTaskStack[500];

    /* Pass out a pointer to the StaticTask_t structure in which the Idle task's
    state will be stored. */
    *ppxIdleTaskTCBBuffer = &xIdleTaskTCB;

    /* Pass out the array that will be used as the Idle task's stack. */
    *ppxIdleTaskStackBuffer = uxIdleTaskStack;

    /* Pass out the size of the array pointed to by *ppxIdleTaskStackBuffer.
    Note that, as the array is necessarily of type StackType_t,
    500 is specified in words, not bytes. */
    *pulIdleTaskStackSize = 500;
  }
  /*-----------------------------------------------------------*/

  /* configSUPPORT_STATIC_ALLOCATION and configUSE_TIMERS are both set to 1, so
  the application must provide an implementation of
  vApplicationGetTimerTaskMemory() to provide the memory that is used by the
  Timer service task. */
  void vApplicationGetTimerTaskMemory(StaticTask_t** ppxTimerTaskTCBBuffer,
                                      StackType_t** ppxTimerTaskStackBuffer,
                                      uint32_t* pulTimerTaskStackSize)
  {
    /* If the buffers to be provided to the Timer task are declared inside this
    function then they must be declared static - otherwise they will be
    allocated on the stack and so not exists after this function exits. */
    static StaticTask_t xTimerTaskTCB;
    static StackType_t uxTimerTaskStack[500];

    /* Pass out a pointer to the StaticTask_t structure in which the Timer
    task's state will be stored. */
    *ppxTimerTaskTCBBuffer = &xTimerTaskTCB;

    /* Pass out the array that will be used as the Timer task's stack. */
    *ppxTimerTaskStackBuffer = uxTimerTaskStack;

    /* Pass out the size of the array pointed to by *ppxTimerTaskStackBuffer.
    Note that, as the array is necessarily of type StackType_t,
    1000 is specified in words, not bytes. */
    *pulTimerTaskStackSize = 1000;
  }
}
