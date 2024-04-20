# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_MODELS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_models():
    return read_table(TABLE_MODELS)


@router.post("/")
def create_model(
    model: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = model.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_MODELS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Model "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_MODELS, model)

    return model


@router.get("/{model_id}")
def read_model(model_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_MODELS, model_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{model_id}' not found"
        )

    return resource[0]


@router.put("/{model_id}")
def update_model(
    model_id: str = Path(...),
    model: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_MODELS, model_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{model_id}' not found"
        )

    if model.get("id") and model["id"] != model_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{model_id}' does not match with model id '{model['id']}'"
        )

    model["id"] = model_id
    update_resouce(TABLE_MODELS, model)

    return model


@router.delete("/{model_id}")
def delete_model(model_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_MODELS, model_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{model_id}' not found"
        )

    print(f"DELETE FROM {TABLE_MODELS} WHERE id = '{model_id}'")
    delete_resouce_by_id(TABLE_MODELS, model_id)

    return resource[0]
