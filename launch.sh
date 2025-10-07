#!/bin/bash
# ARKADU Launcher Script

echo "╔═══════════════════════════════════════╗"
echo "║   ARKADU OS - System Launcher        ║"
echo "╚═══════════════════════════════════════╝"
echo ""

# Check if server is already running
if lsof -Pi :8001 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✓ Server already running on port 8001"
else
    echo "Starting HTTP server on port 8001..."
    cd "/Users/gaia/resurrecting atlantis/ARKADU"
    python3 -m http.server 8001 &
    sleep 2
    echo "✓ Server started"
fi

echo ""
echo "Opening ARKADU systems..."
echo ""

# Open master index
open "http://localhost:8001/index-master.html"

echo "✓ Master index opened"
echo ""
echo "═══════════════════════════════════════"
echo "ARKADU OS is now running!"
echo ""
echo "Available at:"
echo "  • Master Index:  http://localhost:8001/index-master.html"
echo "  • Ecology View:  http://localhost:8001/ARKADU-ECOLOGY.html"
echo "  • TRUE-ARKADU:   http://localhost:8001/TRUE-ARKADU.html"
echo "  • Terminal:      http://localhost:8001/shell/terminal.html"
echo ""
echo "To stop the server: kill $(lsof -t -i:8001)"
echo "═══════════════════════════════════════"
