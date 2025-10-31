#!/bin/bash

# Development startup script for AI Image Generator Bot backend
# Usage: ./run_dev.sh

set -e  # Exit on error

echo "🚀 Starting AI Image Generator Bot backend (development mode)..."
echo ""

# Change to backend directory
cd "$(dirname "$0")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# 2. Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# 3. Check if dependencies are installed
if [ ! -f "venv/lib/python*/site-packages/fastapi/__init__.py" ]; then
    echo -e "${YELLOW}⚠️  Dependencies not found. Installing...${NC}"
    pip install --upgrade pip
    pip install -r requirements.txt
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

# 4. Check .env file
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env file not found!${NC}"
    echo "Please create .env file from .env.example:"
    echo "  cp .env.example .env"
    echo "  # Then edit .env with your API keys"
    exit 1
fi

echo -e "${GREEN}✅ .env file found${NC}"

# 5. Check if PostgreSQL and Redis are running
echo ""
echo "🔍 Checking database connections..."

# Check PostgreSQL
if ! pg_isready -h localhost -p 5432 > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  PostgreSQL not running!${NC}"
    echo "Start it with:"
    echo "  docker-compose -f ../docker-compose.dev.yml up -d postgres"
    echo ""
    read -p "Do you want to start PostgreSQL now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd ..
        docker-compose -f docker-compose.dev.yml up -d postgres
        cd backend
        echo "Waiting for PostgreSQL to start..."
        sleep 5
    else
        exit 1
    fi
fi

echo -e "${GREEN}✅ PostgreSQL is running${NC}"

# Check Redis
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Redis not running!${NC}"
    echo "Start it with:"
    echo "  docker-compose -f ../docker-compose.dev.yml up -d redis"
    echo ""
    read -p "Do you want to start Redis now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd ..
        docker-compose -f docker-compose.dev.yml up -d redis
        cd backend
        echo "Waiting for Redis to start..."
        sleep 3
    else
        exit 1
    fi
fi

echo -e "${GREEN}✅ Redis is running${NC}"

# 6. Run Alembic migrations
echo ""
echo "📊 Applying database migrations..."

# Check if alembic is initialized
if [ ! -d "alembic/versions" ]; then
    echo -e "${YELLOW}⚠️  No migrations found. Creating initial migration...${NC}"
    alembic revision --autogenerate -m "Initial migration"
fi

# Apply migrations
alembic upgrade head

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migrations applied successfully${NC}"
else
    echo -e "${RED}❌ Migration failed!${NC}"
    exit 1
fi

# 7. Start uvicorn server
echo ""
echo "🌟 Starting FastAPI server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Backend is starting...${NC}"
echo ""
echo "📍 API will be available at: http://localhost:8000"
echo "📖 API Docs at: http://localhost:8000/docs"
echo "🔄 Auto-reload is enabled"
echo ""
echo "Press Ctrl+C to stop the server"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Start server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
