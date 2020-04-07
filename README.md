BIG TODO:

WasteOptimiser
--------------

This project is a part of a Master's thesis TODO: (link)

It implements a shape nesting algorithms. It can be used as a GUI app, or you can use the underlying API to leverage the algorithms themselves.

Prerequisites
-------------
required: Shapely library (python)
optional: libnfporb_interface (c++), and therefore: Boost library, cmake


While the app itself is written in Python, a part of it relies on the libnfporb library by kalabala TODO: (link) written in c++, which must be built before (see Building libnfporb), but it can be used without it, as there is a faster but way less accurate fallback algorithm in place.

The program also requires you to install the Shapely python library, which is not available through PyPi, but has to be either built from source TODO: (link) or downloaded from here (Windows only) TODO: (link) and installed manually.

Building libnfporb
------------------
For Windows users, there is a build script provided inside wasteoptimiser/nfp_interface. It requires you to have cmake and Visual Studio 2017 (for other versions, a slight modification of the script is needed). You will also need the boost library (or at least the TODO: and TODO: that it includes). If you decide to go with the recommended way, you will need to define two environment variables: %PYTHONPATH% and %BOOST_ROOT%. You have to run the script through the Developer Command Prompt for Visual Studio and select which version of Python (32/64 bit) you use. When you see no errors in the output, you can assume the library has been correctly built and a new file named libnfporb_interface.pyd will appear in the folder.