# unreal-map-flipper
Unreal Map Flipper (work in progress)

1. In UnrealEd, export map to a .t3d file, run this program on it, then import the map into UnrealEd again using the "Import a new map" option.

2. Now go to Options -> Rebuild (F8)

    2A. Recommended to go to the BSP tab and set Optimization to Optimal, and the Minimize Cuts slider all the way to the left. (UnrealEd will remember this setting as long as the program is open)

    2B. Now go back to the Geometry tab and click the Rebuild Geometry button.

    2C. Then go to the Lighting tab and click the Paths Define button. (Why is this in the Lighting tab?)
    
3. If you don't have any textures that means you didn't have the original map loaded when you did the import.

4. Now you can save the map for real and load it into your game!

![image](https://github.com/Die4Ever/unreal-map-flipper/assets/30947252/e01798e4-f72e-4df9-9d1a-b7fde5ebea98)
