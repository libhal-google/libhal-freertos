# Copyright 2024 Khalil Estell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

cmake_minimum_required(VERSION 3.15)

project(libhal-freertos VERSION 10.5.1 LANGUAGES C)

add_library(freertos_config INTERFACE)
target_include_directories(freertos_config SYSTEM INTERFACE include)
target_compile_definitions(freertos_config PUBLIC INTERFACE projCOVERAGE_TEST=0)

add_subdirectory("third_party")

install(TARGETS freertos_kernel)
install(TARGETS freertos_kernel_port)

# Get the directories in the include list which are almost entirely generator
# expressions for "freertos_kernel_port"
get_target_property(freertos_kernel_includes freertos_kernel
  INCLUDE_DIRECTORIES)
get_target_property(freertos_kernel_port_includes freertos_kernel_port
  INCLUDE_DIRECTORIES)

list(APPEND freertos_includes
  ${freertos_kernel_includes}
  ${freertos_kernel_port_includes})

# Save the result of the generator
file(GENERATE
  OUTPUT "include.list"
  CONTENT "${freertos_includes}")
