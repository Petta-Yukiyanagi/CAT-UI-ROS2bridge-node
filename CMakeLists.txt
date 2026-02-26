cmake_minimum_required(VERSION 3.8)
project(catui_bridge)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CatUICommand.msg"
  DEPENDENCIES builtin_interfaces
)

install(PROGRAMS
  catui_bridge/ui_bridge_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()