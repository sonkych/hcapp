from typing import List
from fastapi import APIRouter

router = APIRouter()


@router.get("/{form_id}")
def view_all_tasks(form_id: int, ):
    pass


@router.get("/{task_id}")
def read_task(task_id: int, ):
    pass


@router.post("/new-task")
def create_task():
    pass


@router.put("/update-task")
def update_task():
    pass


@router.delete("/{task_id}")
def delete_task():
    pass
