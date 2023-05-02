using UnrealBuildTool;

public class PythonRecipeBook : ModuleRules
{
	public PythonRecipeBook(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Blutility",
				"Core",
				"CoreUObject",
				"EditorSubsystem",
				"Engine",
				"PythonScriptPlugin",
				"UnrealEd",
				"UMGEditor"
			}
			);
	}
}
