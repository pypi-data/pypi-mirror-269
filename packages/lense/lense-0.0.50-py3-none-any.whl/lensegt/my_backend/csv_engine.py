from llama_index.core.query_pipeline import (QueryPipeline as QP, Link, InputComponent,)
from llama_index.experimental.query_engine.pandas import PandasInstructionParser
from llama_index.core import PromptTemplate
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.query_pipeline import (QueryPipeline as QP, Link, InputComponent,)
from llama_index.experimental.query_engine.pandas import PandasInstructionParser
from llama_index.core import PromptTemplate
import os
import openai
from llama_index.llms.openai import OpenAI

import warnings
warnings.filterwarnings('ignore')


def csv_engine_azure(df,api_key=None,api_version=None,azure_endpoint=None):


    api_key= api_key
    api_version= api_version
    azure_endpoint= azure_endpoint

    llm = AzureOpenAI(
        model="gpt-35-turbo-16k",
        deployment_name="gpt-35-turbo-16k",
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
    )

    instruction_str = (
    "1. Convert the query to executable Python code using Pandas.\n"
    "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
    "3. The code should represent a solution to the query.\n"
    "4. PRINT ONLY THE EXPRESSION.\n"
    "5. Do not quote the expression.\n"
    "6. Do not halucinate column names, if query is not related to any of the given columns.\n"
    f"7. Must use the given column names- {str(df.columns.tolist())}  don't use any other column names.")

    pandas_prompt_str = (
        "You are working with a pandas dataframe in Python.\n"
        "The name of the dataframe is `df`.\n"
        "This is the result of `print(df.head())`:\n"
        "{df_str}\n\n"
        "Follow these instructions:\n"
        "{instruction_str}\n"
        "Query: {query_str}\n\n"
        "Expression:")
    
    response_synthesis_prompt_str = (
        "Given an input question, synthesize a response from the query results.\n"
        "Query: {query_str}\n\n"
        "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
        "Pandas Output: {pandas_output}\n\n"
        "Response: ")

    pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
        instruction_str=instruction_str, df_str=df.head(5))
    
    pandas_output_parser = PandasInstructionParser(df)
    response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)

    qp = QP(
    modules={
        "input": InputComponent(),
        "pandas_prompt": pandas_prompt,
        "llm1": llm,
        "pandas_output_parser": pandas_output_parser,
        "response_synthesis_prompt": response_synthesis_prompt,
        "llm2": llm,
    },
    verbose=True,
    )
    qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
    qp.add_links(
        [
            Link("input", "response_synthesis_prompt", dest_key="query_str"),
            Link(
                "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
            ),
            Link(
                "pandas_output_parser",
                "response_synthesis_prompt",
                dest_key="pandas_output",
            ),
        ]
    )
    qp.add_link("response_synthesis_prompt", "llm2")
    return qp.run

def csv_engine_openai(df,api_key=None):


    os.environ["OPENAI_API_KEY"] = api_key
    openai.api_key = os.environ["OPENAI_API_KEY"]
    llm = OpenAI(model="gpt-3.5-turbo")

    instruction_str = (
    "1. Convert the query to executable Python code using Pandas.\n"
    "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
    "3. The code should represent a solution to the query.\n"
    "4. PRINT ONLY THE EXPRESSION.\n"
    "5. Do not quote the expression.\n"
    "6. Do not halucinate column names, if query is not related to any of the given columns.\n"
    f"7. Must use the given column names- {str(df.columns.tolist())}  don't use any other column names.")

    pandas_prompt_str = (
        "You are working with a pandas dataframe in Python.\n"
        "The name of the dataframe is `df`.\n"
        "This is the result of `print(df.head())`:\n"
        "{df_str}\n\n"
        "Follow these instructions:\n"
        "{instruction_str}\n"
        "Query: {query_str}\n\n"
        "Expression:")
    
    response_synthesis_prompt_str = (
        "Given an input question, synthesize a response from the query results.\n"
        "Query: {query_str}\n\n"
        "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
        "Pandas Output: {pandas_output}\n\n"
        "Response: ")

    pandas_prompt = PromptTemplate(pandas_prompt_str).partial_format(
        instruction_str=instruction_str, df_str=df.head(5))
    
    pandas_output_parser = PandasInstructionParser(df)
    response_synthesis_prompt = PromptTemplate(response_synthesis_prompt_str)

    qp = QP(
    modules={
        "input": InputComponent(),
        "pandas_prompt": pandas_prompt,
        "llm1": llm,
        "pandas_output_parser": pandas_output_parser,
        "response_synthesis_prompt": response_synthesis_prompt,
        "llm2": llm,
    },
    verbose=True,
    )
    qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
    qp.add_links(
        [
            Link("input", "response_synthesis_prompt", dest_key="query_str"),
            Link(
                "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
            ),
            Link(
                "pandas_output_parser",
                "response_synthesis_prompt",
                dest_key="pandas_output",
            ),
        ]
    )
    qp.add_link("response_synthesis_prompt", "llm2")
    return qp.run

