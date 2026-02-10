# AIP Migration Tracker

Visual tracker for AI Platform migration progress across all deployment steps.

## Quick Start

```bash
# View the tracker
open index.html
```

## Migration Overview

This tracker monitors the 7-step progressive rollout of AI Platform (AIP), which centralizes all API calls to Bedrock.

### Deployment Steps

1. **Pre-rollout** - Bug fixes, data migration, testing
2. **Start Rollout** - Hotfix enabling copilot features
3. **UI Migration** - AI Skills UI uses AIP Models API
4. **Partial Rollout** - Selected sites migrate to AIP
5. **Full Rollout** - All customers (except high-usage)
6. **Large Customers** - Enable IAG, CBA, etc.
7. **Feature Toggles** - Enable BWO AWS for 26.2

## Data Format

Status data is stored in `data/migration-status.json` and follows this structure:

```json
{
  "lastUpdated": "2026-02-10T13:00:00Z",
  "steps": [
    {
      "id": 1,
      "name": "Pre-rollout",
      "status": "completed|in-progress|not-started|blocked",
      "progress": 0-100,
      "notes": "Optional notes"
    }
  ]
}
```

## Updating Status

Edit `data/migration-status.json` manually or use the web interface.

## Constitution

This project follows the principles defined in `.specify/memory/constitution.md`:
- Data Accuracy
- Visual Reporting First
- Simplicity (NON-NEGOTIABLE)
- Stakeholder Communication
