##############################################################
# request classes and response classes for service
##############################################################
from typing import List, Generic, Optional
from dataclasses import dataclass
from .common import ModelClass, ModelKeyType

# create
@dataclass
class CreateModelRequest(Generic[ModelClass]):
    pass

@dataclass
class CreateModelResponse(Generic[ModelClass]):
    model: ModelClass

# list
@dataclass
class ListModelRequest(Generic[ModelClass]):
    skip: Optional[int] = None
    limit: Optional[int] = None

@dataclass
class ListModelResponse(Generic[ModelClass]):
    count: int
    models: List[ModelClass]

# get
@dataclass
class GetModelRequest(Generic[ModelClass, ModelKeyType]):
    id: ModelKeyType

@dataclass
class GetModelResponse(Generic[ModelClass]):
    model: ModelClass

# delete
@dataclass
class DeleteModelRequest(Generic[ModelClass, ModelKeyType]):
    id: ModelKeyType

@dataclass
class DeleteModelResponse(Generic[ModelClass]):
    model: ModelClass

# update
@dataclass
class UpdateModelRequest(Generic[ModelClass, ModelKeyType]):
    id: ModelKeyType

@dataclass
class UpdateModelResponse(Generic[ModelClass]):
    model: ModelClass

# patch
@dataclass
class PatchModelRequest(Generic[ModelClass, ModelKeyType]):
    id: ModelKeyType
    patch_fields: List[str]

@dataclass
class PatchModelResponse(Generic[ModelClass]):
    model: ModelClass
