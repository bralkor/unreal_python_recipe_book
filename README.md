<br></br>

<h2 align="center">Unreal Python Recipe Book</h2>

<p align="center">
This project explores the use of Python to interact with, manage, and extend aspects of Unreal Engine 5
</p>
<br>



<br>

## Overview

This project is meant to supplement the official Epic documentation on Python and is
**unaffiliated** with Epic or any company. This project is written and maintained by Brian Kortbus.
This project is meant to provide examples of how Unreal's systems can be used via Python 
and explore what's possible. This project is considered incomplete, new pages and revisions 
will be added as time allows. We will also try to update this whenever
a new version of Unreal is released, although it may not be available right away.

Please feel free to learn from and reference this project as you explore Python in Unreal!


There are two sections of this Project:
1) [Documentation](./documentation) covering various topics of using Python in Unreal
2) [An Unreal Plugin](./unreal_plugin/PythonRecipeBook) containing working code and demo material 
which may be placed in any `UE5.2` project

<br>




### The Documentation
<ul>

The [Python Documentation](./documentation) covers the Python code provided in the Unreal Plugin for various topics. 
The focus of this documentation is on working examples, it is recommended readers already be familiar with both Unreal Engine and Python.

Currently available pages:

<table>
<tr><td>

(0) [Dev Conveniences](./documentation/00_conveniences.md)

</td><td>

Some small conveniences I've found and make use of in my own code.


</td></tr><tr><td>


(1) [Startup and Shutdown](./documentation/01_startup_and_shutdown.md)
</td><td>

How to run code at various points of Unreal's startup and shutdown sequences. 

</td></tr><tr><td>


(2) [Blueprint Function Libraries](./documentation/02_blueprint_function_libraries.md)
</td><td>

How to create Blueprint Graph function nodes in Python. This allows us far greater freedom and possibilities to call Python logic from the BP Graph.
Examples with screenshots are provided for each individual option.

</td></tr><tr><td>


(3) [Using Assets in Python](./documentation/03_using_assets_in_python.md)
</td><td>

How to interact with Content Browser assets in Python. This covers instancing, properties, and calling Blueprint functions.

</td></tr><tr><td>


(4) [Extending Menus](./documentation/04_extending_menus.md)
</td><td>

How to create and insert new menus in the Editor. This covers how to find menus, create drop down menus, and two styles of adding menu buttons.

</td></tr><tr><td>


(5) [Actor and Component Interactions](./documentation/05_actors_and_components.md)
</td><td>

How to interact with actors and components. This covers walking actor and component hierarchies as well as some basic interactions, 
such as determining the source asset of an actor.

</td></tr><tr><td>


(6) [Using Asset Metadata](./documentation/06_using_asset_metadata.md)
</td><td>

How to use and interact with Content Browser Asset metadata. This covers getting, setting, and searching for assets via metadata.

</td></tr><tr><td>


(7) [Editor Utility Widgets (EUWs) and Python](./documentation/07_editor_utility_widgets.md)
</td><td>

How to manage EUWs with Python. This covers opening and closing EUWs, managing user prefs, and a danger when using EUWs with Python.

</td></tr><tr><td>


(8) [An Editor Utility Widget Example](./documentation/08_editor_widget_example.md)
</td><td>

An example Editor Tool which makes use of Python. This tool displays arbitrary assets and allows for filtering based on their metadata values.

</td></tr><tr><td>


(9) [Making Python Blueprint Functions Safer](./documentation/09_making_python_BP_functions_safer.md)
</td><td>

Addressing the concerns mentioned on the
[Blueprint Function Libraries](./documentation/02_blueprint_function_libraries.md) and
[EUWs and Python](./documentation/07_editor_utility_widgets.md) pages,
this covers how to make Python-based Blueprint Functions safer to use.

</td></tr><tr><td>


(10) [Handling Engine Version Transitions](./documentation/10_engine_version_transitions.md)
</td><td>

Methods to handle supporting or transitioning between Unreal versions. This covers a utility
class for having version-specific Python logic as well as a method to see what classes &
properties have been added to the Unreal Python API

</td></tr>
</table>


</ul>
<br>




### The Unreal Plugin
<ul>

The provided [PythonRecipeBook](./unreal_plugin/PythonRecipeBook) plugin contains all of the code covered in the Documentation.
It may be added to any Unreal 5.2 project to demo the topics covered or review how the various parts work in practice.

The plugin contains the following:

- Python modules for all Documentation topics covered
- c++ code exposing key some useful functionality to Python
- A config ini to declare the metadata used by the the provided assets and `meta_viewer`
- An Editor Utility Widget, `meta_viewer`, to demo using Python in UMG
- A collection of arbitrary demo assets with metadata tags used by `meta_viewer`
- An arbitrary 3D level that was used to test actor/component inspection

<br>

Feel free to demo the `meta_viewer` tool in Unreal, dig into the Plugin modules, and try expanding functionality!

</ul>
<br>




### Special Thanks

<ul>

[Rajesh Sharma](https://www.linkedin.com/in/rajeshxsharma) <br>
For encouraging me to pick up this project again and keep working on it.

<br>

[Spire Animation Studios](https://spirestudios.com/) <br>
For providing an environment where I was able to pursue this project.

</ul>
<br>




### Contact

<ul>
  
This project is written and maintained by Brian Kortbus as a personal project. If you have any questions, suggestions,
or Unreal code snippets you wish to share please feel free to message me on [LinkedIn](https://www.linkedin.com/in/bkortbus/).


</ul>
<br>





### Updates

<ul>

While updates may be infrequent I do plan to add to and update this project as time allows. 
Please allow time as new versions of UE5 are released as updates may take time to publish.

---

**13 August 2023**
<ul>

- Added [documentation](./documentation/10_engine_version_transitions.md)
and [a new Python module](./unreal_plugin/PythonRecipeBook/Content/Python/demo/engine.py)
on `Handling Engine Version Transitions`

</ul>

**19 June 2023**
<ul>

- built plugin for UE5.2 and updated doc links - no notable API changes

</ul>


</ul>
