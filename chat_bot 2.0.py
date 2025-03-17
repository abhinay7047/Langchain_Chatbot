from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
import datetime
import os

load_dotenv()
llm = ChatOpenAI(verbose=True)

chat_template = ChatPromptTemplate([
    ('system', 'You are a helpful customer service expert, which is expert in reimbursement inquiries'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human', 'when will I get my {Topic} reimbursement')
])

chat_history = []

# Load chat history from file
if os.path.exists('chat_history.txt'):
    try:
        with open('chat_history.txt') as f:
            chat_history.extend(f.readlines())
    except Exception as e:
        print(f"Error reading chat history: {e}")

# Get dynamic topic input from user
topic = input("Enter the topic for reimbursement inquiry: ")

# Create prompt and get response from LLM
try:
    prompt = chat_template.invoke({'chat_history': chat_history, 'Topic': HumanMessage(content=topic)})
    result = llm.invoke(prompt)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_history.append(f"{timestamp} - {topic}\n")
    chat_history.append(f"{timestamp} - {result.content}\n")

except Exception as e:
    print(f"Error during LLM invocation: {e}")

# Save updated chat history to file
try:
    with open('chat_history.txt', 'w') as f:
        f.writelines(chat_history)
except Exception as e:
    print(f"Error writing chat history: {e}")

print(chat_history)