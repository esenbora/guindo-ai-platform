from crewai_tools import BaseTool
from typing import Type, Dict, List
from pydantic import BaseModel, Field
import pandas as pd


class CalculatorInput(BaseModel):
    """Input for ROI Calculator."""
    scenarios: List[Dict] = Field(
        ..., 
        description="List of education/career scenarios to analyze"
    )
    years: int = Field(default=15, description="Time horizon in years")
    discount_rate: float = Field(default=0.05, description="Discount rate for NPV")


class ROICalculatorTool(BaseTool):
    name: str = "ROI Calculator Tool"
    description: str = (
        "Calculates Return on Investment for education and career decisions. "
        "Computes NPV, total earnings, and comparison metrics."
    )
    args_schema: Type[BaseModel] = CalculatorInput

    def _run(
        self, 
        scenarios: List[Dict], 
        years: int = 15, 
        discount_rate: float = 0.05
    ) -> str:
        """Calculate ROI for different scenarios."""
        try:
            results = []
            
            for scenario in scenarios:
                name = scenario.get('name', 'Unknown')
                education_years = scenario.get('education_years', 0)
                education_cost = scenario.get('education_cost', 0)
                starting_salary = scenario.get('starting_salary', 30000)
                annual_raise = scenario.get('annual_raise', 0.10)
                
                # Calculate earnings
                working_years = years - education_years
                total_earnings = 0
                npv = -education_cost  # Initial investment
                
                for year in range(working_years):
                    yearly_salary = starting_salary * ((1 + annual_raise) ** year)
                    total_earnings += yearly_salary
                    
                    # Discount future earnings
                    discount_factor = 1 / ((1 + discount_rate) ** (year + education_years))
                    npv += yearly_salary * discount_factor
                
                results.append({
                    'Scenario': name,
                    'Education Years': education_years,
                    'Education Cost': f"${education_cost:,.0f}",
                    'Working Years': working_years,
                    'Total Earnings': f"${total_earnings:,.0f}",
                    'NPV': f"${npv:,.0f}",
                    'Final Salary': f"${starting_salary * ((1 + annual_raise) ** (working_years - 1)):,.0f}"
                })
            
            # Create DataFrame for better formatting
            df = pd.DataFrame(results)
            return df.to_string(index=False)
            
        except Exception as e:
            return f"Error in ROI calculation: {str(e)}"
