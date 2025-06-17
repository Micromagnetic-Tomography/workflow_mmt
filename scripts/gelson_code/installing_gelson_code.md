## Setting up your environment

You'll need a working Python 3 environment with all the standard
scientific packages installed (numpy, pandas, scipy, matplotlib, etc).
This will give you access to a Python 3 environment and the excellent `conda`
package manager (a drop-in replacement for `conda`).

Besides the standard scientific packages, you'll also need to install some
extra libraries like: Numba for just-in-time compilation; Harmonica, Verde,
Boule and Pooch from the [Fatiando a Terra](https://www.fatiando.org) project;
PyGMT for generating maps and more.

Instead of manually installing them, they can all be automatically installed
using a conda environment.

1. Inside the cloned repository (or an unzipped version), create a new virtual
   environment from the `environment.yml` file by running:
   ```
   conda env create -f environment.yml
   ```
2. Check the environment name in the `environment.yml` file.
3. Activate the new environment by running:
   ```
   conda activate ENVIRONMENT_NAME
   ```