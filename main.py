import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import signin, signup, forgotpassword, rolloutbillboard
from app.db.db_setup import SessionLocal, Base, engine
# from app.db.database import connect_db, disconnect_db
# from app.db.database import connect_db,disconnect_db

app = FastAPI()


Base.metadata.create_all(bind=engine)
# # Event handlers for startup and shutdown
# @app.on_event("startup")
# async def on_startup():
#     await connect_db()
#     # await create_tables()

# @app.on_event("shutdown")
# async def on_shutdown():
#     await disconnect_db()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


# API Routes
app.include_router(signup.router)
app.include_router(signin.router)
app.include_router(forgotpassword.router)
app.include_router(rolloutbillboard.router)
# app.include_router(my_billboards.router)
# app.include_router(book_billboard.router)
# app.include_router(my_bookings.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)
