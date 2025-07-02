import asyncio
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.sql.connect import create_db_and_tables
from src.storages.routes import storages_router, suppliers_router, recipes_router, sellproducts_router, receipts_router, typeproducts_router
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import items, login, private, users, utils

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(storages_router)
app.include_router(suppliers_router)
app.include_router(typeproducts_router)
app.include_router(receipts_router)
app.include_router(recipes_router)
app.include_router(sellproducts_router)


app.include_router(login.router)
app.include_router(users.router)
app.include_router(utils.router)
app.include_router(items.router)
app.include_router(private.router)

origins = [
    "http://localhost:5173",
    "localhost:5173"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# async def main():
#     config = uvicorn.Config(app, port=9800, log_level="info", reload=True)
#     server = asyncio.create_task(uvicorn.Server(config).serve())
#     await server


if __name__ == "__main__":
    #asyncio.run(main())
    uvicorn.run("main:app", port=9800, log_level="info", reload=True)
    
    
    #https://fastapi.tiangolo.com/tutorial/path-params/#create-an-enum-class
