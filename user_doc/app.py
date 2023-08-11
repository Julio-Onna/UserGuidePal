import asyncio
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from user_doc.main import main

app = FastAPI()


class Action(BaseModel):
    # We don't really care about the other properties here, so they aren't defined, they'll just get ingored
    id: int
    changes: Optional[Dict[str, Any]] = {}


class WebhookRequest(BaseModel):
    actions: List[Action] = []


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
    # This could be a list of actions, like if you moved multiple stories to complete at the same time
    semaphore = asyncio.Semaphore(5)

    tasks = [
        main(story_id=action.id, semaphore=semaphore)
        for action in body.actions
        if action.changes.get("completed", {}).get("new")
    ]

    await asyncio.gather(*tasks)
