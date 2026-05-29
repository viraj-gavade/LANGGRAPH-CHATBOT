import streamlit as st 
from langchain_core.messages import HumanMessage
import uuid

# Page configuration
st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🤖 LangGraph Chatbot")

###################################### Utility Functions ############################################################################

def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []
    add_thread_id(st.session_state['thread_id'])


def add_thread_id(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def get_coversation(thread_id):
    config = {'configurable': {'thread_id': thread_id}}
    state = chatbot.get_state(config=config)
    messages = state.values.get("messages", [])
    return messages





# Session state -> dict 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()



if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] =   []


add_thread_id(st.session_state['thread_id'])

# Try to import backend
try:
    from langgraph_backend import chatbot
    backend_loaded = True
except Exception as e:
    backend_loaded = False
    error_msg = str(e)
    st.error(f"❌ Backend Error: {error_msg}")
    st.info("Check the terminal for more details. Make sure all dependencies are installed and API keys are set.")



if not backend_loaded:
    st.stop()  # Stop execution if backend failed to load

###################################### Sidebar UI ############################################################################
st.sidebar.title('Langgraph Chatbot')
if st.sidebar.button('New chat'):
    reset_chat()

st.sidebar.header('My conversations')
for thread_id in  st.session_state['chat_threads'] :
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = get_coversation(thread_id)
       

        temp_messages = []

        for message in messages:
        
            if isinstance(message , HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role':role,'content':message.content})
           
            st.session_state['message_history'] = temp_messages
        



# Display chat messages
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input section
st.divider()
user_input = st.chat_input('Type your message here...')

config = {'configurable':{'thread_id':st.session_state['thread_id']}}

if user_input:
    try:
        # Add user message to history
        st.session_state['message_history'].append({'role':'user','content':user_input})
        with st.chat_message('user'):
            st.markdown(user_input)

        # Get response from chatbot
        ai_message =  st.write_stream(
                message_chunk.content for message_chunk, metadata  in chatbot.stream({'messages': HumanMessage(content=user_input)},config=config,stream_mode='messages')

            )
        # Add assistant message to history
        st.session_state['message_history'].append({'role':'assistant','content':ai_message})

        
        st.rerun()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Make sure the backend is running properly and API keys are configured.")





