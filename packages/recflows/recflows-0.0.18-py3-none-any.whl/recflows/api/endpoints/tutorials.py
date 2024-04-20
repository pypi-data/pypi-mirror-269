# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_TUTORIALS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_tutorials():
    return read_table(TABLE_TUTORIALS)


@router.post("/")
def create_tutorial(
    tutorial: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = tutorial.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_TUTORIALS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Tutorial "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_TUTORIALS, tutorial)

    return tutorial


@router.get("/{tutorial_id}")
def read_tutorial(tutorial_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_TUTORIALS, tutorial_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{tutorial_id}' not found"
        )

    return resource[0]


@router.put("/{tutorial_id}")
def update_tutorial(
    tutorial_id: str = Path(...),
    tutorial: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_TUTORIALS, tutorial_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{tutorial_id}' not found"
        )

    if tutorial.get("id") and tutorial["id"] != tutorial_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{tutorial_id}' does not match with tutorial id '{tutorial['id']}'"
        )

    tutorial["id"] = tutorial_id
    update_resouce(TABLE_TUTORIALS, tutorial)

    return tutorial


@router.delete("/{tutorial_id}")
def delete_tutorial(tutorial_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_TUTORIALS, tutorial_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{tutorial_id}' not found"
        )

    print(f"DELETE FROM {TABLE_TUTORIALS} WHERE id = '{tutorial_id}'")
    delete_resouce_by_id(TABLE_TUTORIALS, tutorial_id)

    return resource[0]
