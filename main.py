import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apps import admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    from apps.db import db
    db.command('ping')
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(
    admin.router,
    prefix='/admin',
)


# LATER: move to "core" app

templates = Jinja2Templates(directory="templates")

@app.get('/')
async def index(request: Request) -> str:
    return templates.TemplateResponse('index.html', {'request': request})


# @app.get('/health')
# async def health():
#     return {'status': 'ok'}


# @app.post('/user')
# async def create_user(user: models.User) -> JSONResponse:
#     query = 'INSERT INTO "user" (username, password, first_name, last_name, email, phone) VALUES ($1, $2, $3, $4, $5, $6);'
#     await app.db_pool.execute(query, user.username, user.password, user.first_name, user.last_name, user.email, user.phone)
#     return JSONResponse(status_code=200, content={'status': f'User `{user.username}` was created'})


# @app.get('/user/{username}')
# async def get_user(username: str):
#     query = 'SELECT username, first_name, last_name, email, phone FROM "user" WHERE username = $1;'
#     record = await app.db_pool.fetchrow(query, username)
#     if record is None:
#         return JSONResponse(status_code=404, content={'status': 'error', 'error': 'User not found'})
#     return models.User(**record)

# @app.put('/user/{username}')
# async def update_user(user: models.User) -> JSONResponse:
#     if not await is_user_exists(user.username):
#         return JSONResponse(status_code=404, content={'status': 'error', 'error': 'User not found'})
#     query = 'UPDATE "user" SET username = $1, password = $2, first_name = $3, last_name = $4, email = $5, phone = $6 WHERE username = $1;'
#     await app.db_pool.execute(query, user.username, user.password, user.first_name, user.last_name, user.email, user.phone)
#     return JSONResponse(status_code=200, content={'status': f'User `{user.username}` was updated'})

# @app.delete('/user/{username}')
# async def delete_user(username: str) -> JSONResponse:
#     if not await is_user_exists(username):
#         return JSONResponse(status_code=404, content={'status': 'error', 'error': 'User not found'})
#     query = 'DELETE FROM "user" WHERE username = $1;'
#     await app.db_pool.execute(query, username)
#     return JSONResponse(status_code=200, content={'status': f'User `{username}` was deleted'})

# async def is_user_exists(username) -> bool:
#     query = 'SELECT username FROM "user" WHERE username = $1'
#     record = await app.db_pool.fetchrow(query, username)
#     return record is not None
