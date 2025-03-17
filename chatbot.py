from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
load_dotenv ()
llm=ChatOpenAI(verbose=True)
chat_history=[
    SystemMessage(content='You are helpful and kind AiAssistant'),
    HumanMessage(content='Tell me about Langchain'),
]
while True:
    user_input=input('YOU: ')
    chat_history.append(HumanMessage(content=user_input))
    if user_input=='exit':
        break
    result=llm.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    print('BOT:',result.content)
print(chat_history)