#!/bin/bash
# Quick Setup Script for Fresh Start

echo "🚀 Smart Patient Health Assistant - Setup Script"
echo "=================================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.12 -m venv venv || python3 -m venv venv
    echo "✅ Virtual environment created!"
    echo ""
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel -q

# Install requirements
echo "📥 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt -q

# Install streamlit if not present
echo "📥 Installing Streamlit..."
pip install streamlit -q

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the virtual environment: source venv/bin/activate"
echo "   2. Run the app: ./start.sh"
echo ""
echo "   OR use: ./start.sh (it will auto-activate venv)"
echo ""
