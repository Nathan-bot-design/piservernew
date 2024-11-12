cmake_minimum_required(VERSION 2.8.3)
project(ros_simple_nav)

# Find catkin dependencies
find_package(catkin REQUIRED COMPONENTS
  roscpp
  tf
  tf2
  tf2_ros
  geometry_msgs
  costmap_2d
  global_planner
)

# Declare the catkin package
catkin_package(
  INCLUDE_DIRS include
  LIBRARIES lidar_parser
  CATKIN_DEPENDS roscpp tf tf2 tf2_ros geometry_msgs costmap_2d global_planner
)

# Specify include directories
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

# Add the lidar_parser library
add_library(lidar_parser src/lidar_parser.cpp)

# Add the simple_nav executable
add_executable(simple_nav src/simple_nav.cpp)

# Link required libraries
target_link_libraries(simple_nav
  ${catkin_LIBRARIES}
  lidar_parser
  tf
  tf2
  tf2_ros
  costmap_2d
  global_planner
)


