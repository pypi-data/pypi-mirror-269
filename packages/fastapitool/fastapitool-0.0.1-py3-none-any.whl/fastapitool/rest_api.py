import os
from fastapi import FastAPI
from typing import Generic, TypeVar, Type, Tuple, Optional, List, Callable
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .common import RestModelClass, ModelClass, ModelKeyType
from .model_api import ModelAPI
from .service_io_types import CreateModelResponse, ListModelResponse, ListModelRequest, \
    GetModelRequest, GetModelResponse, DeleteModelRequest, DeleteModelResponse, UpdateModelResponse, \
    PatchModelResponse

class RestCreateModelRequest(BaseModel, Generic[RestModelClass]):
    pass
class RestCreateModelResponse(BaseModel, Generic[RestModelClass]):
    model: RestModelClass

class RestListModelResponse(BaseModel, Generic[RestModelClass]):
    models: List[RestModelClass]

class RestGetModelResponse(BaseModel, Generic[RestModelClass]):
    model: RestModelClass

class RestDeleteModelResponse(BaseModel, Generic[RestModelClass]):
    model: RestModelClass

class RestUpdateModelRequest(BaseModel, Generic[RestModelClass]):
    pass
class RestUpdateModelResponse(BaseModel, Generic[RestModelClass]):
    model: RestModelClass

class RestPatchModelRequest(BaseModel, Generic[RestModelClass]):
    patch_fields: List[str]
class RestPatchModelResponse(BaseModel, Generic[RestModelClass]):
    model: RestModelClass

class SimpleRestAPI(Generic[ModelClass, RestModelClass, ModelKeyType]):
    label: str
    db_factory: Callable[[], Session]
    model_api: ModelAPI[ModelClass, ModelKeyType]
    t_create: Tuple[
        Type[RestCreateModelRequest[RestModelClass]], 
        Type[RestCreateModelResponse[RestModelClass]]
    ]
    t_list: Type[RestListModelResponse[RestModelClass]]
    t_get: Type[RestGetModelResponse[RestModelClass]]
    t_delete: Type[RestDeleteModelResponse[RestModelClass]]
    t_update: Tuple[
        Type[RestUpdateModelRequest[RestModelClass]], 
        Type[RestUpdateModelResponse[RestModelClass]]
    ]
    t_patch: Tuple[
        Type[RestPatchModelRequest[RestModelClass]], 
        Type[RestPatchModelResponse[RestModelClass]]
    ]
    base_url:str

    def __init__(self, 
        label:      str, 
        db_factory: Callable[[], Session],
        model_api:  ModelAPI[ModelClass, ModelKeyType],
        t_create:   Tuple[
            Type[RestCreateModelRequest[RestModelClass]], 
            Type[RestCreateModelResponse[RestModelClass]]
        ],
        t_list:     Type[RestListModelResponse[RestModelClass]],
        t_get:      Type[RestGetModelResponse[RestModelClass]],
        t_delete:   Type[RestDeleteModelResponse[RestModelClass]],
        t_update:   Tuple[
            Type[RestUpdateModelRequest[RestModelClass]], 
            Type[RestUpdateModelResponse[RestModelClass]]
        ],
        t_patch: Tuple[
            Type[RestPatchModelRequest[RestModelClass]], 
            Type[RestPatchModelResponse[RestModelClass]]
        ],
        base_url: str
    ):
        self.label = label
        self.db_factory = db_factory
        self.model_api = model_api
        self.t_create = t_create
        self.t_list = t_list
        self.t_get = t_get
        self.t_delete = t_delete
        self.t_update = t_update
        self.t_patch = t_patch
        self.base_url = base_url
    

    def register(self, app: FastAPI):
        base_url = os.path.join(self.base_url, f"{self.label}s/")
        tag = [ f"{self.label}s" ]

        def create_model(request:RestCreateModelRequest[RestModelClass]) -> CreateModelResponse[ModelClass]:
            with self.db_factory() as db:
                return self.model_api.create_model(db, model_api.CreateModelRequest(**request.dict()))
        create_model.__annotations__["request"] = self.t_create[0]

        def list_models(skip:Optional[int]=None, limit:Optional[int]=None) -> ListModelResponse[ModelClass]:
            with self.db_factory() as db:
                return self.model_api.list_models(db, ListModelRequest(skip=skip, limit=limit))
        
        def get_model(id: ModelKeyType) -> GetModelResponse[ModelClass]:
            with self.db_factory() as db:
                return self.model_api.get_model(db, GetModelRequest(id=id))

        def delete_model(id: ModelKeyType) -> DeleteModelResponse[ModelClass]:
            with self.db_factory() as db:
                return self.model_api.delete_model(db, DeleteModelRequest(id=id))

        def update_model(id: ModelKeyType, request:RestUpdateModelRequest) -> UpdateModelResponse[ModelClass]:
            with self.db_factory() as db:
                service_request = model_api.UpdateModelRequest(
                    id = id, **request.dict()
                )
                return self.model_api.update_model(db, service_request)
        update_model.__annotations__["request"] = self.t_update[0]

        def patch_model(id: ModelKeyType, request:RestPatchModelRequest) -> PatchModelResponse[ModelClass]:
            with self.db_factory() as db:
                service_request = model_api.PatchModelRequest(
                    id = id, **request.dict()
                )
                return self.model_api.patch_model(db, service_request)
        patch_model.__annotations__["request"] = self.t_patch[0]

        app.post(
            self.base_url,
            response_model = self.t_create[1],
            tags = tag,
            summary     = f"Create a new {self.label}",
            description = f"Create a new {self.label}"
        )(create_model)

        app.get(
            self.base_url, 
            response_model = self.t_list,
            tags = tag,
            summary     = f"Retrieve {self.label}s",
            description = f"Retrieve {self.label}s"
        )(list_models)

        app.get(
            os.path.join(self.base_url, "{id}"), 
            response_model = self.t_get,
            tags = tag,
            summary     = f"Retrieve a {self.label} by id",
            description = f"Retrieve a {self.label} by id"
        )(get_model)

        app.delete(
            os.path.join(self.base_url, "{id}"), 
            response_model = self.t_delete,
            tags = tag,
            summary = f"Delete a {self.label} by id", 
            description = f"Delete a {self.label} by id"
        )(delete_model)

        app.put(
            os.path.join(self.base_url, "{id}"), 
            response_model=self.t_update[1],
            tags = tag,
            summary = f"Update a {self.label} by id",
            description = f"Update a {self.label} by id"
        )(update_model)

        app.patch(
            os.path.join(self.base_url, "{id}"), 
            response_model=self.t_patch[1],
            tags = tag,
            summary = f"Patch a {self.label} by id",
            description = f"Patch a {self.label} by id"
        )(patch_model)
