@echo off

rem check if run from Develope console, try to launch it if not
WHERE devenv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    rem Check for VS 2017
    if exist "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat" (
        call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\Common7\Tools\VsDevCmd.bat" >nul
        set vsver=2017
    )
    rem Check for VS 2019
    if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat" (
        call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\Tools\VsDevCmd.bat" >nul
        set vsver=2019
    )
)

rem 
where devenv >nul 2>nul
if %ERRORLEVEL% neq 0 (
	echo Developer command prompt for Visual Studio 2017 or 2019 could not be found or started, please launch this script manually from it.
	echo.
    echo If you use a different version, please refer to README.md for manual installation.
    goto error
)

set skip=%1

if "%skip%"=="-m" (
	echo Skipping path check...
	goto no_path_check
)

set err=0
if not defined PYTHONPATH (
	echo The %%PYTHONPATH%% environment variable is not set
	set err=1
)
if not defined BOOST_ROOT (
	echo The %%BOOST_ROOT%% environment variable is not set
	set err=1
)
if "%err%"=="1" (
    goto err_path
)
:no_path_check

WHERE python >nul 2>nul
if %ERRORLEVEL% neq 0 (
	echo The python.exe executable not found
	goto error
)

REM Get python version (32bit/64bit)
for /f "tokens=*" %%i in ('python -c "import platform; print(platform.architecture()[0])"') do set arch=%%i

set pyarch2017=
set pyarch2019=
if "%arch%"=="64bit" (
	set pyarch2017= Win64
    set pyarch2019= -A x64
    echo Your Python installation is 64bit, Visual Studio %vsver%
) else (
    echo Your Python installation is 32bit, Visual Studio %vsver%
)


if "%vsver%"=="2017" (
    set cmakegen="Visual Studio 15 2017%pyarch2017%"
) else (
    set cmakegen="Visual Studio 16 2019"%pyarch2019%
)

mkdir build
cd build
cmake .. -G %cmakegen% -DCMAKE_SYSTEM_VERSION=10.0
devenv libnfporb_interface.sln /Build Release /Project libnfporb_interface
cd ..
mv -f build/Release/libnfporb_interface.dll libnfporb_interface.pyd

pause
exit /b
:err_path
echo.
echo If you wish to set Python and Boost folders manually, please edit the CMakeLists.txt file:
echo Replace $ENV{PYTHONPATH} and $ENV{BOOST_ROOT} with absolute paths to your python and boost installation
echo and run this script with The -m flag.
echo.
:error
echo Project not built due to errors
echo.
pause