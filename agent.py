import streamlit as st
import google.generativeai as genai

# Configure Google Generative AI API
API_KEY = "AIzaSyA-9-lTQTWdNM43YdOXMQwGKDy0SrMwo6c"
genai.configure(api_key=API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit page configuration
st.set_page_config(page_title="Task-Based AI Agent", page_icon="⚙️", layout="centered")

# Initialize session state for task history
if "task_history" not in st.session_state:
    st.session_state.task_history = []

# Title and description
st.title("⚙️ Task-Based AI Agent")
st.markdown("This AI agent can perform tasks like answering questions, summarizing text, generating ideas, or translating. Select a task or type a command!")

# Task definitions
TASKS = {
    "answer": {
        "description": "Answer a question or provide information.",
        "keywords": ["what", "why", "how", "who", "when", "where", "answer", "explain"],
        "prompt_template": "Provide a concise and accurate answer to the following question: {input}"
    },
    "summarize": {
        "description": "Summarize a given text.",
        "keywords": ["summarize", "summary", "brief", "condense"],
        "prompt_template": "Summarize the following text in 2-3 sentences: {input}"
    },
    "generate": {
        "description": "Generate ideas or creative content.",
        "keywords": ["generate", "ideas", "suggest", "create", "brainstorm"],
        "prompt_template": "Generate 3-5 creative ideas or suggestions for: {input}"
    },
    "translate": {
        "description": "Translate text to a specified language.",
        "keywords": ["translate", "translation", "convert", "language"],
        "prompt_template": "Translate the following text to {language}: {input}"
    }
}

# Function to identify task from input
def identify_task(user_input):
    user_input = user_input.lower().strip()
    for task, details in TASKS.items():
        if any(keyword in user_input for keyword in details["keywords"]):
            return task
    return "answer"  # Default task if no specific task is identified

# Function to process task with Gemini model
def process_task(task, user_input):
    try:
        # Handle translate task specifically
        if task == "translate":
            # Extract language (assume it's specified in input, e.g., "translate to Spanish")
            language = "English"  # Default
            for lang in ["spanish", "french", "german", "italian", "chinese", "japanese"]:
                if lang in user_input.lower():
                    language = lang.capitalize()
                    break
            prompt = TASKS[task]["prompt_template"].format(input=user_input, language=language)
        else:
            prompt = TASKS[task]["prompt_template"].format(input=user_input)
        
        # Generate response using Gemini model
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Task selection and input form
st.subheader("Select or Type Your Task")
task_option = st.selectbox("Choose a task:", [""] + list(TASKS.keys()), format_func=lambda x: TASKS[x]["description"] if x else "Select a task")
with st.form(key="task_form", clear_on_submit=True):
    user_input = st.text_area("Your Input:", placeholder="E.g., 'What is AI?' or 'Summarize this text...'")
    submit_button = st.form_submit_button("Execute Task")

# Handle task submission
if submit_button and user_input:
    # Determine task: use selected task if provided, otherwise identify from input
    task = task_option if task_option else identify_task(user_input)
    
    # Process task and get response
    result = process_task(task, user_input)
    
    # Append to task history
    st.session_state.task_history.append({
        "task": task,
        "input": user_input,
        "output": result
    })

# Display task history
st.subheader("Task History")
if st.session_state.task_history:
    for idx, entry in enumerate(st.session_state.task_history, 1):
        with st.expander(f"Task {idx}: {entry['task'].capitalize()}"):
            st.markdown(f"**Input:** {entry['input']}")
            st.markdown(f"**Output:** {entry['output']}")
else:
    st.write("No tasks completed yet. Submit a task to see results!")

# Button to clear task history
if st.button("Clear Task History"):
    st.session_state.task_history = []
    st.experimental_rerun()
