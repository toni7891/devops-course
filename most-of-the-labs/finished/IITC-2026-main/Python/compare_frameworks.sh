#!/bin/bash
# Automated framework comparison using Apache Bench (ab)
# Usage: ./compare_frameworks.sh

echo "======================================"
echo "Framework Load Test Comparison"
echo "======================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test a URL
test_framework() {
    local name=$1
    local url=$2
    
    echo -e "${YELLOW}Testing $name: $url${NC}"
    echo "Command: ab -n 1000 -c 10"
    echo
    
    # Check if server is running
    if ! curl -s "$url" > /dev/null; then
        echo -e "${RED}ERROR: $name server not running at $url${NC}"
        echo "Start it first, then run this script again."
        echo
        return
    fi
    
    # Run ab and extract key metrics
    result=$(ab -n 1000 -c 10 "$url" 2>&1)
    
    # Extract metrics
    rps=$(echo "$result" | grep "Requests per second" | awk '{print $4}')
    latency=$(echo "$result" | grep "Time per request.*mean" | head -1 | awk '{print $4}')
    failed=$(echo "$result" | grep "Failed requests" | awk '{print $3}')
    
    echo -e "${GREEN}Results for $name:${NC}"
    echo "  Requests/sec: $rps"
    echo "  Avg latency: ${latency}ms"
    echo "  Failed requests: $failed"
    echo
}

echo "Make sure all three servers are running first!"
echo "  - Flask: python3 app.py (port 5000)"
echo "  - Django: python3 manage.py runserver (port 8000)"
echo "  - FastAPI: uvicorn main:app (port 8000 or change it)"
echo
echo "Starting comparison in 5 seconds..."
sleep 5
echo

# Test each framework
test_framework "Flask" "http://localhost:5000/students"
test_framework "Django" "http://localhost:8000/api/students/"
test_framework "FastAPI" "http://localhost:8001/students"  # Assuming port 8001

echo "======================================"
echo -e "${GREEN}Comparison Complete!${NC}"
echo
echo "Winner is the framework with:"
echo "  - Highest Requests/sec"
echo "  - Lowest Avg latency"
echo "  - Zero Failed requests"
echo
