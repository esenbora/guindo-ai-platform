#!/bin/bash

echo "🚀 Setting up Early Retirement Agentic Workflow System"
echo "======================================================"

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env and add your API keys:"
    echo "   - GROQ_API_KEY (get from https://console.groq.com/keys)"
    echo "   - SERPER_API_KEY (get from https://serper.dev/api-key)"
fi

# Create outputs directory
mkdir -p outputs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the workflow: python main.py"
