# 📈 Agentic-Quant-Engine

## 🚀 Overview
**Agentic-Quant-Engine** is an autonomous, multi-agent financial analysis system. It leverages AI not just for text generation, but for **tool orchestration**. 

Instead of relying on a single LLM prompt that might hallucinate math, this system coordinates three specialized AI agents to fetch real-time market data, run risk algorithms via a custom C++ engine, and synthesize live news into an executive investment memo.

## 🧠 How It Works (The Architecture)
This project uses **CrewAI** to manage three distinct agents in a sequential pipeline:

1. **The Data Engineer (yFinance API):** Fetches real-time stock prices and a 1-month historical price array for any public ticker.
2. **The Quant Analyst (C++ Execution):** LLMs are bad at math, so this agent deterministicly passes the price array to a compiled **C++ Engine** to calculate the Maximum Drawdown (risk metric) in $O(N)$ time.
3. **The Investment Strategist (DuckDuckGo Web Search):** Scrapes the live web for the latest company news, blends it with the C++ risk data, and writes the final markdown report.

## 🛠️ Tech Stack
* **Agent Orchestration:** CrewAI, LangChain Tools
* **LLM Core:** Google Gemini 3.5 Flash
* **Algorithmic Engine:** C++ (for high-speed array processing)
* **Frontend:** Streamlit 
* **Data Sources:** yFinance, DuckDuckGo Search

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/astroophilliiiiiiiii/Agentic-Quant-Engine
cd Agentic-Quant-Engine
