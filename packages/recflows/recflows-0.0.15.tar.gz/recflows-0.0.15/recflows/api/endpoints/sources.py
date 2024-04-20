# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_SOURCES

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_sources():
    return read_table(TABLE_SOURCES)


@router.post("/")
def create_source(
    source: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = source.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_SOURCES, id):
        raise HTTPException(
            status_code=428,
            detail=f'Source "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_SOURCES, source)

    return source


@router.get("/{source_id}")
def read_source(source_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_SOURCES, source_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{source_id}' not found"
        )

    return resource[0]


@router.put("/{source_id}")
def update_source(
    source_id: str = Path(...),
    source: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_SOURCES, source_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{source_id}' not found"
        )

    if source.get("id") and source["id"] != source_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{source_id}' does not match with source id '{source['id']}'"
        )

    source["id"] = source_id
    update_resouce(TABLE_SOURCES, source)

    return source


@router.delete("/{source_id}")
def delete_source(source_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_SOURCES, source_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{source_id}' not found"
        )

    print(f"DELETE FROM {TABLE_SOURCES} WHERE id = '{source_id}'")
    delete_resouce_by_id(TABLE_SOURCES, source_id)

    return resource[0]
