from typing import List
from fastapi import APIRouter

router = APIRouter()


@router.get("/{form_id}", include_in_schema=False)
def view_all_tasks(form_id: int, ):
    pass


@router.get("/{task_id}", include_in_schema=False)
def read_task(task_id: int, ):
    pass


@router.post("/new-task", include_in_schema=False)
def create_task():
    pass


@router.put("/update-task", include_in_schema=False)
def update_task():
    pass


@router.delete("/{task_id}", include_in_schema=False)
def delete_task():
    pass
