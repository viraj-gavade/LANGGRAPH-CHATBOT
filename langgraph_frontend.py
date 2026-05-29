import streamlit as st 
from langchain_core.messages import HumanMessage

# Page configuration
st.set_page_config(page_title="LangGraph Chatbot", layout="wide")
st.title("🤖 LangGraph Chatbot")

# Try to import backend
try:
    from langgraph_backend import chatbot
    backend_loaded = True
except Exception as e:
    backend_loaded = False
    error_msg = str(e)
    st.error(f"❌ Backend Error: {error_msg}")
    st.info("Check the terminal for more details. Make sure all dependencies are installed and API keys are set.")

# Session state -> dict 
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if not backend_loaded:
    st.stop()  # Stop execution if backend failed to load


# Display chat messages
st.write("### Chat History")
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Input section
st.divider()
st.write("### Send a Message")
user_input = st.chat_input('Type your message here...')

config = {'configurable':{'thread_id':1}}

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





