# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_RECOMMENDERS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_recommenders():
    return read_table(TABLE_RECOMMENDERS)


@router.post("/")
def create_recommender(
    recommender: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = recommender.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_RECOMMENDERS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Recommender "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_RECOMMENDERS, recommender)

    return recommender


@router.get("/{recommender_id}")
def read_recommender(recommender_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_RECOMMENDERS, recommender_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{recommender_id}' not found"
        )

    return resource[0]


@router.put("/{recommender_id}")
def update_recommender(
    recommender_id: str = Path(...),
    recommender: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_RECOMMENDERS, recommender_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{recommender_id}' not found"
        )

    if recommender.get("id") and recommender["id"] != recommender_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{recommender_id}' does not match with recommender id '{recommender['id']}'"
        )

    recommender["id"] = recommender_id
    update_resouce(TABLE_RECOMMENDERS, recommender)

    return recommender


@router.delete("/{recommender_id}")
def delete_recommender(recommender_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_RECOMMENDERS, recommender_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{recommender_id}' not found"
        )

    print(f"DELETE FROM {TABLE_RECOMMENDERS} WHERE id = '{recommender_id}'")
    delete_resouce_by_id(TABLE_RECOMMENDERS, recommender_id)

    return resource[0]
