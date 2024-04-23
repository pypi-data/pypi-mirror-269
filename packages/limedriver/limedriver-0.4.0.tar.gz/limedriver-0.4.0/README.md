# Python Bindings for LimeDriver

This is a Python package for the [LimeDriver](https://github.com/nqrduck/LimeDriver/) library.

## Dependencies

To build the Python bindings, you will need to have the dependencies for LimeDriver installed, as well as the Python development headers.

### Debian/Ubuntu

```bash
sudo apt-get install g++ cmake libhdf5-dev liblimesuite-dev python3-dev python3-pip python3-venv
```

### Arch Linux

```bash
sudo pacman -S gcc cmake hdf5 limesuite python python-pip
```

## Installation

It is recommended to install the Python bindings in a virtual environment. To create a new virtual environment, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
```

Ensure that the LimeDriver submodule is initialized:

```bash
git submodule update --init
```

Now, the Python bindings can be built and installed using pip:

```bash
pip install .
```

## Usage

The Python bindings provide a high-level interface to the LimeDriver library:

```python
# Import the LimeDriver module
import limedriver

# Set the number of pulses to generate
Npulses = 1000

# Create a new PyLimeConfig object
config = limedriver.PyLimeConfig(Npulses)

# Modify the config as needed
config.srate = 1e6

# Execute the config on the LimeSDR
config.run()

# Get the path to the output file
filename = config.get_path()

# Use the built-in HDF5 reader to read the output file
data = limedriver.hdf_reader.HDF(filename)
data.print_params()
```
