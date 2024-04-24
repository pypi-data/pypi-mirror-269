from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import OpenAI
from langchain_openai import AzureChatOpenAI
from langchain_google_genai import GoogleGenerativeAI

import warnings
warnings.filterwarnings('ignore')

def sql_engine_openai(db_url,api_key=None):
    db = SQLDatabase.from_uri(db_url,sample_rows_in_table_info=6)
    llm = OpenAI(temperature=0, verbose=True,api_key=api_key)
    
    prior_context = f"""Strictly follow the following instructions:
                        -Please always show the data by explaining the query.
                        -whenever ther is no SQLResult do not return anything as Answer.
                        -Never explain the SQLResult and procedure.
                        -Always Explain the final answer according to the query.
                        """
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    while True:
        query = input("Query:")
        query = f"""{prior_context} Question: {query}"""
        try:
            answer=db_chain.run(query)
        except Exception as e:
            print(e)
        print(answer)



def sql_engine_azure(db_url, api_key=None, api_version=None, azure_endpoint=None):
    db = SQLDatabase.from_uri(db_url,sample_rows_in_table_info=6)

    llm = AzureChatOpenAI(model="gpt-35-turbo-16k", temperature=0, max_tokens=600, api_key = api_key ,azure_endpoint=azure_endpoint,api_version=api_version)
    prior_context = f"""Strictly follow the following instructions:
                        -Please always show the data by explaining the query.
                        -whenever ther is no SQLResult do not return anything as Answer.
                        -Never explain the SQLResult and procedure.
                        -Always Explain the final answer according to the query.
                        """
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    while True:
        query = input("Query:")
        query = f"""{prior_context} Question: {query}"""
        try:
            answer=db_chain.run(query)
        except Exception as e:
            print(e)
        print(answer)


def sql_engine_genai(db_url,api_key):
    
    db = SQLDatabase.from_uri(db_url,sample_rows_in_table_info=6)
    llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key= api_key )
    # llm = GoogleGenerativeAI(model="models/gemini-pro", google_api_key= 'AIzaSyAHaL4BHo_77l17oDcNjvlGJEIZgjsjSyE' )
    prior_context = f"""Strictly follow the following instructions:
                        -Please always show the data by explaining the query.
                        -whenever ther is no SQLResult do not return anything as Answer.
                        -Never explain the SQLResult and procedure.
                        -Always Explain the final answer according to the query.
                        """
    db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
    while True:
        query = input("Query:")
        query = f"""{prior_context} Question: {query}"""
        try:
            answer=db_chain.run(query)
        except Exception as e:
            print(e)
        print(answer)