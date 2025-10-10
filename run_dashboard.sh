#!/bin/bash
# Quick start script for Clio KPI Dashboard

set -e

echo "=========================================="
echo "🚀 Clio KPI Dashboard Launcher"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt
echo "✅ Dependencies installed"

# Check if database exists
DB_PATH="../dashboard-neo4j/data/analytics/clio-analytics.db"
if [ ! -f "$DB_PATH" ]; then
    echo "⚠️  Warning: Database not found at $DB_PATH"
    echo "    The dashboard will run with mock data"
else
    echo "✅ Database found: $DB_PATH"
fi

# Set environment variables
export DASH_PORT="${DASH_PORT:-8050}"
export DASH_DEBUG="${DASH_DEBUG:-True}"

echo ""
echo "=========================================="
echo "🎯 Starting Dashboard"
echo "=========================================="
echo ""
echo "📍 URL: http://localhost:$DASH_PORT"
echo "🔧 Debug Mode: $DASH_DEBUG"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run dashboard
python3 dash_clio_dashboard/app.py
