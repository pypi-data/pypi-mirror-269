# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_VERSIONS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_versions():
    return read_table(TABLE_VERSIONS)


# @router.post("/")
# def create_version(
#     version: dict = Body(
#         ...,
#         example={
#             "id": f"id-{int(datetime.now().timestamp())}"
#         }
#     )
# ):
#     id = version.get("id")

#     if not id:
#         raise HTTPException(
#             status_code=400,
#             detail='the required field "id" was not provided.'
#         )

#     if read_resource_by_id(TABLE_VERSIONS, id):
#         raise HTTPException(
#             status_code=428,
#             detail=f'Version "{id}" resource al ready exists.'
#         )

#     insert_resouce(TABLE_VERSIONS, version)

#     return version


# @router.get("/{version_id}")
# def read_version(version_id: str = Path(...)):
#     resource = read_resource_by_id(TABLE_VERSIONS, version_id)

#     if not resource:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Resource '{version_id}' not found"
#         )

#     return resource[0]


# @router.put("/{version_id}")
# def update_version(
#     version_id: str = Path(...),
#     version: dict = Body(
#         ...,
#         example={
#             "id": f"id-{int(datetime.now().timestamp())}"
#         }
#     )
# ):
#     resource = read_resource_by_id(TABLE_VERSIONS, version_id)

#     if not resource:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Resource '{version_id}' not found"
#         )

#     if version.get("id") and version["id"] != version_id:
#         raise HTTPException(
#             status_code=412,
#             detail=f"Resource id '{version_id}' does not match with version id '{version['id']}'"
#         )

#     version["id"] = version_id
#     update_resouce(TABLE_VERSIONS, version)

#     return version


# @router.delete("/{version_id}")
# def delete_version(version_id: str = Path(...)):
#     resource = read_resource_by_id(TABLE_VERSIONS, version_id)

#     if not resource:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Resource '{version_id}' not found"
#         )

#     print(f"DELETE FROM {TABLE_VERSIONS} WHERE id = '{version_id}'")
#     delete_resouce_by_id(TABLE_VERSIONS, version_id)

#     return resource[0]
