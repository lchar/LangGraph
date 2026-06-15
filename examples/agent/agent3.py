# ReAct Agent (Reacting and Acting)
#   Agent has access to tools

import os
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage    # Foundational class for messages in LangGraph
from langchain_core.messages import ToolMessage    # Messages passed back to LLP after a tool call
from langchain_core.messages import SystemMessage  # Messages providing instructions to the LLM
# from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
# from dotenv import load_dotenv  # Used to store API keys and secret information

# Annotated - provides additional context without affecting the type itself
#   e.g.  email = Annotated[str, "This has to be a valid email format"]
#         print(email.__metadata__) would show the context string
# 
#  Sequence - Automatically handles the state updates for sequences such as adding
#             messages to chat history
#
# Reducer Function - (Related to 'tool' import) Rule that controls how updates are combined
#                    with the existing state. Tells us how to merge new data into the current
#                    state. Without a reducer, we would replace the entire value every time.
#                    (like the entire state?)

# load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int):
    """this is an addition function that adds 2 numbers together"""
    # Tools MUST have a docstring

    return a + b

@tool
def subtract(a: int, b: int):
    """this is an subtraction function that computes the difference between 2 numbers"""

    return a - b

@tool
def multiply(a: int, b: int):
    """this is an multiplication function that computes the product of 2 numbers"""

    return a * b

tools = [add, subtract, multiply]

# This can cost money, use local llama for free
# llm = ChatOpenAI(model='gpt-4o')

# Local llama with bind tools
model = ChatOllama(model='llama3.2').bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    """This node will solve the requested query"""
    system_prompt = SystemMessage(content=
        "You are my AI assistant, please answer my query to the best of your ability."
    )
    response = model.invoke([system_prompt] + state['messages'])
    return {'messages': [response]}  # Reducer function takes care of appending


def should_continue(state: AgentState):
    messages = state['messages']
    last_message = messages[-1]
    if not last_message.tool_calls:
        return 'end'
    else:
        return 'continue'


graph = StateGraph(AgentState)
graph.add_node('our_agent', model_call)

tool_node = ToolNode(tools=tools)
graph.add_node('tools', tool_node)

graph.set_entry_point('our_agent')

graph.add_conditional_edges(
    'our_agent', 
    should_continue,
    {
        'continue': 'tools',
        'end': END,
    },
)

graph.add_edge('tools', 'our_agent')

app = graph.compile()


# Helper function to print outputs
def print_stream(stream):
    for s in stream:
        message = s['messages'][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {'messages': [('user', 'Add 34 + 57. Then multiply the result by 3. Also tell me a joke, please.')]}
print_stream(app.stream(inputs, stream_mode='values'))
