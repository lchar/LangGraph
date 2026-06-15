# not really an agent, more like a *Simple Bot*

from typing import TypedDict, List
from langchain_core.messages import HumanMessage
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
# from dotenv import load_dotenv  # Used to store API keys and secret information

# load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

# This can cost money, gemini-2.0 might work for free (or use locallama)
# llm = ChatOpenAI(model='gpt-4o')
llm = ChatOllama(model='llama3.2')

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f'\nAI: {response.content}')
    return state


graph = StateGraph(AgentState)

graph.add_node('process', process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

agent = graph.compile()


user_input = input('Enter: ')
while user_input != 'exit':
    agent.invoke({'messages': [HumanMessage(content=user_input)]})
    user_input = input('Enter: ')