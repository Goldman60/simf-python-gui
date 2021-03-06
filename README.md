# Solar Irradiance Microforecasting Control Panel

A QT and Python3 based graphical control panel for the Lepton-Grabber

## Installation

The application can be installed from pypi using pip:

    pip install SimfPythonGUI
    
On some systems you may need to specify Python 3's version of pip:

    pip3 install SimfPythonGUI
    
Package information can be found on the 
[pypi package page](https://pypi.org/project/SimfPythonGUI/) for the project.

### Dependencies

Dependencies should be managed automatically when installed with pip, but they
are provided here for reference:

* Python3
* PyQT5
* watchdog

The program relies on the following system utilities being installed or
suitably compatible replacements (configure the replacements using the
configuration menu):

* bash
* sudo

## Usage

The gui can be launched from the command line assuming your python package
path is set up properly using the command:

    simfgui

A configuration file is written by default to `~/.simfgui.ini`.  Running the
utility will require sudo permissions

## Contributing and Editing

The repository contains the files for editing with the JetBrains PyCharm IDE.
The .ui files can be editied with QT Designer (they were created using QT
Designer 5.11).  QT Designer can be obtained from the QT website or your
favorite package manager.

### Source Code

The code is hosted online in two locations and accepting pull requests:

* [Primary](https://git.nclf.net/SIMF/simf-python-gui)
* [Mirror (GitHub)](https://github.com/Goldman60/simf-python-gui)

## Questions, comments, issues?

Please use the contact information on [my website](https://ajfite.com).  For
my most recent contact info, I'm happy to help even though by the time you're 
reading this I'm long graduated, just shoot me an email.