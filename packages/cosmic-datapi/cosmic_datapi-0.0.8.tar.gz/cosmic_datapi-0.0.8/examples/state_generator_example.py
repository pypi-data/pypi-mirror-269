from cosmic_datapi import Mod


ID = "light_state_generator"
MOD = Mod(ID)


generator = MOD.block_state_generator(f"{ID}_with_light")
(generator
    .with_generator(f"{ID}:with_light_all")
    .include([
        f"{ID}:with_light_{r}_{g}_{b}"
        for r in range(0, 16)
        for g in range(0, 16)
        for b in range(0, 16)
    ])
    .build())
for r in range(0, 16):
    for g in range(0, 16):
        for b in range(0, 16):
            (generator
                .with_generator(f"{ID}:with_light_{r}_{g}_{b}")
                .with_param(f"{ID}_type_light", f"{r}_{g}_{b}")
                .with_overrides({
                    "lightLevelRed": r,
                    "lightLevelGreen": g,
                    "lightLevelBlue": b,
                })
                .build())
generator.build()


# This will override the default cheese block and add our custom block generator to it
(MOD.block("block_cheese")
    .with_state("default")
        .with_model("model_cheese")
        .with_slabs()
        .with_stairs()
        .with_state_generator(f"{ID}:with_light_all")
        .build()
    .build())


MOD.build()
