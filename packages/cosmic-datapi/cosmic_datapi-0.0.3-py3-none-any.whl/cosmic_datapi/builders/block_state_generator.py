from ..api import AbstractBuilder, BuiltData
from ..api.actions import AbstractAction
from typing import Any, overload
import os


class BlockStateSubgeneratorBuilder(AbstractBuilder):
    def __init__(self, mod: "Mod", name: str, state_generator: "BlockStateGeneratorBuilder"):
        super().__init__(mod)
        self._name = name
        self._state_gen = state_generator
        self._data = {
            "stringId": self._name,
        }

    @overload
    def include(self, id: str) -> "BlockStateSubgeneratorBuilder":
        ...

    @overload
    def include(self, id: list[str]) -> "BlockStateSubgeneratorBuilder":
        ...

    def include(self, id) -> "BlockStateSubgeneratorBuilder":
        if "include" not in self._data:
            self._data["include"] = []

        if type(id) == list:
            self._data["include"].extend(id)
        elif type(id) == str:
            self._data["include"].append(id)

        return self

    def with_model(self, id: str) -> "BlockStateSubgeneratorBuilder":
        self._data["modelName"] = id
        return self

    def with_param(self, key: str, value: Any) -> "BlockStateSubgeneratorBuilder":
        if "params" not in self._data:
            self._data["params"] = {}
        self._data["params"][key] = value
        return self

    def with_params(self, params: dict) -> "BlockStateSubgeneratorBuilder":
        for k, v in self.params.items():
            self.with_param(k, b)
        return self

    def with_override(self, key: str, value: Any) -> "BlockStateSubgeneratorBuilder":
        if "overrides" not in self._data:
            self._data["overrides"] = {}
        self._data["overrides"][key] = value
        return self

    def with_overrides(self, overrides: dict) -> "BlockStateSubgeneratorBuilder":
        for k, v in overrides.items():
            self.with_override(k, v)
        return self

    def build(self) -> "BlockStateGeneratorBuilder":
        if "params" not in self._data and "include" not in self._data:
            print(f"error: block state generator must have params or include another generator (in {self._mod.namespace}:{self._state_gen._name}#{self._name})")
            exit(1)
        self._state_gen._data["generators"].append(self._data)
        return self._state_gen


class BlockStateGeneratorBuilder(AbstractBuilder):
    def __init__(self, mod: "Mod", name: str):
        super().__init__(mod)
        self._name = name
        self._data = {
            "generators": []
        }

    def with_generator(self, id: str) -> BlockStateSubgeneratorBuilder:
        return BlockStateSubgeneratorBuilder(self._mod, id, self)

    def build(self) -> BuiltData:
        path = os.path.join("block_state_generators", f"{self._name}.json")
        return BuiltData(path, self._data)
