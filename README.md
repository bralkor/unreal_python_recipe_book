<br></br>

<h2 align="center">Unreal Python Recipe Book</h2>

<p align="center">
This project explores the use of Python to interact with, manage, and extend aspects of Unreal Engine 5
</p>
<br>



<br>

## Overview

This project is meant to supplement the offical Epic documentation on Python and is
**unaffiliated** with Epic. This project is written and maintained by Brian Kortbus.
This project is meant to provide examples of how Unreal's systems can be used via Python 
and explore what's possible. This project is considered incomplete, new pages and revisions 
will be added as time allows. We will also try to update this whenever
a new version of Unreal is released, although it may not be available right away.

Please feel free to learn from and reference this project as you explore Python in Unreal!


There are two sections of this Project:
1) [Documentation](./documentation) covering various topics of using Python in Unreal
2) [An Unreal Plugin](./unreal_plugin/PythonRecipeBook) containing working code and demo material 
which may be placed in any `UE5.1` project

<br>




### The Documentation
<ul>

The [Python Documentation](./documentation) covers the Python code provided in the Unreal Plugin for various topics. 
The focus of this documentation is on working examples, it is recommended readers already be familiar with both Unreal Engine and Python.

</ul>
<br>




### The Unreal Plugin
<ul>

The provided [PythonRecipeBook](./unreal_plugin/PythonRecipeBook) plugin contains all of the code covered in the Documentation.
It may be added to any Unreal 5.1 project to demo the topics covered or review how the various parts work in practice.

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
For providing an environment where I am able to persue this personal project and supporting my desire to make it public.

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

Notable updates and additions will be logged below

</ul>
