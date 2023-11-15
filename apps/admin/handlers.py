from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import Annotated
from apps.core.models import Project
from apps.db import projects_collection


router = APIRouter()

templates = Jinja2Templates(directory='templates/admin')

@router.get('/')
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/projects')
async def list_projects(request: Request):
    projects_raw = await projects_collection.find().to_list(100)
    print(projects_raw)
    projects = [Project.model_validate(p) for p in projects_raw]
    print(projects)
    return templates.TemplateResponse('list_projects.html', {'request': request, 'projects': projects})

@router.get('/new-project')
async def project_creation_form(request: Request):
    return templates.TemplateResponse('new_project.html', {'request': request, 'Project': Project})


@router.post('/projects')
async def create_project(request: Request, project: Project | ValidationError = Depends(Project.form)):
    if isinstance(project, ValidationError):
        error_msg = project.json(indent=4, include_context=True, include_input=True)
        return templates.TemplateResponse('bad_new_project.html', {'request': request, 'error': error_msg})

    new_project = await projects_collection.insert_one(
        project.model_dump(by_alias=True, exclude=["id"])
    )
    created_project = await projects_collection.find_one(
        {"_id": new_project.inserted_id}
    )
    return RedirectResponse(url=request.url_for('list_projects'), status_code=303)


@router.get('/projects/raw')
async def list_projects_raw(request: Request):
    projects_raw = await projects_collection.find().to_list(100)
    projects = [Project.model_validate(p) for p in projects_raw]
    return templates.TemplateResponse('list_projects_raw.html', {'request': request, 'projects': projects})
