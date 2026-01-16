from dotenv import load_dotenv
from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from modules.middleware import check_api_key
# import os
from modules.chat.router import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://31.97.106.30:5174",
        "http://localhost:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(chat_router)

@app.get("/",dependencies=[Depends(check_api_key)])
def hello_world() : 
  print("API Hitting")
  return JSONResponse(
      content={
      "success" : True,
      "message" : "Hello World",
    },
    status_code=200
  )


if __name__ == "__main__" : 
  import uvicorn
  uvicorn.run("main:app",host="0.0.0.0",port=3003,reload=True)