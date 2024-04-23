from ..builders import BlockModelBuilder

_simple_block_model = lambda kind: lambda mod, name, texture: mod.block_model(name).with_texture(kind, texture)

model_top = _simple_block_model("top")
model_slab_top = _simple_block_model("slab_top")
model_bottom = _simple_block_model("bottom")
model_slab_bottom = _simple_block_model("slab_bottom")
model_side = _simple_block_model("side")
model_slab_side = _simple_block_model("slab_side")
model_all = _simple_block_model("all")
