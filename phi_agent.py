from phi.agent import Agent, RunResponse
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq

agent=Agent(
    model=Groq(id='llama-3.3-70b-versatile', verbose=True),
    tools=[DuckDuckGo(news=True), YFinanceTools(stock_fundamentals=True,company_news=True,key_financial_ratios=True,
                                                technical_indicators=True, analyst_recommendations=True
                                       )],
    description='You are a senior stock news analyzer who is expert in giving stock buying advice'
        ' with the help of current news, financial ratio and techinal indicators of Stock. '
        ,
    instructions=[
        'for the given stock, Analyze the current news and financial ratios and provide the buying advice'
        'and the reason for the same.'
        'Also provide the major shareholders and intutional holding of the company'
    ],
    markdown=True,
    verbose=True,
    provider=Groq(id='llama3-8b-8192', verbose=True)
)

agent.print_response('ANGELONE.NS', stream=True)


