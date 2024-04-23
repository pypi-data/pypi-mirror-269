cmake_minimum_required(VERSION 3.10)  # Adjust the version as needed
project(limedriver VERSION 1.0 LANGUAGES CXX)  # Project name and version

# Find HDF5 if you're using h5c++ otherwise you can omit this part
find_package(HDF5 COMPONENTS CXX REQUIRED)

# Replace this with find_package if LimeSuite provides CMake package configuration
find_path(LIMESUITE_INCLUDE_DIR LimeSuite.h)
find_library(LIMESUITE_LIBRARY LimeSuite)

add_executable(limedriver src/limedriver.cpp)  # Define the executable and its source

target_include_directories(limedriver PRIVATE ${HDF5_INCLUDE_DIRS})  # Include dirs
target_link_libraries(limedriver PRIVATE ${HDF5_LIBRARIES} ${LIMESUITE_LIBRARY})  # Linking libraries

install(TARGETS limedriver DESTINATION bin)  # Install rule
