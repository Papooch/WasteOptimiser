@echo off

mkdir build
cd build
cmake .. -G "Visual Studio 15 2017 Win64" -DCMAKE_SYSTEM_VERSION=10.0.17763.0
devenv libnfporb_interface.sln /Build Release /Project libnfporb_interface
cd ..
mv -f build/Release/libnfporb_interface.dll libnfporb_interface.pyd
pause