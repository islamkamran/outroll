import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import signin, signup, forgotpassword, rolloutbillboard, bookbillboard, listBillboards, mybillboards, mybookings, refreshtoken, searchbillboard, updatebillboard
from app.db.db_setup import Base, engine
from app.logs import setup_logging


app = FastAPI()

# Initiallizing the logging file
setup_logging()

# This function calls the ORM declerative base so that it may catch the difference
Base.metadata.create_all(bind=engine)

# Directory to store the uploaded images
UPLOAD_DIR = "uploads"

# These are used to remove the CORS error B/W different server in my case Python Back-end and flutter-dart front-end
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

# Just for checking if the application is working properly
@app.get("/")
async def main():
    return {"message": "Application is Working"}


# API routes name of the modules remember not the routes itself
app.include_router(signup.router)
app.include_router(signin.router)
app.include_router(forgotpassword.router)
app.include_router(listBillboards.router)
app.include_router(rolloutbillboard.router)
app.include_router(bookbillboard.router)
app.include_router(mybillboards.router)
app.include_router(mybookings.router)
app.include_router(refreshtoken.router)
app.include_router(searchbillboard.router)
app.include_router(updatebillboard.router)




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5002, reload=True)
