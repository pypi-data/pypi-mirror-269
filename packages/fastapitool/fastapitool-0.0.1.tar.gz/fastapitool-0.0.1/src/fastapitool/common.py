from typing import TypeVar
import enum

ModelClass      = TypeVar("ModelClass")
ModelKeyType    = TypeVar("ModelKeyType")

RestModelClass  = TypeVar("RestModelClass")

class PatchIgnore(enum.Enum):
    IGNORE = "IGNORE"
