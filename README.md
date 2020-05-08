BIG TODO:

# WasteOptimiser
This project is a part of a Master's thesis TODO: (link)

It implements a shape nesting algorithm. It can be used as a GUI app, or you can use the underlying API to leverage the algorithms themselves.

## Prerequisites
required dependencies: 
* Shapely library
* numpy

optional dependencies:
* PyQt5, and therefore:
    * matplotlib
* libnfporb_interface (c++), and therefore:
    * Boost library (<= 1.65),
    * cmake

While the app itself is written in Python, a part of it relies on the libnfporb library by Amir Hasan (kalabala) TODO: (link) written in c++, which must be built before (see Building libnfporb), but it can be used without it, as there is a faster but way less accurate fallback algorithm in place.

The program also requires you to install the Shapely python library, which is not available through PyPi, but has to be either built from source TODO: (link) or downloaded from here (Windows only) TODO: (link) and installed manually. If you use Anaconda, it can be also easily installed using `conda install shapely`.

## Building libnfporb
You will need the boost library (or at least the TODO: and TODO: that it includes) IMPORTANT! Make sure to install version <= 1.65, as there is a bug (or a fix) in boost.geometry that breaks the libnfporb library's functionality.

If you decide to go with the recommended way, you will need to define two system environment variables: `%PYTHONPATH%` and `%BOOST_ROOT%`. 

### Visual Studio (Windows)
For Windows users, there is an auto build script provided inside `wasteoptimiser/nfp_interface`. It requires you to have cmake and Visual Studio 2017/2019 (for other versions, a slight modification of the script is needed).

In command prompt just `cd` to the `wasteoptimiser/nfp_interface` folder and then run it with `./build`. It should automatically load the Developer Command Prompt for Visual Studio. If it does not, you have to open it manually (Just start typing "Developer C..." into the search field and it should come right up, then proceed to launch the script from that). Then it will detect the Python version (64/32bit) and build the corresponding library for you.

When you see no errors in the output, you can assume the library has been correctly built and a new file named libnfporb_interface.pyd will appear in the folder.

### Other Platforms
Use `cmake` to generate the project for your favourite compiler with the `CmakeLists.txt` file provided. In the `wasteoptimiser/nfp_interface` folder, run:
```
mkdir build
cd build
cmake .. -G <your favourite generator>
```
Then, build it with your favourite compiler. After that, you need to place the build `libnfporb_interface.dll` into the `wasteoptimiser/nfp_interface` folder and rename it to `libnfporb_interface.pyd`.

## Running the app
### GUI
If you have installed PyQt5 and matplotlib, you can launch the GUI from the parent folder of `wasteoptimiser` with
```
python -m wasteoptimiser
```
In the _Input_ section, you can then browse to a folder with your g-codes, the parser will then try to parse each file as g-code and display the valid ones in the list. You can then select how much of each shape you want to place and whether to use the shape's convex hull as the reference (this is very much preferred for complicated shapes when using the "Use NFP" option in _optimiser_, as it may take a loooong time to find a NFP for them).

In _Settings_ you can select the dimensions of your workspace, clearances between objects and the edge and the preferred location at which the shapes should be placed. (TODO: Add options like "sharpest corner" and "closest to existing geometry", also put this in _Optimiser_)
"Small holes first" ensures that shapes are first tested for placement in the smallest regions found, before conforming to the "Preferred location" option.

In the actual _Workspace_, you can use the buttons "Add", "Subtract" and "Remove" to draw forbidden areas (i.e. holes) where the shapes cannot be placed.

In the _Optimiser_ section, you have the option to "Use NFP" (which leverages the libnfporb functionality) along with the number of rotations to test for. By disabling this option a fallback algorithm that uses the smallest enclosing circle will be used.\
The "Local optimisation" which tries to place the shape as closely to other shapes by minimising the open area around it - it can achieve better results with irregular geometry, but slows down the process a bit.\
The "Start" button starts the process of placing all the selected shapes, "Stop" can be used to stop it. The other buttons do nothing as of now (TODO: make them do something!)

The top menu item "Workspace" lets you import and export created workspaces.

### API
If you only need to use the API, import it in your Python script:
``` Python
from wasteoptimiser.api import api
```
Then, you can create an instance of it with
``` Python
my_api = api.Api()
```
By default, all the log messages will be printed to the console, if you want, you can use the built-in logger where you can select the logging and printing level (e.g. do not print debug messages and stuff).
``` Python
from wasteoptimiser.logger import logger
my_logger = logger.Logger("path/to/log", ...) # for more options TODO: see section Logger
```
and then supply it to the API constructor `my_api = api.Api(logger)`.


## API reference
TODO: API refference
