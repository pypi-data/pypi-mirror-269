from typing import Generic
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from .common import ModelClass, ModelKeyType

from .service_io_types import CreateModelRequest, CreateModelResponse, ListModelRequest, ListModelResponse, \
    GetModelRequest, GetModelResponse, DeleteModelRequest, DeleteModelResponse, UpdateModelRequest, UpdateModelResponse,\
    PatchModelRequest, PatchModelResponse

class ModelAPI(Generic[ModelClass, ModelKeyType], ABC):
    @abstractmethod
    def create_model(self, db: Session, request:CreateModelRequest[ModelClass]) -> CreateModelResponse[ModelClass]:
        pass

    @abstractmethod
    def list_models(self, db: Session, request:ListModelRequest[ModelClass]) -> ListModelResponse[ModelClass]:
        pass

    @abstractmethod
    def get_model(self, db: Session, request:GetModelRequest[ModelClass, ModelKeyType]) -> GetModelResponse[ModelClass]:
        pass

    @abstractmethod
    def update_model(self, db: Session, request:UpdateModelRequest[ModelClass, ModelKeyType]) -> UpdateModelResponse[ModelClass]:
        pass

    @abstractmethod
    def delete_model(self, db: Session, request:DeleteModelRequest[ModelClass, ModelKeyType]) -> DeleteModelResponse[ModelClass]:
        pass

    @abstractmethod
    def patch_model(self, db: Session, request:PatchModelRequest[ModelClass, ModelKeyType]) -> PatchModelResponse[ModelClass]:
        pass

