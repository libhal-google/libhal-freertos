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

#include <libhal-util/serial.hpp>
#include <libhal-util/steady_clock.hpp>

#include "../hardware_map.hpp"

std::array<StackType_t, 64> stack;

void blinker(void* p_hardware_map)
{
  auto& hardware = *reinterpret_cast<hardware_map*>(p_hardware_map);

  while (true) {
    (void)hardware.led->level(true);
    vTaskDelay(500);
    (void)hardware.led->level(false);
    vTaskDelay(500);
  }
}

TaskHandle_t xHandle = NULL;
/* Structure that will hold the TCB of the task being created. */
StaticTask_t xTaskBuffer;

hal::status application(hardware_map& p_map)
{
  using namespace std::chrono_literals;
  using namespace hal::literals;

  /* Create the task without using any dynamic memory allocation. */
  xHandle = xTaskCreateStatic(
    blinker,       /* Function that implements the task. */
    "blinker",     /* Text name for the task. */
    stack.size(),  /* Number of indexes in the xStack array. */
    &p_map,        /* Parameter passed into the task. */
    4,             /* Priority at which the task is created. */
    stack.data(),  /* Array to use as the task's stack. */
    &xTaskBuffer); /* Variable to hold the task's data structure. */

  /* Start the RTOS scheduler, this function should not return as it causes the
  execution context to change from main() to one of the created tasks. */
  vTaskStartScheduler();

  return hal::success();
}
