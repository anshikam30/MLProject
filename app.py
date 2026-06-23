import sys
import os

import certifi
ca = certifi.where()

import pymongo
from src.logger import logging
from src.exception import NetworkSecurityException
from src.pipeline.training_pipeline import Training_Pipeline
from src.utils.main_utils.utils import load_object
from src.utils.ml_utils.utils import NetworkModel

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

from fastapi.templating import Jinja2Templates 
templates = Jinja2Templates(directory = "./templates")


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
    
    
@app.post("/predict")
async def predict_route(request: Request , file: UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        
        preprocessor = load_object("final_models/preprocessing.pkl")
        model = load_object("final_models/model.pkl")
        
        network_model = NetworkModel(preprocessor=preprocessor, model=model)
        
        y_pred = network_model.predict(df)
        df['predicted_column']  = y_pred
        df.to_csv("prediction_output/output.csv")

        table_html = df.to_html(classes="table table-striped", index=False)


        templates.TemplateResponse(
    request=request,
    name="table.html", 
    context={"table": table_html}
)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
    
if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)