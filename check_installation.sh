#!/bin/bash

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "==================================="
echo "Git-Komet Installation Checker"
echo "==================================="
echo ""

# Проверка Python
echo -n "Checking Python... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}✓ Found Python $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 not found${NC}"
fi

# Проверка Node.js
echo -n "Checking Node.js... "
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Found Node.js $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found${NC}"
fi

# Проверка npm
echo -n "Checking npm... "
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✓ Found npm $NPM_VERSION${NC}"
else
    echo -e "${RED}✗ npm not found${NC}"
fi

# Проверка Git
echo -n "Checking Git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "${GREEN}✓ Found Git $GIT_VERSION${NC}"
else
    echo -e "${RED}✗ Git not found${NC}"
fi

# Проверка Docker (опционально)
echo -n "Checking Docker (optional)... "
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    echo -e "${GREEN}✓ Found Docker $DOCKER_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Docker not found (optional)${NC}"
fi

# Проверка Docker Compose (опционально)
echo -n "Checking Docker Compose (optional)... "
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version | awk '{print $3}' | tr -d ',')
    echo -e "${GREEN}✓ Found Docker Compose $COMPOSE_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Docker Compose not found (optional)${NC}"
fi

echo ""
echo "==================================="
echo "Installation Status"
echo "==================================="

# Проверка backend зависимостей
echo ""
echo "Backend (Python) dependencies:"
if [ -d "backend" ]; then
    if [ -f "backend/requirements.txt" ]; then
        echo -e "${GREEN}✓ requirements.txt found${NC}"
    else
        echo -e "${RED}✗ requirements.txt not found${NC}"
    fi
    
    if [ -f "backend/.env" ]; then
        echo -e "${GREEN}✓ .env configured${NC}"
    else
        echo -e "${YELLOW}⚠ .env not found - copy from .env.example${NC}"
    fi
else
    echo -e "${RED}✗ backend directory not found${NC}"
fi

# Проверка frontend зависимостей
echo ""
echo "Frontend (Node.js) dependencies:"
if [ -d "frontend" ]; then
    if [ -f "frontend/package.json" ]; then
        echo -e "${GREEN}✓ package.json found${NC}"
    else
        echo -e "${RED}✗ package.json not found${NC}"
    fi
    
    if [ -d "frontend/node_modules" ]; then
        echo -e "${GREEN}✓ node_modules installed${NC}"
    else
        echo -e "${YELLOW}⚠ node_modules not found - run 'npm install' in frontend/${NC}"
    fi
    
    if [ -f "frontend/.env" ]; then
        echo -e "${GREEN}✓ .env configured${NC}"
    else
        echo -e "${YELLOW}⚠ .env not found - copy from .env.example${NC}"
    fi
else
    echo -e "${RED}✗ frontend directory not found${NC}"
fi

echo ""
echo "==================================="
echo "Next Steps"
echo "==================================="
echo ""
echo "1. Backend setup:"
echo "   cd backend"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   pip install -r requirements.txt"
echo "   cp .env.example .env"
echo "   python init_db.py"
echo "   python run.py"
echo ""
echo "2. Frontend setup (in a new terminal):"
echo "   cd frontend"
echo "   npm install"
echo "   cp .env.example .env"
echo "   npm run dev"
echo ""
echo "3. Or use Docker:"
echo "   docker-compose up --build"
echo ""
echo "For more details, see QUICKSTART.md"
