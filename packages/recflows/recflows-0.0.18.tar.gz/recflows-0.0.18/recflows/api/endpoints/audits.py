# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_AUDITS

# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_audits():
    return read_table(TABLE_AUDITS)


@router.post("/")
def create_audit(
    audit: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    id = audit.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_AUDITS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Audit "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_AUDITS, audit)

    return audit


@router.get("/{audit_id}")
def read_audit(audit_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_AUDITS, audit_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{audit_id}' not found"
        )

    return resource[0]


@router.put("/{audit_id}")
def update_audit(
    audit_id: str = Path(...),
    audit: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}"
        }
    )
):
    resource = read_resource_by_id(TABLE_AUDITS, audit_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{audit_id}' not found"
        )

    if audit.get("id") and audit["id"] != audit_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{audit_id}' does not match with audit id '{audit['id']}'"
        )

    audit["id"] = audit_id
    update_resouce(TABLE_AUDITS, audit)

    return audit


@router.delete("/{audit_id}")
def delete_audit(audit_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_AUDITS, audit_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{audit_id}' not found"
        )

    print(f"DELETE FROM {TABLE_AUDITS} WHERE id = '{audit_id}'")
    delete_resouce_by_id(TABLE_AUDITS, audit_id)

    return resource[0]
