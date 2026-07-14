import os
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_groq import ChatGroq
from src.prompt_templates import INVENTORY_AGENT_PREFIX

def get_inventory_agent():
    CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'inventory', 'stok_obat.csv')
    
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"File data tidak ditemukan di: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile", 
        temperature=0
    )
    
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        prefix=INVENTORY_AGENT_PREFIX,
        verbose=True,
        agent_type="tool-calling", 
        allow_dangerous_code=True
    )
    
    return agent