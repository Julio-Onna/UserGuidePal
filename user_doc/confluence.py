import json
import uuid
from datetime import datetime

from user_doc.base_client import BaseClient


class ConfluenceClient(BaseClient):
    def __init__(self, key):
        super().__init__()
        self.headers = self.build_headers(key)
        self.base_url = "https://juliopedia.atlassian.net/wiki"
        self.api_endpoint = "/rest/api/content"

    @staticmethod
    def build_headers(token):
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }
        return headers

    async def create_confluence_page(self, title, body="<p>This is a new page</p>"):
        """
        Creates a basic page in Confluence using the title & body provided
        """
        time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "type": "page",
            "title": f"[DRAFT - {time}-{uuid.uuid4().hex[:6]}] " + title,
            "space": {"key": "FeatureDoc"},
            "body": {"storage": {"value": body, "representation": "storage"}},
        }
        async with self.session.post(
            f"{self.base_url}{self.api_endpoint}", json=data, headers=self.headers
        ) as response:
            json_data = await response.json()
            if response.status == 200:
                print(f'Confluence page "{title}" created successfully.')
                return json_data["id"]
            else:
                print(
                    f"Failed to create Confluence page. Status code: {response.status}"
                )
                print(json_data)

    async def add_link(self, post_id, page_title, url):
        """
        Adds a footer comment with a link
        """
        data = {"title": f"{page_title}"}
        async with self.session.get(
            f"{self.base_url}{self.api_endpoint}/{post_id}",
            json=data,
            headers=self.headers,
        ) as response:
            page = await response.json()

        post_link = self.base_url + page["_links"]["webui"]
        comment_data = {
            "type": "comment",
            "container": page,
            "body": {
                "storage": {
                    "value": f'<a href="{url}">Link to story</a>',
                    "representation": "storage",
                }
            },
        }
        async with self.session.post(
            f"{self.base_url}{self.api_endpoint}",
            data=json.dumps(comment_data),
            headers=self.headers,
        ) as response:
            if response.status == 200:
                print("SC link added to confluence page")

        return post_link
