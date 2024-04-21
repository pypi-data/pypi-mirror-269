from typing import Type
from dataclasses import asdict
from sqlalchemy.orm import Session

from .common import ModelClass, ModelKeyType, PatchIgnore
from .model_api import ModelAPI
from .service_io_types import CreateModelRequest, CreateModelResponse, ListModelRequest, ListModelResponse, \
    GetModelRequest, GetModelResponse, DeleteModelRequest, DeleteModelResponse, UpdateModelRequest, UpdateModelResponse, \
    PatchModelRequest, PatchModelResponse
from .exceptions import ObjectNotFoundException

class SimpleModelAPI(ModelAPI[ModelClass, ModelKeyType]):
    model_class: Type[ModelClass]

    def __init__(self, model_class:Type[ModelClass]):
        self.model_class = model_class

    def create_model(self, db: Session, request:CreateModelRequest[ModelClass]) -> CreateModelResponse[ModelClass]:
        model = self.model_class(**asdict(request))
        db.add(model)
        db.commit()
        db.refresh(model)
        return CreateModelResponse[ModelClass](model=model)


    def list_models(self, db: Session, request:ListModelRequest[ModelClass]) -> ListModelResponse[ModelClass]:
        q = db.query(self.model_class)
        if request.skip is not None:
            q = q.offset(skip)
        if request.limit is not None:
            q = q.limit(limit)
        count = db.query(self.model_class).count()
        return ListModelResponse[ModelClass](count=count, models = q.all())

    def get_model(self, db: Session, request:GetModelRequest[ModelClass, ModelKeyType]) -> GetModelResponse[ModelClass]:
        model = db.get(self.model_class, request.id)
        if model is None:
            raise ObjectNotFoundException()
        return GetModelResponse[ModelClass](model=model)

    def update_model(self, db: Session, request:UpdateModelRequest[ModelClass, ModelKeyType]) -> UpdateModelResponse[ModelClass]:
        model = db.get(self.model_class, request.id)
        if model is None:
            raise ObjectNotFoundException()
        for field_name, field_value in asdict(request).items():
            if field_name == "id":
                continue
            setattr(model, field_name, field_value)
        db.commit()
        db.refresh(model)
        return UpdateModelResponse[ModelClass](model=model)

    def delete_model(self, db: Session, request:DeleteModelRequest[ModelClass, ModelKeyType]) -> DeleteModelResponse[ModelClass]:
        model = db.get(self.model_class, request.id)
        if model is None:
            raise ObjectNotFoundException()
        db.delete(model)
        db.commit()
        return DeleteModelResponse(model=model)

    def patch_model(self, db: Session, request:PatchModelRequest[ModelClass, ModelKeyType]) -> PatchModelResponse[ModelClass]:
        model = db.get(self.model_class, request.id)
        if model is None:
            raise ObjectNotFoundException()

        patch_fields = request.patch_fields
        for field_name, field_value in asdict(request).items():
            if field_name == "id" or field_name == "patch_fields":
                continue
            
            if field_name not in patch_fields:
                continue

            setattr(model, field_name, field_value)
        db.commit()
        db.refresh(model)
        return UpdateModelResponse[ModelClass](model=model)
