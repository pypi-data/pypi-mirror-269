import pandas as pd
import pathlib
import warnings
from llama_index.readers.file import PyMuPDFReader
from lensegt.my_backend.error_handling import *
from lensegt.my_backend.replace_file import *
import warnings
warnings.filterwarnings('ignore')

def load_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None

def load_pdf(file_path):
    try:
        loader = PyMuPDFReader()
        documents = loader.load(file_path=file_path)
        return documents
    except Exception as e:
        print(f"Error reading file '{file_path}': {e}")
        return None   

def load_document(filepath):
  
  filepath = pathlib.Path(filepath)
  if not filepath.is_file():
    raise FileNotFoundError(f"File not found: {filepath}")
  
  extension = filepath.suffix.lower()
  if extension == ".pdf":
    return load_pdf(filepath)
  elif extension == ".csv":
    return load_csv(filepath)
  
  warnings.warn(f"Unsupported file format: {extension}")
  return None


