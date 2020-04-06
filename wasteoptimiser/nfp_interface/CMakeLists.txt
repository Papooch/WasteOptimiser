cmake_minimum_required ( VERSION 3.1 ) # za hashtagem je vsechno koment, toto pouze vynucuje verzi cmake

project (libnfporb_interface) # nazev solution souboru, dll knihovny, package, atd

set(CMAKE_CXX_FLAGS "/MD /EHsc")

link_directories($ENV{PYTHONPATH}/libs)
include_directories($ENV{BOOST_ROOT})
include_directories($ENV{PYTHONPATH}/include)

add_library ( ${PROJECT_NAME} SHARED
	libnfporb_interface.cpp
) # totok ma hodne parametru, ale by default by to melo delat sdilenou knihovnu (dll). davas tam pouze soubory s implementaci, nikoliv hlavicky