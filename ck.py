from phi.agent import Agent, RunResponse
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from dotenv import load_dotenv
import os       
load_dotenv()

agent=Agent(
    model=OpenAIChat(id='gpt-4o', verbose=True),
    tools=[DuckDuckGo(news=True), YFinanceTools(stock_fundamentals=True,company_news=True,key_financial_ratios=True,
                                                technical_indicators=True, analyst_recommendations=True
                                       )],
    description='You are a senior stock news analyzer who is expert in giving stock buying advice'
        ' with the help of current news, financial ratio and techinal indicators of Stock.'
        
        ,
    instructions=[
        'for the given stock, Analyze the current news and financial ratios and provide the buying advice'
        'and the reason for the same.'
        'Also provide the major shareholders and intutional holding (stats of FIS and DIS) of the company'
        'give me target price and its setiment'
    ],
    markdown=True,
    verbose=True,
)

agent.print_response('SBIN.NS', stream=True)


