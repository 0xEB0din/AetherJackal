#!/usr/bin/env bash
#
# migrate.sh - Helper script for running CloudMigrate Pro locally
#
# Usage:
#   ./scripts/migrate.sh setup     - Install dependencies
#   ./scripts/migrate.sh dev       - Start dev servers (backend + frontend)
#   ./scripts/migrate.sh test      - Run all tests
#   ./scripts/migrate.sh docker    - Build and run via Docker Compose
#   ./scripts/migrate.sh clean     - Tear down containers and temp files

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()   { echo -e "${GREEN}[migrate]${NC} $*"; }
warn()  { echo -e "${YELLOW}[migrate]${NC} $*"; }
error() { echo -e "${RED}[migrate]${NC} $*" >&2; }

cmd_setup() {
    log "Installing backend dependencies..."
    cd "$PROJECT_ROOT/backend"
    pip install -r requirements.txt

    log "Installing frontend dependencies..."
    cd "$PROJECT_ROOT/frontend"
    npm install

    log "Setup complete."
}

cmd_dev() {
    log "Starting backend (port 5000)..."
    cd "$PROJECT_ROOT/backend"
    FLASK_ENV=development python app.py &
    BACKEND_PID=$!

    log "Starting frontend (port 3000)..."
    cd "$PROJECT_ROOT/frontend"
    npm start &
    FRONTEND_PID=$!

    trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
    log "Dev servers running. Press Ctrl+C to stop."
    wait
}

cmd_test() {
    log "Running backend tests..."
    cd "$PROJECT_ROOT/backend"
    python -m pytest tests/ -v --tb=short

    log "Running frontend tests..."
    cd "$PROJECT_ROOT/frontend"
    npm test -- --watchAll=false

    log "All tests passed."
}

cmd_docker() {
    log "Building and starting containers..."
    cd "$PROJECT_ROOT"
    docker-compose up --build -d
    log "Services running. Backend: http://localhost:5000  Frontend: http://localhost:3000"
}

cmd_clean() {
    log "Stopping containers..."
    cd "$PROJECT_ROOT"
    docker-compose down -v 2>/dev/null || true
    rm -rf /tmp/migrations
    log "Cleaned up."
}

case "${1:-help}" in
    setup)  cmd_setup ;;
    dev)    cmd_dev ;;
    test)   cmd_test ;;
    docker) cmd_docker ;;
    clean)  cmd_clean ;;
    *)
        echo "Usage: $0 {setup|dev|test|docker|clean}"
        exit 1
        ;;
esac
