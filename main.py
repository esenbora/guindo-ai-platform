#!/usr/bin/env python3
"""
Early Retirement Agentic Workflow System
Main orchestration file for CrewAI agents
"""

import os
import yaml
from dotenv import load_dotenv
from crewai import Crew, Task, Process
from langchain_groq import ChatGroq

# Import agent creators
from agents import (
    create_career_mapper,
    create_roi_analyzer,
    create_fire_planner,
    create_market_watcher
)


def load_tasks_config():
    """Load tasks from YAML configuration."""
    with open('config/tasks.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def setup_llm():
    """Initialize the LLM."""
    return ChatGroq(
        model=os.getenv('LLM_MODEL', 'llama-3.3-70b-versatile'),
        temperature=float(os.getenv('LLM_TEMPERATURE', 0.7)),
        max_tokens=int(os.getenv('LLM_MAX_TOKENS', 4096)),
        groq_api_key=os.getenv('GROQ_API_KEY')
    )


def create_tasks(agents_dict, tasks_config):
    """Create Task objects from configuration."""
    tasks = []
    
    # Task 1: Research Career Paths
    career_task = Task(
        description=tasks_config['research_career_paths']['description'],
        expected_output=tasks_config['research_career_paths']['expected_output'],
        agent=agents_dict['career_mapper']
    )
    tasks.append(career_task)
    
    # Task 2: Analyze Education ROI
    roi_task = Task(
        description=tasks_config['analyze_education_roi']['description'],
        expected_output=tasks_config['analyze_education_roi']['expected_output'],
        agent=agents_dict['roi_analyzer'],
        context=[career_task]  # Depends on career research
    )
    tasks.append(roi_task)
    
    # Task 3: Create FIRE Plan
    fire_task = Task(
        description=tasks_config['create_fire_plan']['description'],
        expected_output=tasks_config['create_fire_plan']['expected_output'],
        agent=agents_dict['fire_planner'],
        context=[career_task, roi_task]  # Depends on both previous tasks
    )
    tasks.append(fire_task)
    
    # Task 4: Discover Income Streams
    market_task = Task(
        description=tasks_config['discover_income_streams']['description'],
        expected_output=tasks_config['discover_income_streams']['expected_output'],
        agent=agents_dict['market_watcher']
    )
    tasks.append(market_task)
    
    return tasks


def main():
    """Main execution function."""
    print("🚀 Early Retirement Agentic Workflow System")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Validate API keys
    if not os.getenv('GROQ_API_KEY'):
        print("❌ Error: GROQ_API_KEY not found in .env file")
        print("Please create a .env file and add your API keys.")
        return
    
    if not os.getenv('SERPER_API_KEY'):
        print("⚠️  Warning: SERPER_API_KEY not found. Web search may not work.")
    
    # Initialize LLM
    print("\n🧠 Initializing LLM...")
    llm = setup_llm()
    
    # Create agents
    print("🤖 Creating agents...")
    agents_dict = {
        'career_mapper': create_career_mapper(llm),
        'roi_analyzer': create_roi_analyzer(llm),
        'fire_planner': create_fire_planner(llm),
        'market_watcher': create_market_watcher(llm)
    }
    
    # Load tasks configuration
    print("📋 Loading tasks configuration...")
    tasks_config = load_tasks_config()
    
    # Create tasks
    print("✅ Creating tasks pipeline...")
    tasks = create_tasks(agents_dict, tasks_config)
    
    # Create crew
    print("👥 Assembling crew...")
    crew = Crew(
        agents=list(agents_dict.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    
    # Execute workflow
    print("\n" + "=" * 60)
    print("🎯 Starting workflow execution...")
    print("=" * 60 + "\n")
    
    try:
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("✅ Workflow completed successfully!")
        print("=" * 60)
        print("\n📊 Results:")
        print(result)
        
        print("\n📁 Output files have been generated in the 'outputs/' directory:")
        print("   - career_paths_*.csv")
        print("   - education_vs_work_*.xlsx")
        print("   - retirement_plan_*.md")
        print("   - microbusiness_report_*.md")
        
    except Exception as e:
        print(f"\n❌ Error during workflow execution: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
