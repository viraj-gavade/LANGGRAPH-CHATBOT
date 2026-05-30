from langgraph.graph import StateGraph , add_messages, START , END
from typing import TypedDict ,Annotated , Literal
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel , Field 
from langgraph.checkpoint.sqlite import SqliteSaver
import operator
from langchain_core.messages import SystemMessage , HumanMessage , BaseMessage
from langgraph.checkpoint.memory import MemorySaver
import os
import sqlite3

conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


checkpointer = SqliteSaver(conn=conn)

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    api_key='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'
)


def chat_node(state : ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages' : [response]}


graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

chatbot = graph.compile(checkpointer=checkpointer)




# test 
# config = {'configurable':{'thread_id':1}}
# response = chatbot.invoke({'messages': HumanMessage(content='what is my name?')},config=config)

# print(response)


## GETTING THE NUMBER OF THREADS

def retrive_all_threads():
    all_threads = []

    for checkpoint in checkpointer.list(None):
        if checkpoint.config['configurable']['thread_id'] not in all_threads:
            all_threads.append(checkpoint.config['configurable']['thread_id'])
    return all_threads
