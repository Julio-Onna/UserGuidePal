import asyncio
import os
from typing import Any, Dict, List, Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request

from user_doc.confluence import ConfluenceClient
from user_doc.content_generator import ContentGenerator
from user_doc.shortcut import ShortcutClient
from user_doc.utils import write_doc_from_story


class HTTPApplication(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        _ = load_dotenv(find_dotenv())  # read local .env file
        sc_api_key = os.environ["SHORTCUT_TOKEN"]
        cf_api_key = os.environ["CONFLUENCE_TOKEN"]
        gpt_api_key = os.environ["GPT_TOKEN"]

        self.shortcut_client = ShortcutClient(sc_api_key)
        self.bot = ContentGenerator(gpt_api_key)
        self.confluence_client = ConfluenceClient(cf_api_key)


app = HTTPApplication()


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
async def webhook(request: Request, body: WebhookRequest):
    # This could be a list of actions, like if you moved multiple stories to complete at the same time
    semaphore = asyncio.Semaphore(5)

    tasks = [
        write_doc_from_story(request, story_id=action.id, semaphore=semaphore)
        for action in body.actions
        if action.changes.get("completed", {}).get("new")
    ]

    await asyncio.gather(*tasks)
