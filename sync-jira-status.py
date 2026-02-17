#!/usr/bin/env python3
"""
Sync Jira ticket status to migration tracker.
Updates tasks marked as 'blocked' or 'in-progress' if Jira shows 'Done' or 'Closed'.
"""

import json
import os
import re
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import base64

JIRA_BASE_URL = "https://appian-eng.atlassian.net"
DATA_FILE = "data/migration-status.json"

def get_jira_status(ticket_key, email, api_token):
    """Fetch Jira ticket status via API."""
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{ticket_key}?fields=status"
    
    # Create basic auth header
    credentials = f"{email}:{api_token}"
    encoded = base64.b64encode(credentials.encode()).decode()
    
    req = Request(url)
    req.add_header("Authorization", f"Basic {encoded}")
    req.add_header("Accept", "application/json")
    
    try:
        with urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data["fields"]["status"]["name"]
    except HTTPError as e:
        if e.code == 403:
            print(f"Error: 403 Forbidden for {ticket_key}")
            print(f"  Check that JIRA_EMAIL ({email}) is correct")
            print(f"  Check that JIRA_API_TOKEN is valid")
        else:
            print(f"Error fetching {ticket_key}: {e}")
        return None

def extract_jira_key(link):
    """Extract Jira ticket key from URL."""
    match = re.search(r'/browse/([A-Z]+-\d+)', link)
    return match.group(1) if match else None

def should_mark_completed(status):
    """Check if Jira status means task is complete."""
    completed_statuses = ["Done", "Closed", "Resolved", "Complete"]
    return status in completed_statuses

def update_task_status(task, email, api_token):
    """Update task status if Jira ticket is completed."""
    if task.get("status") not in ["blocked", "in-progress"]:
        return False
    
    link = task.get("link", "")
    if not link or "atlassian.net" not in link:
        return False
    
    ticket_key = extract_jira_key(link)
    if not ticket_key:
        return False
    
    print(f"Checking {ticket_key}...")
    jira_status = get_jira_status(ticket_key, email, api_token)
    
    if jira_status and should_mark_completed(jira_status):
        print(f"  ✓ {ticket_key} is {jira_status} - marking as completed")
        task["status"] = "completed"
        return True
    
    return False

def sync_jira_status(email, api_token):
    """Main sync function."""
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    changes_made = False
    
    for step in data["steps"]:
        for task in step.get("tasks", []):
            if update_task_status(task, email, api_token):
                changes_made = True
            
            # Check subtasks
            for subtask in task.get("subtasks", []):
                if update_task_status(subtask, email, api_token):
                    changes_made = True
    
    if changes_made:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        print("\n✓ Updated migration-status.json")
        return True
    else:
        print("\n✓ No changes needed")
        return False

if __name__ == "__main__":
    email = os.environ.get("JIRA_EMAIL")
    api_token = os.environ.get("JIRA_API_TOKEN")
    
    if not email or not api_token:
        print("Error: JIRA_EMAIL and JIRA_API_TOKEN environment variables required")
        sys.exit(1)
    
    changes = sync_jira_status(email, api_token)
    sys.exit(0 if changes else 1)
