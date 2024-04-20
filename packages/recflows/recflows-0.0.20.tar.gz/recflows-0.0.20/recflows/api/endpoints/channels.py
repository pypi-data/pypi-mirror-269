# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_CHANNELS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_channels():
    return read_table(TABLE_CHANNELS)


@router.post("/")
def create_channel(
    channel: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = channel.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_CHANNELS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Channel "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_CHANNELS, channel)

    return channel


@router.get("/{channel_id}")
def read_channel(channel_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_CHANNELS, channel_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{channel_id}' not found"
        )

    return resource[0]


@router.put("/{channel_id}")
def update_channel(
    channel_id: str = Path(...),
    channel: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_CHANNELS, channel_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{channel_id}' not found"
        )

    if channel.get("id") and channel["id"] != channel_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{channel_id}' does not match with channel id '{channel['id']}'"
        )

    channel["id"] = channel_id
    update_resouce(TABLE_CHANNELS, channel)

    return channel


@router.delete("/{channel_id}")
def delete_channel(channel_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_CHANNELS, channel_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{channel_id}' not found"
        )

    print(f"DELETE FROM {TABLE_CHANNELS} WHERE id = '{channel_id}'")
    delete_resouce_by_id(TABLE_CHANNELS, channel_id)

    return resource[0]
