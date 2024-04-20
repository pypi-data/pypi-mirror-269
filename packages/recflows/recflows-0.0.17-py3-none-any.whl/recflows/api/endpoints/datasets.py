# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_DATASETS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_datasets():
    return read_table(TABLE_DATASETS)


@router.post("/")
def create_dataset(
    dataset: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = dataset.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_DATASETS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Dataset "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_DATASETS, dataset)

    return dataset


@router.get("/{dataset_id}")
def read_dataset(dataset_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_DATASETS, dataset_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{dataset_id}' not found"
        )

    return resource[0]


@router.put("/{dataset_id}")
def update_dataset(
    dataset_id: str = Path(...),
    dataset: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_DATASETS, dataset_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{dataset_id}' not found"
        )

    if dataset.get("id") and dataset["id"] != dataset_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{dataset_id}' does not match with dataset id '{dataset['id']}'"
        )

    dataset["id"] = dataset_id
    update_resouce(TABLE_DATASETS, dataset)

    return dataset


@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_DATASETS, dataset_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{dataset_id}' not found"
        )

    print(f"DELETE FROM {TABLE_DATASETS} WHERE id = '{dataset_id}'")
    delete_resouce_by_id(TABLE_DATASETS, dataset_id)

    return resource[0]
