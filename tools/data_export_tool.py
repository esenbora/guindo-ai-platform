from crewai_tools import BaseTool
from typing import Type, Any
from pydantic import BaseModel, Field
import pandas as pd
import os
from datetime import datetime


class ExportInput(BaseModel):
    """Input for Data Export Tool."""
    data: str = Field(..., description="Data to export (CSV, JSON, or text format)")
    filename: str = Field(..., description="Output filename")
    format: str = Field(default="csv", description="Export format: csv, xlsx, md")


class DataExportTool(BaseTool):
    name: str = "Data Export Tool"
    description: str = (
        "Exports data to various formats (CSV, Excel, Markdown). "
        "Saves files to the outputs directory."
    )
    args_schema: Type[BaseModel] = ExportInput

    def _run(self, data: str, filename: str, format: str = "csv") -> str:
        """Export data to specified format."""
        try:
            # Ensure output directory exists
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            # Add timestamp to filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = filename.rsplit('.', 1)[0]
            file_path = os.path.join(output_dir, f"{base_name}_{timestamp}.{format}")
            
            if format == "csv":
                # Try to parse as CSV
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
                    
            elif format == "xlsx":
                # Convert to DataFrame and save as Excel
                try:
                    df = pd.read_csv(pd.compat.StringIO(data))
                    df.to_excel(file_path, index=False, engine='openpyxl')
                except:
                    # If not CSV format, save as text in Excel
                    df = pd.DataFrame({'Data': [data]})
                    df.to_excel(file_path, index=False, engine='openpyxl')
                    
            elif format == "md":
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
            else:
                return f"Unsupported format: {format}"
            
            return f"Successfully exported to {file_path}"
            
        except Exception as e:
            return f"Error exporting data: {str(e)}"
