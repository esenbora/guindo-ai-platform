from crewai import Agent
from langchain_groq import ChatGroq
from tools import search_web, export_data
import yaml


def create_market_watcher(llm: ChatGroq) -> Agent:
    """Create market_watcher agent."""
    
    with open('config/agents.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    agent_config = config['market_watcher']
    
    return Agent(
        role=agent_config['role'],
        goal=agent_config['goal'],
        backstory=agent_config['backstory'],
        verbose=agent_config['verbose'],
        allow_delegation=agent_config['allow_delegation'],
        llm=llm,
        tools=[search_web, export_data]
    )
