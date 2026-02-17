#!/bin/bash
# Run Jira sync locally and push changes

cd "$(dirname "$0")"

echo "🔄 Syncing Jira status..."

# Prompt for credentials
read -p "Jira email: " JIRA_EMAIL
read -sp "Jira API token: " JIRA_API_TOKEN
echo ""

# Export and run sync
export JIRA_EMAIL
export JIRA_API_TOKEN

python3 sync-jira-status.py

# Check if changes were made
if git diff --quiet data/migration-status.json; then
    echo "✓ No changes to commit"
else
    echo "📝 Committing changes..."
    git add data/migration-status.json
    git commit -m "chore: sync Jira status"
    git push origin main
    echo "✓ Changes pushed to GitHub"
fi
