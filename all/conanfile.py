# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get, copy
from conan.errors import ConanInvalidConfiguration
from pathlib import Path
import os


required_conan_version = ">=1.50.0"
hard_coded_freertos_config = """
#define configUSE_ALTERNATIVE_API               0
#define configENABLE_BACKWARD_COMPATIBILITY     0
#define configAPPLICATION_ALLOCATED_HEAP        0

#define configSUPPORT_STATIC_ALLOCATION         1
#define configSUPPORT_DYNAMIC_ALLOCATION        1

#define configUSE_MINI_LIST_ITEM                1
#define configIDLE_SHOULD_YIELD                 1
#define configUSE_TIME_SLICING                  1

#define configUSE_QUEUE_SETS                    1
#define configUSE_MUTEXES                       1
#define configUSE_RECURSIVE_MUTEXES             1
#define configUSE_COUNTING_SEMAPHORES           1

#define INCLUDE_vTaskPrioritySet                1
#define INCLUDE_uxTaskPriorityGet               1
#define INCLUDE_vTaskDelete                     1
#define INCLUDE_vTaskSuspend                    1
#define INCLUDE_xResumeFromISR                  1
#define INCLUDE_vTaskDelayUntil                 1
#define INCLUDE_vTaskDelay                      1
#define INCLUDE_xTaskGetSchedulerState          1
#define INCLUDE_xTaskGetCurrentTaskHandle       1
#define INCLUDE_uxTaskGetStackHighWaterMark     1
#define INCLUDE_uxTaskGetStackHighWaterMark2    1
#define INCLUDE_xTaskGetIdleTaskHandle          1
#define INCLUDE_eTaskGetState                   1
#define INCLUDE_xEventGroupSetBitFromISR        1
#define INCLUDE_xTaskAbortDelay                 1
#define INCLUDE_xTaskGetHandle                  1
#define INCLUDE_xTaskResumeFromISR              1

#define configCPU_CLOCK_HZ 12000000
#define configTICK_RATE_HZ ((TickType_t)1000)

/* Cortex-M specific definitions. */
#define configPRIO_BITS 3
#define configMAX_SYSCALL_INTERRUPT_PRIORITY 5
#define configLOWEST_INTERRUPT_PRIORITY 15
#define configKERNEL_INTERRUPT_PRIORITY (configLOWEST_INTERRUPT_PRIORITY - 1)

#define vPortSVCHandler SVC_Handler
#define xPortPendSVHandler PendSV_Handler
#define xPortSysTickHandler SysTick_Handler
"""


class libhal_freertos(ConanFile):
    name = "libhal-freertos"
    license = "MIT"
    homepage = "https://www.freertos.org/"
    description = ("libhal compatible freertos package")
    topics = ("freertos", "rtos", "threads",
              "multithreading", "mulitthread", "threaded")
    settings = "os", "arch", 'compiler', 'build_type'
    generators = "CMakeDeps", "CMakeToolchain", "VirtualBuildEnv"
    exports_sources = "CMakeLists.txt"
    short_paths = True
    build_policy = "missing"
    options = {
        "FREERTOS_HEAP": [3, 4, 5],
        "configUSE_PREEMPTION": [True, False],
        "configUSE_PORT_OPTIMISED_TASK_SELECTION": [True, False],
        "configUSE_TICKLESS_IDLE": [True, False],
        "configMAX_PRIORITIES": ["ANY"],
        "configMINIMAL_STACK_SIZE": ["ANY"],
        "configMAX_TASK_NAME_LEN": ["ANY"],
        "configUSE_16_BIT_TICKS": [True, False],
        "configUSE_TASK_NOTIFICATIONS": [True, False],
        "configTASK_NOTIFICATION_ARRAY_ENTRIES": ["ANY"],
        "configQUEUE_REGISTRY_SIZE": ["ANY"],
        "configUSE_NEWLIB_REENTRANT": [True, False],
        "configNUM_THREAD_LOCAL_STORAGE_POINTERS": ["ANY"],
        "configSTACK_DEPTH_TYPE": [
            "uint8_t", "uint16_t", "uint32_t", "uint64_t", "size_t"],
        "configMESSAGE_BUFFER_LENGTH_TYPE": [
            "uint8_t", "uint16_t", "uint32_t", "uint64_t", "size_t"],
        "configHEAP_CLEAR_MEMORY_ON_FREE": [True, False],
        "configUSE_TIMERS": [True, False],

        # Memory allocation related definitions
        "configSTACK_ALLOCATION_FROM_SEPARATE_HEAP": [True, False],

        # Hook function related definitions.
        "configUSE_IDLE_HOOK": [True, False],
        "configUSE_TICK_HOOK": [True, False],
        "configCHECK_FOR_STACK_OVERFLOW": [True, False],
        "configUSE_MALLOC_FAILED_HOOK": [True, False],
        "configUSE_DAEMON_TASK_STARTUP_HOOK": [True, False],

        # Run time and task stats gathering related definitions.
        "configGENERATE_RUN_TIME_STATS": [True, False],
        "configUSE_TRACE_FACILITY": [True, False],

        # Co-routine related definitions.
        "configMAX_CO_ROUTINE_PRIORITIES": ["ANY"],

        # Software timer related definitions.
        "configTIMER_TASK_PRIORITY": ["ANY"],
        "configTIMER_QUEUE_LENGTH": ["ANY"],
        "configTIMER_TASK_STACK_DEPTH": ["ANY"],

        # FreeRTOS MPU specific definitions.
        "configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS": [True, False],
        "configTOTAL_MPU_REGIONS": ["ANY"],
        "configTEX_S_C_B_FLASH": ["ANY"],
        "configTEX_S_C_B_SRAM": ["ANY"],
        "configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY": [True, False],
        "configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS": [True, False],
        "configENABLE_ERRATA_837070_WORKAROUND": [True, False],
        "configPROTECTED_KERNEL_OBJECT_POOL_SIZE": ["ANY"],
        "configSYSTEM_CALL_STACK_SIZE": ["ANY"],

        # ARMv8-M secure side port related definitions.
        "secureconfigMAX_SECURE_CONTEXTS": ["ANY"],
    }

    default_options = {
        "FREERTOS_HEAP": 3,
        "configUSE_PREEMPTION": True,
        "configUSE_PORT_OPTIMISED_TASK_SELECTION": False,
        "configUSE_TICKLESS_IDLE": False,
        "configMAX_PRIORITIES": 5,
        "configMINIMAL_STACK_SIZE": 128,
        "configMAX_TASK_NAME_LEN": 16,
        "configUSE_16_BIT_TICKS": False,
        "configUSE_TASK_NOTIFICATIONS": True,
        "configTASK_NOTIFICATION_ARRAY_ENTRIES": 3,
        "configQUEUE_REGISTRY_SIZE": 10,
        "configUSE_NEWLIB_REENTRANT": False,
        "configNUM_THREAD_LOCAL_STORAGE_POINTERS": 16,
        "configSTACK_DEPTH_TYPE": "uint32_t",
        "configMESSAGE_BUFFER_LENGTH_TYPE": "size_t",
        "configHEAP_CLEAR_MEMORY_ON_FREE": True,
        "configUSE_TIMERS": False,

        # Memory allocation related definitions.
        "configSTACK_ALLOCATION_FROM_SEPARATE_HEAP": False,

        # Hook function related definitions.
        "configUSE_IDLE_HOOK": False,
        "configUSE_TICK_HOOK": False,
        "configCHECK_FOR_STACK_OVERFLOW": False,
        "configUSE_MALLOC_FAILED_HOOK": False,
        "configUSE_DAEMON_TASK_STARTUP_HOOK": False,

        # Run time and task stats gathering related definitions.
        "configGENERATE_RUN_TIME_STATS": False,
        "configUSE_TRACE_FACILITY": False,

        # Co-routine related definitions.
        "configMAX_CO_ROUTINE_PRIORITIES": 3,

        # Software timer related definitions.
        "configTIMER_TASK_PRIORITY": 1,
        "configTIMER_QUEUE_LENGTH": 5,
        "configTIMER_TASK_STACK_DEPTH": 256,

        # FreeRTOS MPU specific definitions.
        "configINCLUDE_APPLICATION_DEFINED_PRIVILEGED_FUNCTIONS": False,
        "configTOTAL_MPU_REGIONS": 8,
        "configTEX_S_C_B_FLASH": 0x7,
        "configTEX_S_C_B_SRAM": 0x7,
        "configENFORCE_SYSTEM_CALLS_FROM_KERNEL_ONLY": True,
        "configALLOW_UNPRIVILEGED_CRITICAL_SECTIONS": True,
        "configENABLE_ERRATA_837070_WORKAROUND": False,
        "configPROTECTED_KERNEL_OBJECT_POOL_SIZE": 10,
        "configSYSTEM_CALL_STACK_SIZE": 128,

        # ARMv8-M secure side port related definitions.
        "secureconfigMAX_SECURE_CONTEXTS": 8,
    }

    def arm_cortex_port(self, processor: str, float_abi: str):
        if processor.startswith("cortex-m0"):
            return "GCC_ARM_CM0"
        elif processor == "cortex-m3":
            return "GCC_ARM_CM3"
        elif processor == "cortex-m4" and float_abi == "soft":
            return "GCC_ARM_CM3"  # Use CM3's implementation for CM4 without FPU
        elif processor == "cortex-m4" and float_abi == "hard":
            return "GCC_ARM_CM4F"
        else:  # Add additional ports here!
            raise ConanInvalidConfiguration(
                f"The processor '{processor}' and float abi '{float_abi}' is " "not supported!")

    @property
    def freertos_port(self):
        architecture = str(self.settings.arch)
        if architecture.startswith("thumbv"):
            processor_name = str(self.settings.arch.processor)
            float_abi = self.settings.arch.get_safe('float_abi', 'soft')
            return self.arm_cortex_port(processor_name, float_abi)
        else:
            raise ConanInvalidConfiguration(
                f"The architecture '{architecture}' is not supported!")

    def macro_entry(key: str, value: int):
        return "\n#define " + key + " " + value

    def generate_freertos_config(self):
        global hard_coded_freertos_config

        keys = []
        for config in self.default_options:
            keys.append(config)

        header_file = "#ifndef FREERTOS_CONFIG_H\n" + \
            "#define FREERTOS_CONFIG_H\n"

        for key in keys:
            value = str(self.options.get_safe(key, None))

            if key == "configUSE_TIMERS" and str(value) == "True":
                header_file = header_file + \
                    "#define INCLUDE_xTimerPendFunctionCall 1"

            if str(value) == "True":
                header_file = header_file + "\n#define " + key + " 1"
            elif str(value) == "False":
                header_file = header_file + "\n#define " + key + " 0"
            else:
                header_file = header_file + "\n#define " + key + " " + value

        header_file = header_file + hard_coded_freertos_config
        header_file = header_file + """\n\n#endif /* FREERTOS_CONFIG_H */"""
        return header_file

    def source(self):
        get(self,
            **self.conan_data["sources"][self.version],
            destination="third_party/",
            strip_root=True)

    def layout(self):
        cmake_layout(self)

    def build(self):
        config_file = self.generate_freertos_config()
        print(config_file)

        freertos_include_dir = os.path.join(
            self.source_folder, "third_party/include")

        Path(os.path.join(freertos_include_dir, "FreeRTOSConfig.h")
             ).write_text(config_file)

        cmake = CMake(self)
        head_type = self.options.get_safe("FREERTOS_HEAP", 3)

        cmake.configure(variables={
            "FREERTOS_HEAP": int(str(head_type)),
            "FREERTOS_PORT": self.freertos_port,
        })

        cmake.build()

    def package(self):
        freertos_include_dir = os.path.join(
            self.source_folder, "third_party/include")
        include_dir = os.path.join(self.source_folder, "include")
        include_list_path = os.path.join(self.build_folder, "include.list")
        destination = os.path.join(self.package_folder, "include/")

        include_list = Path(include_list_path).read_text().split(";")
        # Remove all empty strings
        include_list = [i for i in include_list if i]

        for header_directory in include_list:
            copy(self, pattern="*.h", src=header_directory, dst=destination)

        copy(self, pattern="*.h", src=freertos_include_dir, dst=destination)
        copy(self, pattern="*.h", src=include_dir, dst=destination)

        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["freertos_kernel", "freertos_kernel_port"]
        self.cpp_info.set_property("cmake_target_name", "libhal::freertos")
