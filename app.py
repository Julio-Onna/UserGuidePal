from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, List
from main import main

app = FastAPI()

class WebhookRequest(BaseModel):
    actions: List[Dict[str, Any]]


"""
Example request
{
    [
        {
            "id": 32,
            "entity_type": "story",
            "action": "update",
            "name": "Test1",
            "story_type": "feature",
            "app_url": "https://app.shortcut.com/jcav/story/32",
            "changes": {
                "completed_at": {"new": "2023-08-10T21:49:43Z"},
                "completed": {"new": True, "old": False},
                "started": {"new": True, "old": False},
                "position": {"new": 52147483648, "old": 12147483648},
                "workflow_state_id": {"new": 500000010, "old": 500000006},
                "started_at": {"new": "2023-08-10T21:49:43Z"},
            },
        }
    ]
}
"""

@app.post("/webhook")
async def webhook(body: WebhookRequest):
    if len(body.actions) and body.actions[0].get("changes") and body.actions[0]["changes"]["completed"]["new"]:
        main()
