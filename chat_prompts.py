from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

chat_prompts=ChatPromptTemplate([
    ('system', 'You are helpful {Domain} expert AiAssistant'),
    ('human', 'Explain in simple terms what is {Topic}')
])

prompt=chat_prompts.invoke({'Domain':'Cricket', 'Topic':'Tell me about god of cricket'})

print(prompt)
