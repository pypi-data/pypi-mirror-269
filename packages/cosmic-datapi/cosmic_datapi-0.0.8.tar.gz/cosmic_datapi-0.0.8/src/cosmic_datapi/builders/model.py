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
