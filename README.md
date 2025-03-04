# WasteOptimiser
This project is a part of my Master's thesis: [__Software for efficient use of material in 2D machining__](https://dspace.vutbr.cz/handle/11012/191851).

It implements a shape nesting algorithm and can be used as a GUI app, or you can use the underlying API to leverage the algorithms themselves.

-------
## Prerequisites
required dependencies: 
* Shapely library
* numpy
* pybind11 (!required as of now, even if not using libnfporb, TODO: make optional)

optional dependencies:
* PyQt5, and therefore:
    * matplotlib
* libnfporb_interface (c++), and therefore:
    * Boost library (<= 1.65),
    * cmake
    * pybind11

While the app itself is written in Python, a part of it relies on the [libnfporb library by Amir Hassan (kalabala)](https://github.com/kallaballa/libnfporb/) written in c++, which must be built before (see Building libnfporb), but it can be used without it, as there is a faster but way less accurate fallback algorithm in place.

> License notice: `libnfporb` is published under the GPL-3.0 license, so while the code in this repository is MIT-licensed, when used with `libnpforb`, it inherits the GPL-3.0 license as well.

The program also requires you to install the Shapely Python library, which is available through PyPi, but still has to be [built from source](https://github.com/Toblerity/Shapely), or the binary can be downloaded from [here (Windows only)](https://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely) and installed manually. If you use Anaconda, it can be also easily installed using `conda install shapely`.

------------
## Building libnfporb
You will need the [Boost library](https://www.boost.org/) (or at least [Boost.geometry](https://www.boost.org/doc/libs/1_65_1/libs/geometry/doc/html/index.html) that it includes) IMPORTANT! Make sure to install version <= 1.65, as there is a bug (or a fix) in Boost.geometry that breaks the libnfporb library's functionality.

If you decide to go with the recommended way, you will need to define two system environment variables: `%PYTHONPATH%` and `%BOOST_ROOT%`. 

### Visual Studio (Windows)
For Windows users, there is an auto build script provided inside `wasteoptimiser/nfp_interface`. It requires you to have cmake and Visual Studio 2017/2019 (for other versions, a slight modification of the script is needed).

In command prompt just `cd` to the `wasteoptimiser/nfp_interface` folder and then run it with `./build`. It should automatically load the Developer Command Prompt for Visual Studio. If it does not, you have to open it manually (Just start typing "Developer C..." into the search field and it should come right up, then proceed to launch the script from that). Then it will detect the Python version (64/32bit) and build the corresponding library for you.

When you see no errors in the output, you can assume the library has been correctly built and a new file named libnfporb_interface.pyd will appear in the folder.

### Other Platforms
Use `cmake` to generate the project for your favourite compiler with the `CmakeLists.txt` file provided. In the `wasteoptimiser/nfp_interface` folder, run:
``` cmd
mkdir build
cd build
cmake .. -G <your favourite generator>
```
Then, build it with your favourite compiler. After that, you need to place the build `libnfporb_interface.dll` into the `wasteoptimiser/nfp_interface` folder and rename it to `libnfporb_interface.pyd`.

--------
## Running the app
### GUI
If you have installed PyQt5 and matplotlib, you can launch the GUI from the parent folder of `wasteoptimiser` with
``` bash
# by running the module as a script
python -m wasteoptimiser
# or simply by using the provided run script
python run.py
```

![GUI](/screenshots/gui1.png)

In the _Input_ section, you can then browse to a folder with your g-codes, the parser will then try to parse each file as g-code and display the valid ones in the list. You can then select how much of each shape you want to place and whether to use the shape's convex hull as the reference (this is very much preferred for complicated shapes when using the "Use NFP" option in _Optimiser_, as it may take a loooong time to find a NFP for them).

In _Settings_ you can select the dimensions of your workspace, clearances between objects and the edge and the preferred location at which the shapes should be placed. "Small holes first" ensures that shapes are first tested for placement in the smallest regions found, before conforming to the "Preferred location" option.

In the actual _Workspace_, you can use the buttons "Add", "Subtract" and "Remove" to draw forbidden areas (i.e. holes) where the shapes cannot be placed.

In the _Optimiser_ section, you have the option to "Use NFP" (which leverages the libnfporb functionality) along with the number of rotations to test for. By disabling this option a fallback algorithm that uses the smallest enclosing circle will be used.\
The "Local optimisation" which tries to place the shape as closely to other shapes by minimising the open area around it - it can achieve better results with irregular geometry, but slows down the process a bit.\
The "Start" button starts the process of placing all the selected shapes, "Stop" can be used to stop it.

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
my_logger = logger.Logger("path/to/log", ...) # for more options see API reference
```
and then supply it to the API constructor `my_api = api.Api(logger)`.


### Quick start

First, construct the shape dictionary using (note that an absolute path is needed as of now)

``` Python
my_api.constructShapeDict("full/path/to/gcodes/")
```

This automatically parses the G-Codes from the given folder and constructs a dictionary of shapes in `my_api.shape_dict`. The keys are the file names and the values are dictionaries of the form `{'count': int, 'shape': shape, 'convex': bool}`, where `shape` is a list of polygons.

The count and whether to use the shape's convex hull (default) as its representation, can be set using

``` Python
my_api.setShapeCount('shape.gcode', 3)
my_api.setShapeConvex('shape.gcode', False)
```

The workspace with holes can be imported using
```Python
my_api.loadWorkspace('path/to/workspace.json')
```

The settings are currently a bit all over the place, but they can be set using

``` Python
my_api.optimiser.hole_offset = 5  # minimual clearance between shapes and holes
my_api.optimiser.edge_offset = 5  # minimal clearance between shapes and boundary
my_api.optimiser.preffered_pos = 1 # 0-6 (top left, top right, bottom left..)

my_api.settings.use_nfp = True # False to use smallest enclosing circle method
my_api.settings.nfp_rotations = 4 # number of shape rotations for NFP construction
my_api.settings.local_optimisation = True
```

To start the optimisation, run 
``` Python
my_api.placeAllSelectedShapes()
```
For drawing purposes, the geometry can be extracted as list of polygons
``` Python
board_polygon  = my_api.optimiser.getBoardShape()
holes_polygons = my_api.optimiser.getHoles(htype='holes')
shape_polygons = my_a0pi.optimiser.getHoles(htype='shapes')
    # without htype returns both holes and shapes as holes
```
To get the list of filenames, locations and angles for export, use
```Python
my_api.optimiser.getShapeNamesPositions()
```

---------
## API reference

The API is currently still under development and many things can change, please refer to the docstrings of functions in `wasteoptimiser/api/api.py`
