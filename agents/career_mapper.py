from crewai import Agent
from langchain_groq import ChatGroq
from tools import search_web, export_data
import yaml


def create_career_mapper(llm: ChatGroq) -> Agent:
    """Create Career Mapper agent."""
    
    with open('config/agents.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    agent_config = config['career_mapper']
    
    return Agent(
        role=agent_config['role'],
        goal=agent_config['goal'],
        backstory=agent_config['backstory'],
        verbose=agent_config['verbose'],
        allow_delegation=agent_config['allow_delegation'],
        llm=llm,
        tools=[search_web, export_data]
    )
