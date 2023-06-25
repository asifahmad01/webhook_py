# Create a FastAPI application

import os

import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI

from api import whatsapp_handler

app = FastAPI()
app.include_router(whatsapp_handler.router)

@app.post("/webhook")
async def handle_webhook():
    # Handle the webhook logic here
    return {"message": "Webhook received"}

if __name__ == "__main__":py
    
    uvicorn.run(app, port=8000)
