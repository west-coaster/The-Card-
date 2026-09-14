#!/bin/bash

# Single AI Model - Quick Setup & Run

echo "🚀 THE CARD - Single AI Model Setup"
echo "===================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✓ Python version: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

echo "✓ Virtual environment created"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements-ai.txt

echo "✓ Dependencies installed"

# Copy environment file
echo ""
echo "Setting up configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✓ Created .env file"
    echo "⚠️  Please edit .env with your Supabase credentials!"
else
    echo "✓ .env already exists"
fi

# Create logs directory
mkdir -p logs

echo ""
echo "===================================="
echo "✓ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your Supabase URL and API key"
echo "2. Run: python ai_orchestrator.py"
echo ""
echo "The AI model will:"
echo "  - Fetch data every 5 minutes"
echo "  - Run AI analysis"
echo "  - Push to Supabase"
echo "  - Broadcast to all users"
echo "===================================="
