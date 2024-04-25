# Installation

## From Python Package Index
Note that because the tausworthe random number generator is a .so file the
program can currently only run on Linux systems - Windows is not supported
at the moment. The program can be installed with the following command.

```console
$ pip install ained
```

## From Source

The `ained` program uses a variety of python libraries so it is recommended that
you create a virtual environment if you don't want package conflicts.

```commandline
$ python3 -m venv .venv
```
Then activate the virtual environment:
```commandline
$ source .venv/bin/activate
```
`ained` uses the **Poetry** package to manage its dependencies. 
We need to install this in our virtual environment using
```commandline
(.venv) $ pip install poetry
```

Now clone the repository to your local machine:
```commandline
(.venv) $ git clone https://github.com/aschroede/AiNed.git
```
Change directories so you are inside the AiNed repository you just cloned
```commandline
(.venv) $ cd AiNed
```
Inside this folder there should be a `pyproject.toml` file which is a list of all
the dependencies and is what allows you to actually install ained. To install:
```commandline
(.venv) ~/Ained $ poetry install
```
You should now have poetry installed! To see how to use it, proceed to the next section. 

# Running Experiments
To run the experiments make sure you have cloned the repository to your local machine.
Navigate to the `Experiments` folder which contains a list of input files, one for each
experiment. There is also a script called `run_experiments.sh` which will process each
of the files in the `Input` directory and save the corresponding output to an `Outputs`
folder. To process the input files run the following (make sure you are in the Experiments
directory first!)
```commandline
$ ~/Experiments source run_experiments.sh
```
Note that the repository may already have Outputs that I have previously generated
inside the `Outputs` folder. You can delete this folder and regenerate it using the
above command and check that the new outputs are the same as the old ones (they should be!).
You can also add additional input files you want to test to the `Inputs` folder and
they will be processed along with all the other input files when the above script is used.




# ained Usage

**Usage**:

```console
$ ained [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate-numbers`: Generate a file with random numbers from 0...
* `gui`: Create a visual representation of the...
* `process-file`: Read in a json file (input_file) with...

## `ained generate-numbers`

Generate a file with random numbers from 0 to 100. Used for reproducible results.

**Usage**:

```console
$ ained generate-numbers [OPTIONS] COUNT FILEPATH
```

**Arguments**:

* `COUNT`: Number of random numbers to generate.  [required]
* `FILEPATH`: File to save the random numbers to.  [required]

**Options**:

* `--help`: Show this message and exit.

## `ained gui`

Create a visual representation of the dipole grid that you can interact with via a GUI.

**Usage**:

```console
$ ained gui [OPTIONS] ROWS COLUMNS
```

**Arguments**:

* `ROWS`: Number of rows of the dipole grid.  [required]
* `COLUMNS`: Number of columns of the dipole grid.  [required]

**Options**:

* `--probability FLOAT`: Strength of co-varying effect  [default: 0.7]
* `--help`: Show this message and exit.

## `ained process-file`

Read in a json file (input_file) with board properties and a series of writes. Perform each write operation
and propagate the results to neighboring bits. Save the entire history of writes and board states to (output_file)

**Usage**:

```console
$ ained process-file [OPTIONS] INPUT_FILE OUTPUT_FILE
```

**Arguments**:

* `INPUT_FILE`: File path to JSON file to process.  [required]
* `OUTPUT_FILE`: File path to save results to.  [required]

**Options**:

* `--help`: Show this message and exit.


## Fixed Point Arithmetic ##

Because this software is intended to be a functional model for simulating calculations
on an FPGA the goal was to avoid floating point arithmetic since DSPs are limited on
an FPGA. Thus the [fxpmath](https://github.com/francof2a/fxpmath)  library was used to
enforce 16-bit fixed point arithmetic. Specifically the following precision was used:

```
dtype = fxp-u16/16
Signed = False
Word bits = 16
Fract bits = 16
Int bits = 0
Val data type = <class 'float'>

Upper = 0.9999847412109375
Lower = 0.0
Precision = 1.52587890625e-05
Overflow = saturate
Rounding = trunc
Shifting = expand
```

To understand what this all means, please refer to the fxpmath library documentation.
To change the precision change this line
`DTYPE = "fxp-u16/16"` in the `fixedpoint_config.py` file.

# Running from Pycharm Terminal
## Normal Mode
Because the source code is organized into a package structure, one cannot
simply call 

```console
python3 main.py gui 7 7
```
as this will result in relative import errors. Instead you must run the following
from the root of the cloned repository (AiNed).

```console
python3 -m ained.main gui 7 7
```

The `-m` tells python to load `main` as a module inside the package `ained`
instead of loading it as a top-level script.

Similarly, you can run all the tests by doing the following:
```console
python3 -m pytest
```

## Debug Mode
If you are using Pycharm and want to run the code in debug mode, you must first
setup a debug configuration via [this tutorial](https://www.jetbrains.com/help/pycharm/run-debug-configuration.html#createExplicitly).
Inside of the *Run/Debug Configuration* dialog enter the following information

1. Select **module** and enter the module path as **ained.main**
2. In the parameters section enter the ained arguments -  for example to start the gui process with a 7 by 7 grid enter **gui 7 7**
3. Ensure the working directory is set to the root of the cloned repository (AiNed). 

Once the debug configuration is setup you should be able to select the configuration and click on the
debug icon in Pycharm to run the program in debug mode. 
