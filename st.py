import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from phi.agent import Agent, RunResponse
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Stock Analysis Assistant",
    page_icon="📈",
    layout="wide"
)

# App title and description
st.title("📊 Stock Analysis Assistant")
st.markdown("""
This application provides expert stock buying advice based on current news, 
financial ratios, and technical indicators. Enter a stock ticker to get a comprehensive analysis.
""")

# Sidebar for configuration
st.sidebar.header("Configuration")

# Model selection
model_option = st.sidebar.selectbox(
    "Select AI Model",
    ["gpt-4o", "groq-llama3-70b", "gpt-3.5-turbo"]
)

# Create placeholder for API key input
api_key = st.sidebar.text_input("OpenAI API Key (optional)", type="password")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# Function to create agent with selected model
def create_agent(model_name):
    if "groq" in model_name.lower():
        model = Groq(id=model_name)
    else:
        model = OpenAIChat(id=model_name, verbose=True)
    
    return Agent(
        model=model,
        tools=[
            DuckDuckGo(news=True), 
            YFinanceTools(
                stock_fundamentals=True,
                company_news=True,
                key_financial_ratios=True,
                technical_indicators=True, 
                analyst_recommendations=True
            )
        ],
        description='You are a senior stock news analyzer who is expert in giving stock buying advice'
        ' with the help of current news, financial ratios and technical indicators of Stock.',
        instructions=[
            'For the given stock, analyze the current news and financial ratios and provide the buying advice'
            ' and the reason for the same.',
            'Also provide the name of major shareholders and name of institutional holdings of the company',
            'Give me target price and its sentiment',
            'Format your response in markdown with clear sections for News Analysis, Financial Analysis, Technical Analysis, and Recommendation'
        ],
        markdown=True,
        verbose=False,
    )

# Main area for stock input - centered layout
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
stock_symbol = st.text_input("Enter Stock Symbol (e.g., TSLA, AAPL, MSFT)", "TSLA", key="stock_input")
analyze_button = st.button("Analyze Stock", type="primary", key="analyze_button")
st.markdown("</div>", unsafe_allow_html=True)

# Analysis section
if analyze_button:
    if not stock_symbol:
        st.error("Please enter a stock symbol")
    else:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Show loading message
        status_text.text("Creating agent...")
        progress_bar.progress(10)
        
        try:
            # Create agent with selected model
            agent = create_agent(model_option)
            status_text.text("Fetching stock data...")
            progress_bar.progress(30)
            
            # Get stock basic info for header
            with st.spinner("Getting stock information..."):
                progress_bar.progress(50)
                status_text.text("Analyzing stock data...")
                
                # Get agent response
                response = agent.run(stock_symbol)
                progress_bar.progress(90)
                status_text.text("Formatting results...")
                
                # Display the results
                progress_bar.progress(100)
                status_text.text("Analysis complete!")
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                # Center the analysis results
                st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 10, 1])
                with col2:
                    st.markdown("## Analysis Results")
                    st.markdown(response.content)
                st.markdown("</div>", unsafe_allow_html=True)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Make sure you have valid API keys in your .env file or entered in the sidebar.")

# Add a stock price chart widget - Fixed indentation issue
if stock_symbol:
    st.markdown("---")
    st.subheader("Recent Stock Performance")
    
    date_range = st.selectbox(
        "Select Time Range",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        index=2
    )
    
    chart_placeholder = st.empty()
    
    try:
        # Fixed indentation by using a proper string without leading spaces
        import yfinance as yf
        
        # Get stock data directly without exec()
        data = yf.download(stock_symbol, period=date_range)
        
        # Create figure
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name=stock_symbol
        )])
        
        fig.update_layout(
            title=f'{stock_symbol} Stock Price',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            xaxis_rangeslider_visible=False,
            height=500
        )
        
        # Display the figure
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load chart: {str(e)}")

# Add historical comparison tool - Fixed indentation issues
st.markdown("---")
st.subheader("Compare Multiple Stocks")

# Get comparison stocks
comparison_symbols = st.text_input("Enter stock symbols separated by commas (e.g., TSLA,AAPL,MSFT)", "TSLA,AAPL,MSFT")
comparison_period = st.selectbox("Comparison Period", ["1mo", "3mo", "6mo", "1y"], index=2)

if st.button("Compare Stocks"):
    symbols = [s.strip() for s in comparison_symbols.split(",")]
    
    with st.spinner("Generating comparison..."):
        try:
            # Create comparison chart directly without exec()
            import yfinance as yf
            
            # Get normalized stock data for comparison
            fig = go.Figure()
            for symbol in symbols:
                data = yf.download(symbol, period=comparison_period)
                # Normalize to initial value
                normalized_data = data['Close'] / data['Close'].iloc[0] * 100
                fig.add_trace(go.Scatter(
                    x=data.index,
                    y=normalized_data,
                    mode='lines',
                    name=symbol
                ))
            
            fig.update_layout(
                title='Normalized Stock Comparison (Starting Value = 100)',
                xaxis_title='Date',
                yaxis_title='Normalized Value',
                height=500
            )
            
            # Display the figure
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Could not generate comparison: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 10px; font-size: 0.8em;">
This app is for educational purposes only. Not financial advice.
</div>
""", unsafe_allow_html=True)