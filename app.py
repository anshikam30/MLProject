import sys
import os

import certifi
ca = certifi.where()

import pymongo
from src.logger import logging
from src.exception import NetworkSecurityException
from src.pipeline.training_pipeline import Training_Pipeline
from src.utils.main_utils.utils import load_object

from fastapi import FastAPI, File , UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware 
from starlette.responses import RedirectResponse

import pandas as pd

from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGODB_URL_KEY")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile= ca)


from src.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


@app.get("/", tags = ["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/train")
async def train_route():
    try:
        train_pipeline  = Training_Pipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful.")
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)