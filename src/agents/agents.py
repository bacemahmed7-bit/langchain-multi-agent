from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search , scrape_url

import os
from dotenv import load_dotenv , find_dotenv

_=load_dotenv(find_dotenv)
groq_api_key=os.environ['GROQ_API_KEY']

groq_llm_model = ChatGroq(model="openai/gpt-oss-120b" , temperature=0)


def build_search_agent():
    search_agent = create_agent(
        model=groq_llm_model, 
        tools=[web_search]
        )
    return search_agent



def build_Reader_agent():
    reader_agent =create_agent(
        model=groq_llm_model,
        tools=[scrape_url]
    )
    return reader_agent