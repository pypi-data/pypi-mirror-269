from fastapi import HTTPException


def handle_exception(f):
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise HTTPException(status_code=406, detail=str(e))
    return wrapper
