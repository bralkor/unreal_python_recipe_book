"""
This is more of a personal preference, I found myself constantly
getting the same systems and library classes so I decided to make
a module for them. This by no means every library or system,
just a few to give the idea
"""


import unreal


# Registries and Libraries
asset_registry_helper = unreal.AssetRegistryHelpers()
asset_registry        = asset_registry_helper.get_asset_registry()
EditorAssetLibrary    = unreal.EditorAssetLibrary()
ToolMenus             = unreal.ToolMenus.get()
AssetTools            = unreal.AssetToolsHelpers.get_asset_tools()

# Subsystems
AssetEditorSubsystem   = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
EditorActorSubsystem   = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
EditorUtilitySubsystem = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
LevelEditorSubsystem   = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
