# Vectovert
## Table of Contents
* [Introduction](#introduction)
* [Dependencies](#dependencies)
* [Installation](#installation)
    * Standalone
    * Vectorworks 2021
* [Usage](#usage)
    * Standalone
    * Vectorworks 2021
* [Developer: General Plugin Design](#developer-general-plugin-design)
* [Known issues](#known-issues)

<br>
<br>
<br>

# Introduction
Vectovert is a Python script that converts DXF files to SVG files. The repository includes a plugin script for Vectorworks 2021 and a standalone script for use outside of the Vectorworks interface. 

Vectovert uses *ezdxf* and *svgwrite* to parse DXF files, convert graphical DXF entities to SVG elements, inject them with custom attributes and finally write them to a SVG file. 

<br>
<br>
<br>

# Dependencies
* **Python 3.6+** 
* **ezdxf** - *tested with version 0.14.2*
* **svgwrite** - *tested with version 1.4*

<br>
<br>
<br>

# Installation
## Standalone
Installing Vectovert as a standalone involves less steps than setting it up as a plugin for Vectorworks 2021. The steps are detailed below:

1. Download this repository from GitHub (https://github.com/Manisprani/Vectovert)
2. If your system doesn't have a Python installation of version 3.6 or newer, ensure you install one!
3. Install the script dependencies *ezdxf* and *svgwrite*, for instance using: `pip install ezdxf svgwrite`

<br>

## Vectorworks 2021
Installing Vectovert as a Vectorworks plugin consists of a few more steps. Since Vectorworks includes its own Python installation, installing the dependencies is not done manually. Instead, Marionette handles this through the .vsm script. The steps are categorized and detailed below:

### Get and setup Vectovert
1. Download this repository from GitHub (https://github.com/Manisprani/Vectovert)
2. Put the .vsm script in the directory: `User\AppData\Roaming\Nemetschek\Vectorworks\2021\Plug-ins`
3. Go to Tools -> Plugins -> Script options in Vectorworks and add the downloaded Vectovert repository folder containing the `main.py` to the path.
4. Restart Vectorworks.

### Add “Convert to SVG” to the export-menu.

1. Press Tools - Workspaces - Edit Current Workspace. Two panels Commands and Menu show up. 
2. Open Import/Export in the Commands panel.
3. Open Export under File in the Menus panel. 
4. Drag “Convert to SVG” from Commands and drop it under Export in Menus.
5. Press OK.

### Install plugin dependencies

1. Navigate to and click File - Export - Convert to SVG. 
2. If this is the first time running the plugin, a command prompt will ask you to install the dependencies ezdxf and svgwrite. Press OK for both these prompts.
3. After these modules are installed, exit the plugin by pressing Cancel.
4. Restart VectorWorks. This ensures that the plugin doesn’t repeatedly ask you to install the dependencies.

<br>
<br>
<br>

# Usage
## Standalone
After ensuring your machine is running Python 3.6 or newer, and the module dependencies are installed, you can run the script through a command line as you would any Python script: `python3 vectovert_standalone.py`

Alternatively, use the provided file `vectovert.bat`, to run the command above.

<br>

## Vectorworks 2021
When the plugin has been added to the Import/Export menu, it is simply run by:

1. Navigating to the Import/Export menu and clicking Convert to SVG... 
2. A prompt will ask whether to convert the current working file, or whether to browse for an existing DXF.
3. After this, Vectorworks will prompt the user to export the file as a DXF.
4. Then, Vectorworks prompts the user to navigate to the exported DXF and choose it.
5. Finally, a prompt asks the user to start the conversion. 

Given the recursive nature of the plugin (and the size of some DWG files), the conversion might take a while!

<br>
<br>
<br>

# Developer: General Plugin Design
The plugin uses Vectorworks built-in DXF export. The generated DXF file is then used as an intermediate file format for conversion to SVG using the Python module ezdxf. Using the Vectorworks API, the file path is chosen and given to the Python script. If the script can’t identify the file as a .DXF or deems the file corrupted, it stops executing.

When SVG conversion begins, all graphical entities in the DXF are iterated over. If it is a singular entity with no children, it is added to the SVG. However, if it is an INSERT (an entity with children entities) it is first added as a SVG group, then its children are iterated over and added to that group. This is done recursively, since INSERTs can contain other INSERTs, with their own children entities.

Every added group gets an attribute code and type assigned to it, signalling its code and component type. The script works on the assumption that the DWG entities follow the naming convention points below:
* A component name starts with the character `$`
* The string following `$` is the ID of the component. <br>
**Example:** A conveyor belt could have the following name: `$A.WA01.01.004RF.RF1_1`
* A component belonging to another component drops the last dot-separated part of that component’s ID, and adds a suffix that starts with a dash (`-`) followed by the component type and ID.<br>
**Example:** A motor belonging to the conveyor belt in the point example above could have the name `$A.WA01.01.004RF-MA01_1`

In the generated SVG tags, the code attribute represents the components position - the part it belongs to, typically a conveyor. 

The component ID is parsed to determine what component type to put down the component as, according to the component ID list. This is currently represented by an incomplete, but easily extendable dictionary in [svgbuilder.py](svgbuilder.py).

So, if the motor `MA.01` is a part of the conveyor `$A.WA01.01.004RF.RF1_1`, its final SVG tag will be as follows: <br> 
``` 
<g id="$A.WA01.01.004RF-MA.01" code="$A.WA01.01.004RF" type="motor" />
``` 

<br>
<br>
<br>

# Known issues

To be listed...