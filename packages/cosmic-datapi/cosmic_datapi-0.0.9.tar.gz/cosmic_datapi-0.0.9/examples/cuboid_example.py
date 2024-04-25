from cosmic_datapi import Mod
from cosmic_datapi.api.actions import ActionReplaceBlockState


ID = "cuboid_example"
MOD = Mod(ID)


# This is just the vanilla cube model reimplemented with the datapi
(MOD.cuboid_block_model("cube_clone")
    .with_cuboid()
        .with_local_bounds(0, 0, 0, 16, 16, 16)
        .with_face("localNegX", "side", [0, 0, 16, 16])
        .with_face("localPosX", "side", [0, 0, 16, 16])
        .with_face("localNegY", "bottom", [0, 0, 16, 16])
        .with_face("localPosY", "top", [0, 0, 16, 16])
        .with_face("localNegZ", "side", [16, 0, 0, 16])
        .with_face("localPosZ", "side", [0, 0, 16, 16])
        .build()
    .build())


MOD.build()
