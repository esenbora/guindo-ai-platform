from crewai import Agent
from langchain_groq import ChatGroq
from tools import search_web, export_data
import yaml


def create_fire_planner(llm: ChatGroq) -> Agent:
    """Create fire_planner agent."""
    
    with open('config/agents.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    agent_config = config['fire_planner']
    
    return Agent(
        role=agent_config['role'],
        goal=agent_config['goal'],
        backstory=agent_config['backstory'],
        verbose=agent_config['verbose'],
        allow_delegation=agent_config['allow_delegation'],
        llm=llm,
        tools=[search_web, export_data]
    )
