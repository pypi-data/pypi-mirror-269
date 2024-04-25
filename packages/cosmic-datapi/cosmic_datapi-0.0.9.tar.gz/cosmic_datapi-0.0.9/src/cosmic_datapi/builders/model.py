from ..api import AbstractBuilder, BuiltData
from .block_state import BlockStateBuilder
import os


class AbstractModelBuilder(AbstractBuilder):
    def __init__(self, mod: "Mod", path: str, name: str):
        super().__init__(mod)
        self._path = path
        self._name = name
        self._data = {}

    def build(self) -> BuiltData:
        path = os.path.join("models", self._path, f"{self._name}.json")
        return BuiltData(path, self._data)


class BlockModelBuilder(AbstractModelBuilder):
    def __init__(self, mod: "Mod", name: str):
        super().__init__(mod, "blocks", name)
        self._data = {
            "parent": "cube",
            "textures": {}
        }

    def with_parent(self, id: str) -> "BlockModelBuilder":
        self._data["parent"] = id
        return self

    def with_texture(self, kind: str, file_name: str) -> "BlockModelBuilder":
        self._data["textures"][kind] = {
            "fileName": file_name
        }
        return self


class CuboidBuilder(AbstractBuilder):
    def __init__(self, cuboid_builder: "CuboidBlockModelBuilder"):
        super().__init__(cuboid_builder._mod)
        self._cuboid_builder = cuboid_builder
        self._data = {
            "localBounds": [0,0,0, 16,16,16],
            "faces": {}
        }

    def with_local_bounds(self, x1: int, y1: int, z1: int, x2: int, y2: int, z2: int) -> "CuboidBuilder":
        self._data["localBounds"] = [x1, y1, z2, x2, y2, z2]
        return self

    def with_face(self, name: str, texture: str, uv: list[int], ambient_occlusion: bool = True, cull_face: bool = True) -> "CuboidBuilder":
        self._data["faces"][name] = {
            "uv": uv,
            "ambientocclusion": ambient_occlusion,
            "cullFace": cull_face,
            "texture": texture
        }
        return self

    def build(self) -> "CuboidBlockModelBuilder":
        self._cuboid_builder._data["cuboids"].append(self._data)
        return self._cuboid_builder


class CuboidBlockModelBuilder(AbstractModelBuilder):
    def __init__(self, mod: "Mod", name: str):
        super().__init__(mod, "blocks", name)
        self._data = {
            "cuboids": []
        }

    def with_cuboid(self) -> CuboidBuilder:
        return CuboidBuilder(self)
