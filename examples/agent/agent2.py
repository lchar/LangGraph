# Chatbot with memory

import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
# from dotenv import load_dotenv  # Used to store API keys and secret information

# load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

# This can cost money, use local llama for free
# llm = ChatOpenAI(model='gpt-4o')

# Local llama
llm = ChatOllama(model='llama3.2')

def process(state: AgentState) -> AgentState:
    """This node will solve the requested query"""
    response = llm.invoke(state["messages"])

    state['messages'].append(AIMessage(content=response.content))

    print(f'\nAI: {response.content}')
    # print('CURRENT STATE: ', state['messages'])

    return state


graph = StateGraph(AgentState)

graph.add_node('process', process)
graph.add_edge(START, 'process')
graph.add_edge('process', END)

agent = graph.compile()

conversation_history = []

user_input = input('Enter: ')
while user_input != 'exit':
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({'messages': conversation_history})
    conversation_history = result['messages']
    user_input = input('Enter: ')

# Try to :
#   1. load this if it exists when we restart the agent
#   2. Limit the memory to the last n exchanges (say n = 5) where an exchange is a pair of human and AI messages
with open('C:/Users/donga/Python Projects/LangGraph/examples/agent/logs/logging_agent2.txt', 'w') as file:
    file.write('Your conversation log:\n')
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f'You: {message.content}\n')
        elif isinstance(message, AIMessage):
            file.write(f'AI: {message.content}\n\n')
    file.write('End of conversation')

print('Conversation saved to logging.txt')