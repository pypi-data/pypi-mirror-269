# Information

These files are used for the control of the LimeSDR based spectrometer.
With permission from the author Andrin Doll, the files are included in this repository.

A. Doll; Pulsed and continuous-wave magnetic resonance spectroscopy using a low-cost software-defined radio. AIP Advances 1 November 2019; 9 (11): 115110. https://doi.org/10.1063/1.5127746

## Building

The software is written in C++ and uses the LimeSuite and HDF5 libraries. The software is built using CMake.

On Debian-based systems, the following packages are required to build the software:

```
sudo apt-get install g++ cmake liblimesuite-dev libhdf5-dev
```

On Arch Linux, the following packages are required to build the software:

```
sudo pacman -S gcc cmake limesuite hdf5
```

To build the software, run the following commands in the root directory of the repository:

```
cmake -B build
cmake --build build
```

This will create an executable called `limedriver` in the `build` directory.
