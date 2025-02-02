<br></br>

![](resources/banner.PNG)

<h2 align="center">Unreal Python Recipe Book</h2>

<p align="center">
This project explores the use of Python to interact with, manage, and extend aspects of Unreal Engine 5
<br>
For the web documentation, please visit:
<br>
<a href="https://bkortbus.gitbook.io/unreal-python-recipe-book">bkortbus.gitbook.io/unreal-python-recipe-book</a>
</p>


## Overview

This project is meant to supplement the official Epic documentation on Python and is unaffiliated with Epic 
or any other company. This project is written and maintained by Brian Kortbus. This project is meant to provide 
examples of how Unreal's systems can be used via Python and explore what's possible. This project is considered 
incomplete, new pages and revisions will be added as time allows.


There are two sections of this Project:
1) [Documentation](https://bkortbus.gitbook.io/unreal-python-recipe-book) - available on GitBook, 
the Python Documentation covers a wide assortment of Unreal Python features

2) [Unreal Demo Plugin](./unreal_plugin/PythonRecipeBook) - available here on GitHub,
the Unreal Plugin provides samples on the code covered in the documentation

<br>


### The Unreal Plugin
<ul>

The provided [PythonRecipeBook](./unreal_plugin/PythonRecipeBook) plugin contains example code covered in the Documentation.
It may be added to any Unreal 5.3 project to demo the topics covered or review how the various parts work in practice.

The plugin contains the following:
- Python modules for all Documentation topics covered
- c++ code exposing key some useful functionality to Python
- A Python startup script
- An Editor Utility Widget, `meta_viewer`, to demo using Python in UMG
- A collection of arbitrary demo assets with metadata tags used by `meta_viewer`
- An arbitrary 3D level that was used to test actor/component inspection

<br>

Feel free to demo the `meta_viewer` tool in Unreal, dig into the Plugin modules, and try expanding functionality!

</ul>
<br>


### Contact

<ul>
  
This project is written and maintained by Brian Kortbus as a personal project. 
If you have any questions, suggestions, or Unreal code snippets you wish to share please 
feel free to message me on [LinkedIn](https://www.linkedin.com/in/bkortbus/).

</ul>
<br>