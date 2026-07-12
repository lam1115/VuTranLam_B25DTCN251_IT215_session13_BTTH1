from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from database import engine, Base, get_db
from schema import NewItems, ApiResponse, ApiListResponse
from service import (
    add_item,
    get_all,
    get_item_by_id,
    update_item_by_id,
    delete_item_by_id,
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(HTTPException)
def handle_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "message": exc.detail["message"],
            "data": None,
            "error": exc.detail["error"],
            "path": request.url.path,
            "timestamp": datetime.now().isoformat(),
        },
    )


@app.post(
    "/menu-items", response_model=ApiResponse, status_code=status.HTTP_201_CREATED
)
def new_item(request: Request, item: NewItems, db: Session = Depends(get_db)):
    result = add_item(item, db)

    if result == 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Item already exists", "error": "Conflict"},
        )

    return {
        "statusCode": 201,
        "message": "Thêm món ăn thành công",
        "data": result,
        "error": None,
        "path": request.url.path,
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/menu-items", response_model=ApiListResponse, status_code=status.HTTP_200_OK)
def get_all_item(request: Request, db: Session = Depends(get_db)):
    result = get_all(db)

    return {
        "statusCode": 200,
        "message": "Danh sách món ăn",
        "data": result,
        "error": None,
        "path": request.url.path,
        "timestamp": datetime.now().isoformat(),
    }


@app.get(
    "/menu-items/{item_id}", response_model=ApiResponse, status_code=status.HTTP_200_OK
)
def get_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    result = get_item_by_id(item_id, db)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Không tìm thấy món ăn", "error": "Not found"},
        )

    return {
        "statusCode": 200,
        "message": "Tìm thấy món ăn",
        "data": result,
        "error": None,
        "path": request.url.path,
        "timestamp": datetime.now().isoformat(),
    }


@app.put(
    "/menu-items/{item_id}", response_model=ApiResponse, status_code=status.HTTP_200_OK
)
def update_item(
    request: Request, item_id: int, item: NewItems, db: Session = Depends(get_db)
):
    result = update_item_by_id(item_id, item, db)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Không tìm thấy món ăn", "error": "Not found"},
        )

    return {
        "statusCode": 200,
        "message": "Danh sách món ăn",
        "data": result,
        "error": None,
        "path": request.url.path,
        "timestamp": datetime.now().isoformat(),
    }


@app.delete(
    "/menu-items/{item_id}", response_model=ApiResponse, status_code=status.HTTP_200_OK
)
def delete_item(request: Request, item_id: int, db: Session = Depends(get_db)):
    result = delete_item_by_id(item_id, db)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Không tìm thấy món ăn", "error": "Not found"},
        )

    return {
        "statusCode": 200,
        "message": "Danh sách món ăn",
        "data": result,
        "error": None,
        "path": request.url.path,
        "timestamp": datetime.now().isoformat(),
    }
