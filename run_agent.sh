#!/bin/bash

echo "=========================================="
echo "Finance Agent - Setup & Run"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Install Python 3.8+"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Run agent
echo "=========================================="
echo "Starting Finance Agent..."
echo "=========================================="
echo ""

python3 finance_agent.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Agent completed successfully!"
    echo "📄 Check audit_log.json for detailed results"
else
    echo ""
    echo "❌ Agent failed. Check error messages above."
    exit 1
fi
