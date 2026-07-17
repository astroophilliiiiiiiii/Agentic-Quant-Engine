import os
import subprocess
import yfinance as yf
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# --- STREAMLIT PAGE CONFIGURATION ---
st.set_page_config(page_title="Agentic Quant Analyst", page_icon="📈", layout="centered")

st.title("📈 Multi-Agent Financial Analyst")
st.markdown("**Autonomous Investment Strategist Powered by CrewAI & Custom C++ Engine**")
st.markdown("---")

# --- BACKEND LOGIC (Your existing code wrapped in a function) ---
def run_financial_analysis(ticker):
    llm = LLM(
        model="gemini/gemini-3.5-flash", # Corrected to 1.5 Flash
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    @tool("Web Searcher")
    def web_search(query: str) -> str:
        """Searches the internet for real-time news and data about a company."""
        search_tool = DuckDuckGoSearchRun()
        return search_tool.run(query)

    @tool("YFinance Market Data Fetcher")
    def fetch_stock_data(ticker_symbol: str) -> str:
        """Fetches real-time stock price and historical 1-month data for a given ticker."""
        stock = yf.Ticker(ticker_symbol)
        hist = stock.history(period="1mo")
        if hist.empty:
            return f"Could not fetch data for {ticker_symbol}."
        
        current_price = hist['Close'].iloc[-1]
        recent_prices = ",".join([str(round(p, 2)) for p in hist['Close'].tolist()])
        return f"Current Price: {current_price}\nRecent 1-Month Prices: {recent_prices}"

    @tool("C++ Max Drawdown Calculator")
    def calculate_risk_cpp(price_history: str) -> str:
        """Passes a comma-separated list of stock prices to a compiled C++ engine."""
        try:
            result = subprocess.run(['engine.exe', price_history], capture_output=True, text=True, check=True)
            return f"C++ Engine Calculated Max Drawdown: {result.stdout.strip()}%"
        except Exception as e:
            return f"Execution failed: {str(e)}"

    data_engineer = Agent(
        role="Senior Market Data Engineer",
        goal="Extract real-time stock prices and recent historical price strings for {company_ticker} using YFinance.",
        backstory="You fetch clean API data. You output exact numerical values and comma-separated price lists.",
        tools=[fetch_stock_data],
        verbose=True,
        llm=llm
    )

    quant_analyst = Agent(
        role="Quantitative Risk Analyst",
        goal="Take the price history from the data engineer and run the C++ Max Drawdown Calculator tool to evaluate risk.",
        backstory="You are a strict quant. You rely on high-performance C++ algorithms to assess financial risk.",
        tools=[calculate_risk_cpp],
        verbose=True,
        llm=llm
    )

    investment_strategist = Agent(
        role="Lead Investment Strategist",
        goal="Search the web for the latest news on {company_ticker} and combine it with the quant's risk data to write a final investment memo.",
        backstory="You write executive summaries for portfolio managers, blending market news with hard algorithmic data.",
        tools=[web_search],
        verbose=True,
        llm=llm
    )

    task1 = Task(
        description="Fetch the live stock data and 1-month price history for {company_ticker}.",
        expected_output="A structured report containing the Current Price and the comma-separated 1-Month Price History.",
        agent=data_engineer
    )

    task2 = Task(
        description="Extract the comma-separated price history from Task 1 and pass it to your C++ Max Drawdown Calculator tool. Determine the risk percentage.",
        expected_output="The exact Max Drawdown percentage calculated by the C++ engine.",
        agent=quant_analyst
    )

    task3 = Task(
        description="Search the web for recent news regarding {company_ticker}. Write a 3-paragraph Markdown report combining the news sentiment, the current stock price, and the C++ risk metric.",
        expected_output="A formatted Markdown investment memo.",
        agent=investment_strategist
    )

    fin_crew = Crew(
        agents=[data_engineer, quant_analyst, investment_strategist],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        verbose=True
    )
    
    return fin_crew.kickoff(inputs={"company_ticker": ticker})

# --- FRONTEND UI COMPONENTS ---
ticker_input = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, RELIANCE.NS):").upper()

if st.button("Generate Executive Memo"):
    if ticker_input:
        with st.spinner(f"Agents are analyzing data for {ticker_input}... This might take a minute."):
            try:
                # Trigger the CrewAI execution
                final_result = run_financial_analysis(ticker_input)
                
                # Display the results
                st.success("Analysis Complete!")
                st.markdown("### 📋 Final Executive Memo")
                st.markdown(final_result.raw) # `.raw` extracts the string output from CrewAI
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a ticker symbol first.")