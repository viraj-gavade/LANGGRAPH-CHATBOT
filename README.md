# LangGraph Chatbot 🤖

> 🎓 **This is my FIRST PROJECT learning LangGraph!** A learning-phase exploration of graph-based AI workflows.

A simple yet powerful chatbot built with **LangGraph** and **Streamlit**, demonstrating core concepts of state management, graph-based workflows, and persistent conversation history.

## 📖 Project Description

This is a conversational AI chatbot that leverages LangGraph's StateGraph architecture to manage conversation state and ensure thread-safe, persistent message handling. It provides a clean web interface built with Streamlit and integrates with the Groq API for fast LLM inference using the Qwen 3 model.

**Learning Focus:** Understanding LangGraph fundamentals including state management, graph construction, message handling, and memory persistence.

### Key Features

✨ **Graph-Based Architecture** - Uses LangGraph's StateGraph for clean, composable workflow management  
💾 **Persistent Memory** - MemorySaver checkpointer maintains conversation history across sessions  
🧵 **Thread Management** - Thread-based conversation tracking for multi-user support  
⚡ **Fast Inference** - Powered by Groq's API with Qwen3-32B model  
🎨 **Streamlit UI** - Beautiful, interactive chat interface  
📝 **Message History** - Maintains full conversation context for better responses  

## 🏗️ Architecture

### Backend (`langgraph_backend.py`)

The backend implements a simple but effective graph-based chatbot:

```
START → chat_node → END
```

**Components:**
- **ChatState** - TypedDict that defines the conversation state with message history
- **chat_node()** - Processing node that sends messages to the LLM and returns responses
- **StateGraph** - Graph structure that orchestrates the workflow
- **MemorySaver** - Checkpointer for persisting conversation state

**LLM Configuration:**
- Model: `qwen/qwen3-32b` (32B parameter reasoning model)
- Temperature: 0 (deterministic responses)
- Reasoning Format: Parsed (structured reasoning output)

### Frontend (`langgraph_frontend.py`)

The frontend provides an interactive chat interface:

**Features:**
- Real-time message display with Streamlit's chat UI
- Session state management for client-side message history
- Thread-based conversation context (thread_id: 1)
- Automatic message formatting with sender roles

## 📋 Prerequisites

- Python 3.8+
- Groq API key (get one at https://console.groq.com)
- pip or conda package manager

## 🚀 Setup & Installation

### 1. Clone/Download the Project
```bash
cd "Agentic AI (CampusX)/LANGGRAPH-CHATBOT"
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install langgraph langchain langchain-groq streamlit pydantic python-dotenv
```

Or from the parent directory's requirements.txt:
```bash
pip install -r ../requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in this directory:
```
GROQ_API_KEY=your_groq_api_key_here
```

**To get your API key:**
1. Visit https://console.groq.com
2. Sign up or log in
3. Navigate to API Keys
4. Copy your key to the `.env` file

## 🎮 Running the Chatbot

Start the Streamlit app:

```bash
streamlit run langgraph_frontend.py
```

The application will open automatically in your browser at `http://localhost:8501`

**Usage:**
1. Type your message in the chat input box
2. Press Enter to send
3. Wait for the AI response
4. Chat history persists in the current session

## 📁 File Structure

```
LANGGRAPH-CHATBOT/
├── langgraph_backend.py      # LangGraph workflow and state management
├── langgraph_frontend.py      # Streamlit UI and session handling
├── .env                       # Environment variables (API keys)
└── README.md                  # This file
```

## 🔄 How It Works

### Message Flow

```
User Input (Streamlit)
    ↓
HumanMessage created
    ↓
chatbot.invoke() - invokes the graph
    ↓
chat_node processes message
    ↓
LLM (Qwen3-32B via Groq) generates response
    ↓
Response stored in state
    ↓
Display in chat UI
```

### State Management

The `ChatState` uses LangChain's `add_messages` reducer:
- Automatically appends new messages to the history
- Maintains proper message ordering
- Supports message deduplication

### Thread Persistence

```python
config = {'configurable': {'thread_id': 1}}
```

- Each conversation gets a unique thread ID
- MemorySaver stores state for each thread
- Enables multi-user scenarios (modify thread_id per user)
- State persists across app restarts during development

## 🛠️ Configuration Options

### Customize the LLM

Edit `langgraph_backend.py`:

```python
llm = ChatGroq(
    model="qwen/qwen3-32b",           # Change model here
    temperature=0,                     # 0=deterministic, 1=creative
    max_tokens=None,                   # Set token limit if needed
    reasoning_format="parsed",         # Response format
    max_retries=2,                     # Retry on failure
)
```

**Available Models on Groq:**
- `mixtral-8x7b-32768`
- `llama2-70b-4096`
- `qwen/qwen3-32b` (current)
- And others - check Groq console for latest

### Change Thread ID (for multi-user)

Edit `langgraph_frontend.py`:

```python
# Instead of hardcoded 1, use user identifier:
thread_id = st.session_state.get('user_id', 'default')
config = {'configurable': {'thread_id': thread_id}}
```

## 🔍 Understanding the Code

### Backend Walkthrough

1. **State Definition**
   ```python
   class ChatState(TypedDict):
       messages: Annotated[list[BaseMessage], add_messages]
   ```
   - Defines what data the graph manages

2. **Node Function**
   ```python
   def chat_node(state: ChatState):
       messages = state['messages']
       response = llm.invoke(messages)
       return {'messages': [response]}
   ```
   - Takes current state, processes it, returns updates

3. **Graph Construction**
   ```python
   graph = StateGraph(ChatState)
   graph.add_node('chat_node', chat_node)
   graph.add_edge(START, 'chat_node')
   graph.add_edge('chat_node', END)
   chatbot = graph.compile(checkpointer=checkpointer)
   ```
   - Creates workflow: START → chat_node → END
   - Compiles with memory persistence

### Frontend Walkthrough

1. **Session State Initialization**
   ```python
   if 'message_history' not in st.session_state:
       st.session_state['message_history'] = []
   ```
   - Keeps chat history between interactions

2. **Display History**
   ```python
   for message in st.session_state['message_history']:
       with st.chat_message(message['role']):
           st.text(message['content'])
   ```
   - Renders previous messages

3. **Handle User Input**
   ```python
   if user_input:
       # Add to history
       # Call backend
       # Display response
   ```

## 🚧 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langgraph'`
**Solution:** Install dependencies
```bash
pip install langgraph langchain langchain-groq
```

### Issue: `AuthenticationError` from Groq
**Solution:** Check your `.env` file
- Verify `GROQ_API_KEY` is correct
- Make sure `.env` is in the same directory as the Python files
- Run `python -c "from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('GROQ_API_KEY'))"` to debug

### Issue: Streamlit not opening
**Solution:** Try explicit URL
```bash
streamlit run langgraph_frontend.py --logger.level=debug
```

### Issue: Chat not responding
**Solution:** 
- Check internet connection (Groq API needs it)
- Verify API key has quota
- Check Groq status at https://status.groq.com

## 📚 Learning Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Message Types](https://python.langchain.com/docs/modules/memory/chat_messages/)
- [Streamlit Chat UI](https://docs.streamlit.io/develop/api-reference/chat)
- [Groq API Docs](https://console.groq.com/docs)

## 🎯 Next Steps & Ideas

- [ ] Add system prompts for specific chatbot personalities
- [ ] Implement tool calling / function execution
- [ ] Add conversation reset functionality
- [ ] Support multiple concurrent conversations
- [ ] Add conversation analytics/logging
- [ ] Implement RAG (Retrieval Augmented Generation)
- [ ] Add streaming responses for better UX
- [ ] Database storage instead of in-memory checkpointer

## 💡 Tips for Learning

1. **Modify the prompt** - Add system messages to change chatbot behavior
2. **Try different models** - Experiment with Groq's available models
3. **Inspect state** - Print `state` and `response` to understand data flow
4. **Extend the graph** - Add more nodes for complex workflows
5. **Add memory** - Implement SQLiteSaver instead of MemorySaver for persistence

## 📝 Learning Project Notes

🌱 **This is my first project with LangGraph** - a hands-on learning experience to understand:
- How LangGraph structures workflows with StateGraph
- State management with TypedDict and message reducers
- Building graph nodes and edges
- Memory persistence with checkpointers
- Integrating frontend UI (Streamlit) with backend graphs

**Code written for learning clarity** - focuses on understanding concepts over production optimization. As I progress, I'll apply best practices and more sophisticated patterns.

**Current limitations (intentional for learning):**
- State is stored in memory (lost when app restarts)
- Thread ID is hardcoded (suitable for single-user learning)
- No error handling implemented (will add for production)
- Simple single-node graph (foundation for learning)

---

**Happy Learning! 🚀**  
My journey into building agentic AI systems starts here!
