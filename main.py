from dotenv import load_dotenv
from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from modules.helper.middleware import check_api_key
import os
load_dotenv()

app = FastAPI()

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
  uvicorn.run("main:app",host="0.0.0.0",port=3002,reload=True)