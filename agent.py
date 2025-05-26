from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
from tools import (
    get_genre_recommendation,
    get_movie_info,
    get_movie_recommendation,
    get_popular_movies,
    search_tool
)
load_dotenv()


#memory=ConversationBufferMemory(memory_key="chat_history",return_messages=True)

def ai_agent(query):
    prompt=hub.pull("hwchase17/react")
    memory=ConversationBufferMemory(memory_key="chat_history",return_messages=True)

    llm = ChatGroq(model='Gemma2-9b-It')

    agent = create_react_agent(
        llm=llm,
        tools=[get_movie_recommendation,get_movie_info,search_tool,get_popular_movies,get_genre_recommendation],
        prompt=prompt
    )



    agent_executor=AgentExecutor(
        agent=agent,
        tools=[get_movie_recommendation,get_movie_info,search_tool,get_popular_movies,get_genre_recommendation],
        memory=memory

    )

    response = agent_executor.invoke({'input':f'{query}'})

    return response['output']