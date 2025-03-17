from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
load_dotenv ()
llm=ChatOpenAI(verbose=True)
msg=[
    SystemMessage(content='You are helpful and kind AiAssistant'),
    HumanMessage(content='Tell me about Langchain'),
]
result=llm.invoke(msg)
msg.append(AIMessage(content=result.content))
print(msg)