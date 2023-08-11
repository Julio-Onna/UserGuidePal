import json
import uuid

from user_doc.base_client import BaseClient


class Confluence(BaseClient):
    def __init__(self, key):
        super().__init__()
        self.headers = self.build_headers(key)
        self.base_url = "https://juliopedia.atlassian.net/wiki"
        self.api_endpoint = "/rest/api/content"
        self.post_id = ""
        self.post_link = ""

    async def create_confluence_page(self, title, body="<p>This is a new page</p>"):
        """
        Creates a basic page in Confluence using the title & body provided
        """
        data = {
            "type": "page",
            "title": f"[DRAFT - {uuid.uuid4().hex[:-5]}] " + title,
            "space": {"key": "FeatureDoc"},
            "body": {"storage": {"value": body, "representation": "storage"}},
        }
        async with self.session.post(
            f"{self.base_url}{self.api_endpoint}", json=data, headers=self.headers
        ) as response:
            json_data = await response.json()
            if response.status == 200:
                self.post_id = json_data["id"]
                print(f'Confluence page "{title}" created successfully.')
            else:
                print(
                    f"Failed to create Confluence page. Status code: {response.status}"
                )
                print(json_data)

    async def add_link(self, page_title, url):
        """
        Adds a footer comment with a link
        """
        data = {"title": f"{page_title}"}
        async with self.session.get(
            f"{self.base_url}{self.api_endpoint}", json=data, headers=self.headers
        ) as response:
            json_data = await response.json()

        parent_page = self.get_parent_page(self.post_id, json_data["results"])
        comment_data = {
            "type": "comment",
            "container": parent_page,
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

    @staticmethod
    def build_headers(token):
        headers = {
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        }
        return headers

    def get_parent_page(self, post_id, pages):
        """
        :return: Container with the page that matches post_id
        """
        found_page = None
        for page in pages:
            if page.get("id") == post_id:
                found_page = page
                break
        self.post_link = self.base_url + found_page["_links"]["webui"]
        return found_page
