cmake_minimum_required ( VERSION 2.8 )

project (libnfporb_interface)

set(CMAKE_CXX_FLAGS "/MD /EHsc")

set(PATH_PYTHON $ENV{PYTHONPATH}) # replace $ENV{PYTHONPATH} with absolute path to your Python installation
set(PATH_BOOST $ENV{BOOST_ROOT}) # replace $ENV{BOOST_ROOT} with absolute path to your Boost installation

link_directories(${PATH_PYTHON}/libs) 
include_directories(${PATH_BOOST})
include_directories(${PATH_PYTHON}/include)

add_library ( ${PROJECT_NAME} SHARED
	libnfporb_interface.cpp
)