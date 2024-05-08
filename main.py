from fastapi import FastAPI, Depends, status, HTTPException, Response
from database import engine, get_db 
import schema, model
from routers import users, auth, election, vote
# from routers import history, transactions, users, auth, transactions, admin, vote
from config import settings as ss
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI(title=ss.project_title, 
              description="Online Voting System", 
              version=ss.project_version)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#i added this try except block to catch database connection issues
while True:
    try:
        conn = psycopg2.connect(host="127.0.0.1",database="postgres",user="postgres",password="password",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print(cursor)
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(5)

@app.get("/api")
def root():
    return {"message": "One to many"}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(election.router)
app.include_router(vote.router)
# app.include_router(vote.router)



model.Base.metadata.create_all(engine)

















 


# if __name__== "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=9000)


