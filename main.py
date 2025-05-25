from fastapi import FastAPI, Request, Form, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response

import sqlalchemy as sa

from models import Todo
from db import Session


templates = Jinja2Templates(directory="templates")

app = FastAPI(name="todo")


@app.get('/')
async def home(request: Request, hide_done_tasks: bool = False):
    with Session() as session:
        query = sa.select(Todo)

        if hide_done_tasks:
            query = query.where(sa.not_(Todo.is_done))

        todo_list = session.scalars(
            query
        ).all()

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "todo_list": todo_list,
                "hide_done_tasks": hide_done_tasks
            }
        )


@app.post('/todo')
async def create_todo(request: Request, name: str = Form('')):
    with Session() as session:
        todo = Todo(
            name=name
        )

        session.add(todo)
        session.commit()

        return templates.TemplateResponse(
            request=request,
            name="todo_item.html",
            context={
                "todo": todo
            }
        )


@app.put('/todo/{task_id}/done')
async def mark_todo_as_done(request: Request, task_id: int):
    with Session() as session:
        todo: Todo = session.scalars(
            sa.select(Todo).where(Todo.id == task_id)
        ).first()

        todo.is_done = True
        session.add(todo)
        session.commit()

        return templates.TemplateResponse(
            request=request,
            name="todo_item.html",
            context={
                "todo": todo
            }
        )


@app.delete('/todo/{task_id}')
async def delete_todo(request: Request, task_id: int):
    with Session() as session:
        session.execute(
            sa.delete(Todo).where(Todo.id == task_id)
        )

        session.commit()

        return Response(
            status_code=status.HTTP_200_OK
        )
