# <span style="color:white">Handling Engine Version Transitions</span>


A challenge we may have to tackle with our Python tools is handling multiple versions of Unreal.
We may want version-specific tool logic if the Python API has changed, or to take advantage of a new feature.
Another scenario is discovering what's been added or removed from the Unreal Python API.

This page covers the [engine](../unreal_plugin/PythonRecipeBook/Content/Python/demo/engine.py)
python module

<br>

## <span style="color:yellow">Tracking Unreal Versions</span>
<ul>

To see the current Unreal Engine version of an Editor session we can use
[get_engine_version()](https://docs.unrealengine.com/5.2/en-US/PythonAPI/class/SystemLibrary.html#unreal.SystemLibrary.get_engine_version)
:
```python
print(unreal.SystemLibrary.get_engine_version())

# Result:
    5.2.1-26001984+++UE5+Release-5.2
```
For our purposes today, we really only care about the three numbers at the start:
```python
5.2.1
```

Using this information we'll create a utility class we can use to make version-specific Python logic.

<br>


### <span style="color:orange">Saving The Version Info to a Utility Class</span>
<ul>

The version numbering used in the Unreal versions follows the 
[Semantic Versioning](https://semver.org/)
schema, which is generally presented in the order of `major.minor.patch`. For our Utility class, let's assume
the version is being provided as a string, either in the format of `"5"`, `"5.0"`, or `"5.0.0"`. We'll store
each value in a dedicated class property:

```python
class EngineVersion:
    def __init__(self, version: str):

        # convert the version ID info to a list of ints
        version_ids = version.split(".")
        version_ids = [int(i) for i in version_ids]

        # Ensure enough values are available to unpack
        version_ids.extend([0, 0])
        self.major, self.minor, self.patch = version_ids[0:3]
```
We now have a class storing our version information:
```python
engine_data = EngineVersion("5.2.1")
print(f"{engine_data.major}.{engine_data.minor}.{engine_data.patch}")

# Result:
    5.2.1
```

<br>
</ul>


### <span style="color:orange">Making the Class Version More Convenient</span>
<ul>

Now that we have our utility class, let's make it a little bit easier to print its information!

To start, let's give it a user-friendly string rep to make printouts easier:
```python
def __str__(self):
    return f"{self.major}.{self.minor}.{self.patch}"
```

Next, let's give it a computer-friendly int rep to make comparisons easier:
```python
@property
def value(self):
    return self.major*1000000 + self.minor*1000 + self.patch
```
This will let us compare engine versions using a single integer, giving us plenty of digits to work with for each component.
Using the `@property` decorator lets us call this function like a variable (no parenthesis required!). 
We'll use this property in the next section to create our tests!

<br>

another convenience, let's update the init to use the current session's version if a string isn't provided:
```python
def __init__(self, version: str = ""):
    # Get the current UE session's version if not provided
    if not version:
        version_info = str(unreal.SystemLibrary.get_engine_version())
        version = version_info.split("-", 1)[0]
    (...)
```

We can now get the current UE version and have access to both a human-friendly and computer-friendly format:
```python
engine_data =  EngineVersion()
print(engine_data)
print(engine_data.value)

# Result:
    5.2.1
    5002001
```

<br>
</ul>


### <span style="color:orange">The Comparison Functions</span>
<ul>

I like to use the
[@total_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering)
decorator when writing comparison functions for a class, this decorator is great for reducing clutter in our Python module. 
if we provide the `less than` and `equal to` functions, it will generate the rest for us. 

Using the total_ordering decorator, here's everything we need to add to our class:
```python
from functools import total_ordering

@total_ordering
class EngineVersion:
    def __lt__(self, other: 'EngineVersion') -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value
```
The `__le__`, `__gt__`, `__ge__` functions will be made automatically by the decorator.


There are some small differences in the demo Python module (mostly added validation checks),
but we now have everything we need to track and compare Engine versions:
```python
print(EngineVersion())
print(EngineVersion() > EngineVersion("5.2"))
print(EngineVersion() > EngineVersion("5.3"))

# Result:
    5.2.1
    True
    False
```

And this is generally how it would be used, gating logic specific to each UE version:
```python
if EngineVersion() >= EngineVersion("5.3"):
    # do the new 5.3 thing!
else:
    # do the old 5.2 thing!
```

<br>
</ul>
</ul>


<br>

## <span style="color:yellow">Tracking Unreal Python API changes</span>
<ul>

Another part of transitioning Unreal versions is hunting down the additions to the Python API!
While it may take some times for the [official API docs](https://docs.unrealengine.com/5.2/en-US/PythonAPI/)
to be updated, and there is a method to generate your own docs, it doesn't really list what's been freshly exposed to Python.

For this section that's what we're going to focus on: tracking what's been added to the Unreal Python classes between
two different Unreal versions. We'll first worry about saving the current session's data, then how to compare two sets
of data after. This will rely more on traditional Python logic than anything truly Unreal-specific.


### <span style="color:orange">Collecting the Current Unreal Classes/Properties</span>
<ul>

First off, we want to build a dictionary of every class under `unreal` in Python, tracking each one's properties.
This will make use of [dir()](https://docs.python.org/3/library/functions.html#dir)
and [getattr()](https://docs.python.org/3/library/functions.html#getattr) to loop over all of the data:
```python
class_data = {}
# loop over each class in unreal.*
for class_name in sorted(dir(unreal)):
    # get a handle on the class object
    class_obj = getattr(unreal, class_name)
    # get the properties of the class, ignoring any private variables
    properties = [i for i in dir(class_obj) if not i.endswith("__")]
    if properties:
        class_data[class_name] = sorted(properties)
```
</ul>


### <span style="color:orange">Saving the Data to Disk</span>
<ul>

Our next step is to save this information to disk -- to do this we'll make use of the 
[pathlib.Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) object, 
[json](https://docs.python.org/3/library/json.html), 
[get_platform_user_dir()](https://docs.unrealengine.com/5.2/en-US/PythonAPI/class/SystemLibrary.html#unreal.SystemLibrary.get_platform_user_dir),
and our EngineVersion class from earlier.

First, let's make a folder in our computer's User dir to save this data in:
```python
from pathlib import Path

data_dir = Path(unreal.SystemLibrary.get_platform_user_dir()) / "unreal/engine_python_data/"
data_dir.mkdir(exist_ok=True)
```
We now have a folder in our computer's User dir: `<user_dir>/unreal/engine_python_data/`. 
This is a cool feature of Path objects that I really like, use `/` to add any strings to the Path object's path!

Next, let's use the EngineVersion() class to help us build the full json file path:
```python
data_file = data_dir / (str(EngineVersion()).replace(".", "_") + ".json")

# Result:
    <user_dir>/unreal/engine_python_data/5_2_1.json
```

We want to avoid having `.` in the file name, so I converted them to `_` here to be computer-safe! 
And now with our file ready to go, all we need to do is open the json file and
[dump the class_data dict](https://docs.python.org/3/library/json.html#json.dump) -
This will write our Python dict data to the json file:
```python
import json

with data_file.open("w", encoding="utf-8") as f:
    json.dump(class_data, f, indent=2)
```

We now have our Python dict class data in a json file on disk!

</ul>

### <span style="color:orange">Loading the Json Data</span>
<ul>

After we've exported the Python data for our two Unreal versions (in this case 5.2.1 and 5.3), we're ready to make
a comparison script!

For this function let's make it work with our EngineVersion class and ask the user for two engine versions:
```python
def compare_unreal_python_versions(source_version: str, target_version: str):
    source = EngineVersion(source_version)
    target = EngineVersion(target_version)
```

Using the same process as earlier we'll get their file objects and load the json file data into memory:
```python
data_dir = Path(unreal.SystemLibrary.get_platform_user_dir()) / "unreal/engine_python_data/"

source_file = data_dir / (str(source).replace(".", "_") + ".json")
target_file = data_dir / (str(target).replace(".", "_") + ".json")

source_data = json.loads(source_file.read_text())
target_data = json.loads(target_file.read_text())
```
</ul>

### <span style="color:orange">Comparing the Data</span>
<ul>

To find out what's new we'll loop over the newer version and see what's missing from the older version:
```python
new_properties = {}
for class_name, properties in target_data.items():
    # If the class didn't exist in the older version we can add everything
    if class_name not in source_data:
        new_properties[class_name] = properties
    # Otherwise, check each property to see which (if any) are new
    else:
        added_properties = [p for p in properties if p not in source_data[class_name]]
        if added_properties:
            new_properties[class_name] = added_properties

# return the new class/property data
return new_properties
```

We can now print the data or further refine what we want to see. As an example, the first thing I always look for are
any classes with `System` in the name:
```python
data = compare_unreal_python_versions("5.2.1", "5.3")

for item in data:
    if "System" in item:
        print(item)
        print(json.dumps(data[item], indent=4))
```

This is provided as [collect_python_class_data()](../unreal_plugin/PythonRecipeBook/Content/Python/demo/engine.py)
in the engine module
</ul>

</ul>


# <span style="color:yellow">Summary</span>
<ul>

It might be infrequent, but having the ability to support multiple versions of a software is an excellent tool to have
in one's toolbox. Whether you're supporting multiple versions or adopting a new one, it allows that bridge to use the
same code safely in both places. And while I am constantly scouring the Unreal Engine Python docs online, having a
convenient means to find newly exposed classes & properties allows us to find interesting additions quicker that we can
dive into more later.

</ul>
