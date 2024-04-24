#from loader import load_document
from lensegt.my_backend.qna_engine import *
from lensegt.my_backend.SQL_engine import *
from lensegt.my_backend.csv_engine import *
from fastapi import FastAPI, File, UploadFile, Form
from enum import Enum
from lensegt.my_backend.qna_engine import embed_and_run_openai, embed_and_run_azureopenai, embed_and_run_mistral
import shutil
import os
from lensegt.my_backend.loader import load_document
from fastapi import FastAPI, Request ,APIRouter
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
import uvicorn
import warnings
warnings.filterwarnings('ignore')


app = FastAPI()

# Define an Enum for engine selection
class EngineType(str, Enum):
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"
    MISTRAL = "Mistral"

class EngineType1(str, Enum):
    OPENAI = "OpenAI"
    AZURE_OPENAI = "Azure OpenAI"

# List to store engines
engines = []

uploaded_file_path = None


@app.post("/upload/")
def upload_file(file: UploadFile = File(...)):
    global uploaded_file_path
    try:
        # Save the uploaded file to the temporary directory
        save_path = f"{file.filename}"
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update the temporary variable with the uploaded file path
        uploaded_file_path = save_path
        
        return {"result": "File uploaded successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    
    

@app.post("/process_document/")
def process_document(
    engine_type: EngineType,
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None),
    hf_token: str = Form(None)
):
    global uploaded_file_path
    try:
        # Check if a file has been uploaded
        if uploaded_file_path is None:
            return {"error": "No file uploaded"}

        # Load the document
        documents = load_document(uploaded_file_path)
        
        # Select and run the appropriate engine based on user input
        if engine_type == EngineType.OPENAI:
            if api_key is None:
                return {"error": "api_key is required for OpenAI"}
            engine = embed_and_run_openai(
                documents=documents,
                api_key=api_key
            )
        elif engine_type == EngineType.AZURE_OPENAI:
            if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
            engine = embed_and_run_azureopenai(
                documents=documents,
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
        elif engine_type == EngineType.MISTRAL:
            if hf_token is None:
                return {"error": "hf_token is required for Mistral"}
            engine = embed_and_run_mistral(
                documents=documents,
                hf_token=hf_token
            )
        else:
            return {"error": "Invalid engine type"}
        
        # Store the engine in the list
        engines.append(engine)
        
        # Clean up: Remove the temporary file
        os.remove(uploaded_file_path)
        
        # Reset the uploaded file path
        uploaded_file_path = None
        
        return {"result": "Engine created and stored successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/use-engine_document/")
def use_engine(
    query: str = Form(...)
     ):
    try:
        # Check if any engine has been stored
        if not engines:
            return {"error": "No engine available"}
        
        # Use the latest stored engine to run the query
        engine = engines[-1]
        result = engine(query)

        return {"result": str(result)}
    
    except Exception as e:
        return {"error": str(e)}
@app.post("/process_csv/")
def process_document(
    engine_type: EngineType1,
    api_key: str = Form(None),
    api_version: str = Form(None),
    azure_endpoint: str = Form(None)
):
    global uploaded_file_path
    try:
        # Check if a file has been uploaded
        if uploaded_file_path is None:
            return {"error": "No file uploaded"}

        # Load the document
        documents = load_document(uploaded_file_path)
        
        # Select and run the appropriate engine based on user input
        if engine_type == EngineType1.OPENAI:
            if api_key is None:
                return {"error": "api_key is required for OpenAI"}
            engine = csv_engine_openai(
                df=documents,
                api_key=api_key
            )
        elif engine_type == EngineType1.AZURE_OPENAI:
            if any(arg is None for arg in [api_key, api_version, azure_endpoint]):
                return {"error": "api_key, api_version, and azure_endpoint are required for Azure OpenAI"}
            engine = csv_engine_azure(
                df=documents,
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=azure_endpoint
            )
        else:
            return {"error": "Invalid engine type"}
        
        # Store the engine in the list
        engines.append(engine)
        
        # Clean up: Remove the temporary file
        os.remove(uploaded_file_path)
        
        # Reset the uploaded file path
        uploaded_file_path = None
        
        return {"result": "Engine created and stored successfully"}
    
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/use-engine_csv/")
def use_engine(
    query: str = Form(...)
):
    try:
        # Check if any engine has been stored
        if not engines:
            return {"error": "No engine available"}
        
        # Use the latest stored engine to run the query
        engine = engines[-1]
        result = engine(query_str=query)
        result = result.message.content

        return {"result": result}
    
    except Exception as e:
        return {"error": str(e)}
    

def start():
    print("-"*100)
    print("Inside the the start function")
    print("current path of directory",os.getcwd())
    app.mount("/", StaticFiles(directory="lensegt/my_frontend", html=True), name="my_frontend")
    uvicorn.run("lensegt.lense.app:app", reload=False, host="127.0.0.1", port=9017,workers=1)
