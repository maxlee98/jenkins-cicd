from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from prediction_model.predict import generate_predictions

app = FastAPI(
    title = "Loan Prediction App using API - CI CD Jenkins",
    description = "A simple CI CD Demo",
    version = "1.0"

)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class LoanPrediction(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str


@app.get("/")
def index():
    return {"Message": "Welcome to Loan Prediction App using API - CI CD Jenkins"}

@app.post("/prediction_status")
def predict(loan_details: LoanPrediction):
    data = loan_details.model_dump()
    prediction = generate_predictions([data])["Prediction"][0]
    pred = "Approved" if prediction == "Y" else "Rejected"
    return {"status": pred}

@app.post("/prediction_ui") # Using "Try it out" in FastAPI docs GUI
def predict_gui(Gender: str, Married: str, Dependents: str, Education: str, 
                Self_Employed: str, ApplicantIncome: float, CoapplicantIncome: float, 
                LoanAmount: float, Loan_Amount_Term: float, Credit_history: str, Property_Area: str):
    input_data = [Gender, Married, Dependents, Education, Self_Employed, 
                  ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, 
                  Credit_history, Property_Area]
    cols  = ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 
            'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
            'Credit_history', 'Property_Area']
    
    data_dict = dict(zip(cols, input_data))
    prediction = generate_predictions([data_dict])["Prediction"][0]
    pred = "Approved" if prediction == "Y" else "Rejected"
    return {"status": pred}

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0",port=8005)