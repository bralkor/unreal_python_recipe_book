"""
Unreal will run any `init_unreal.py` files it finds during startup

Where Unreal looks for init_unreal.py files:
    1) in the project's content folder:
           `<project_dir>/Content/Python/init_unreal.py`
    2) in a plugin's content folder:
           `<plugin_dir>/Content/Python/init_unreal.py`
    3) in your computer's Documents folder:
           `Documents/UnrealEngine/Python/init_unreal.py`
    4) in any folders declared in the `UE_PYTHONPATH` environment variable
           (env variable) UE_PYTHONPATH: "D:\env_path_test\Python;"
           (init_unreal path): `D:/env_path_test/Python/init_unreal.py`

This provides us the means to deliver Python tools / libraries based on
(1) the current project, (2) the plugin(s) being used, (3) the user, and (4) the environment.

NOTE: For any folders declared in the `UE_PYTHONPATH` environment variable
      it is expecting to find the `init_unreal.py` file directly in that folder
"""
from demo import startup_shutdown

# Run the startup_shutdown setup
startup_shutdown.run()
