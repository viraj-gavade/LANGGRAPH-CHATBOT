from langgraph.graph import StateGraph , add_messages, START , END
from typing import TypedDict ,Annotated , Literal
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel , Field 
import operator
from langchain_core.messages import SystemMessage , HumanMessage , BaseMessage
from langgraph.checkpoint.memory import MemorySaver
import os

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


checkpointer = MemorySaver()

llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
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




