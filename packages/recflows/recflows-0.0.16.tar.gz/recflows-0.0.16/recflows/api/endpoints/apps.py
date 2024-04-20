# Python dependencies
from datetime import datetime

# External dependencies
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import HTTPException

# Inner dependencies
from recflows.services.database import run_query, read_table, read_resource_by_id
from recflows.services.database import insert_resouce, update_resouce, delete_resouce_by_id
from recflows.vars import TABLE_APPS, TABLE_VARIABLES, TABLE_DATASETS, TABLE_MODELS, TABLE_RECOMMENDERS
from recflows.utils.encryption import get_variable_record, encrypt_variable_record


# Create a router to group the endpoints
router = APIRouter()


@router.get("/")
def read_apps():
    return read_table(TABLE_APPS)


@router.post("/")
def create_app(
    app: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}",
            "name": f"name-{int(datetime.now().timestamp())}",
            "description": f"desc-{int(datetime.now().timestamp())}",
        }
    )
):
    id = app.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_APPS, id):
        raise HTTPException(
            status_code=428,
            detail=f'App "{id}" resource al ready exists.'
        )

    insert_resouce(TABLE_APPS, app)

    return app


@router.get("/{app_id}")
def read_app(app_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    return resource[0]


@router.put("/{app_id}")
def update_app(
    app_id: str = Path(...),
    app: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}",
            "name": f"name-{int(datetime.now().timestamp())}",
            "description": f"desc-{int(datetime.now().timestamp())}",
        }
    )
):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    if app.get("id") and app["id"] != app_id:
        raise HTTPException(
            status_code=412,
            detail=f"Resource id '{app_id}' does not match with app id '{app['id']}'"
        )

    app["id"] = app_id
    update_resouce(TABLE_APPS, app)

    return app


@router.delete("/{app_id}")
def delete_app(app_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    print(f"DELETE FROM {TABLE_APPS} WHERE id = '{app_id}'")
    delete_resouce_by_id(TABLE_APPS, app_id)

    return resource[0]


@router.get("/{app_id}/variables")
def read_app_variables(app_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    query = f"""
    SELECT v.*
    FROM {TABLE_VARIABLES} v, {TABLE_APPS} a
    WHERE app_id = a.id
        AND a.id = '{app_id}'
    """
    records = run_query(query)

    return [get_variable_record(r) for r in records]


@router.post("/{app_id}/variables")
def create_app_variable(
    app_id: str = Path(...),
    var: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}",
            "key": "MY_SECRET",
            "value": "VALUE_FOR_MI_SECRET",
        }
    )
):
    id = var.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_VARIABLES, id):
        raise HTTPException(
            status_code=428,
            detail=f'Variable "{id}" resource al ready exists.'
        )

    if not read_resource_by_id(TABLE_APPS, app_id):
        raise HTTPException(
            status_code=404,
            detail=f"Resource app_id='{app_id}' not found"
        )

    var["app_id"] = app_id
    var = encrypt_variable_record(var)

    insert_resouce(TABLE_VARIABLES, var)

    return var


@router.get("/{app_id}/datasets")
def read_app_datasets(app_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    query = f"""
    SELECT d.*
    FROM {TABLE_DATASETS} d, {TABLE_APPS} a
    WHERE app_id = a.id
        AND a.id = '{app_id}'
    """
    return run_query(query)


@router.post("/{app_id}/datasets")
def create_app_dataset(
    app_id: str = Path(...),
    dataset: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}",
            "name": "DATASET_NAME",
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

    if not read_resource_by_id(TABLE_APPS, app_id):
        raise HTTPException(
            status_code=404,
            detail=f"Resource app_id='{app_id}' not found"
        )

    dataset["app_id"] = app_id
    insert_resouce(TABLE_DATASETS, dataset)

    return dataset


@router.get("/{app_id}/models")
def read_app_models(app_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    query = f"""
    SELECT m.*
    FROM {TABLE_MODELS} m, {TABLE_APPS} a
    WHERE app_id = a.id
        AND a.id = '{app_id}'
    """
    return run_query(query)


@router.post("/{app_id}/models")
def create_app_model(
    app_id: str = Path(...),
    models: dict = Body(
        ...,
        example={
            "id": f"id-{int(datetime.now().timestamp())}",
            "name": "MODELS_NAME",
        }
    )
):
    id = models.get("id")

    if not id:
        raise HTTPException(
            status_code=400,
            detail='the required field "id" was not provided.'
        )

    if read_resource_by_id(TABLE_MODELS, id):
        raise HTTPException(
            status_code=428,
            detail=f'Models "{id}" resource al ready exists.'
        )

    if not read_resource_by_id(TABLE_APPS, app_id):
        raise HTTPException(
            status_code=404,
            detail=f"Resource app_id='{app_id}' not found"
        )

    models["app_id"] = app_id
    insert_resouce(TABLE_MODELS, models)

    return models


@router.get("/{app_id}/recommenders")
def read_app_recommenders(app_id: str = Path(...)):
    resource = read_resource_by_id(TABLE_APPS, app_id)

    if not resource:
        raise HTTPException(
            status_code=404,
            detail=f"Resource '{app_id}' not found"
        )

    query = f"""
    SELECT r.*
    FROM {TABLE_RECOMMENDERS} r, {TABLE_MODELS} m, {TABLE_APPS} a
    WHERE r.model_id = m.id
        AND m.app_id = a.id
        AND a.id = '{app_id}'
    """
    return run_query(query)
