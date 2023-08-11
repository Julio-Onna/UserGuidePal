from user_doc.base_client import BaseClient


class ShortcutClient(BaseClient):
    def __init__(self, key):
        super().__init__()
        self.headers = self.build_headers(key)
        self.key = key
        self.api_url_base = "https://api.app.shortcut.com/api/v3"
        self.search_endpoint = "/search/stories"

    @staticmethod
    def build_headers(token):
        headers = {"Content-Type": "application/json", "Shortcut-Token": token}
        return headers

    async def get_story(self, story_id):
        """
        Uses shortcut rest api to get details about a specific story
        """
        search_query = {"query": story_id, "page_size": 1}

        url = self.api_url_base + self.search_endpoint
        async with self.session.get(
            url, params=search_query, headers=self.headers
        ) as response:
            response.raise_for_status()
            return await response.json()

    async def add_link_to_comment(self, story_id, link, message="LLM generated docs"):
        """
        :param message: text in the comment
        :param link: url
        :param story_id: shortcut story id
        """
        data = {"text": f'<a href="{link}">{message}</a>'}
        url = self.api_url_base + f"/stories/{story_id}/comments"
        async with self.session.post(url, json=data, headers=self.headers) as response:
            response.raise_for_status()

    async def get_member(self, member_id):
        """
        Translates shortcut's member id to a name, with the idea to tag them,
        email them...
        :return: member name as string
        """
        headers = {"Content-Type": "application/json", "Shortcut-Token": self.key}
        url = self.api_url_base + "/members/" + member_id
        async with self.session.get(url, headers=headers) as response:
            response.raise_for_status()
            member = await response.json()

        return member["profile"]["name"]


class Shortcut:
    def __init__(self, client):
        self.client = client
        self.id = ""
        self.link = ""
        self.owner = ""
        self.doc_tag = "doc_needed"
        self.title = ""
        self.body = ""
        self.labels = []

    async def get_story(self, story_id):
        """
        Uses shortcut rest api to get details about a specific story
        """
        data = await self.client.get_story(story_id)

        story = data["data"][0]
        self.title = story["name"]
        self.id = story["id"]
        self.link = story["app_url"]
        self.body = story["description"]
        self.labels = story["labels"]

        if len(story["owner_ids"]) > 0:
            self.owner = await self.client.get_member(story["owner_ids"][0])

        print(self.title)

    async def add_link_to_comment(self, story_id, link, message="LLM generated docs"):
        """
        :param message: text in the comment
        :param link: url
        :param story_id: shortcut story id
        """
        await self.client.add_link_to_comment(story_id, link, message)

    def is_doc_needed(self):
        """
        :return: True if story has a 'doc_needed' label. False otherwise.
        """
        has_doc_label = any(label["name"] == self.doc_tag for label in self.labels)
        return has_doc_label

    def get_content_labels(self):
        """
        :return: removes doc label and returns everything else
        """
        return [string for string in self.labels if string != self.doc_tag]
