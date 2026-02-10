#!/bin/bash
# Simple script to update migration status

echo "🚀 AIP Migration Tracker - Status Update"
echo "========================================"
echo ""

# Show current status
echo "Current Steps:"
cat data/migration-status.json | grep -A 2 '"name"' | grep 'name\|status\|progress' | head -21

echo ""
echo "To update status, edit: data/migration-status.json"
echo "Then refresh the browser to see changes."
echo ""
echo "View tracker: open index.html"
