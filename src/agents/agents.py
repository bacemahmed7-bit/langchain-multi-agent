from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search , scrape_url

import os
from dotenv import load_dotenv , find_dotenv

_=load_dotenv(find_dotenv())
groq_api_key=os.environ['GROQ_API_KEY']


groq_llm_model = ChatGroq(model="openai/gpt-oss-20b" , temperature=0)



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


writer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are an expert research writer . Write clear , srtructured and insightful reports .  "),
        ('human'  , 
         """
            Write a detailed research report on the topic below.

                Topic: {topic}

                Research Gathered:
                {research}

                Structure the report as:
                - Introduction
                - Key Findings (minimum 3 well-explained points)
                - Conclusion
                - Sources (list all URLs found in the research)

                Be detailed, factual and professional.

         """ 
         )
    ]
)

writer_agent = writer_prompt | groq_llm_model | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a sharp and constructive research critic. Be honest and specific."),
        ("human", 
            """
            Review the research report below and evaluate it strictly.

                Report: {report}

                Respond in this exact format:

                    Score: X/10

                    Strengths:
                        - ...
                        - ...

                    Areas to Improve:
                    - ...
                    - ...

                    One line verdict:
                    -...

            """
    ),
])

critic_agent = critic_prompt | groq_llm_model | StrOutputParser()

