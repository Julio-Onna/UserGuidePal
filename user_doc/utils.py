import asyncio
import os


async def write_draft(request, subject_matter, title, details):
    """
    Uses ContentGenerator class to ask the GPT endpoint.
    Uses Confluence class to post to confluence.
    """
    # Get GPT response
    draft = request.app.bot.get_completions_response(subject_matter, title, details)
    # Post to confluence
    docs = request.app.docs
    story = request.app.story
    await docs.create_confluence_page(story.title, draft)
    # Shortcut link in confluence
    await docs.add_link(story.title, story.link)
    # Confluence link in shortcut
    await story.add_link_to_comment(story.id, docs.post_link)


async def write_doc_from_story(request, story_id=22, semaphore=asyncio.Semaphore(1)):
    async with semaphore:
        # Get story details
        # Shortcut's Story ID goes here
        story = request.app.story
        await story.get_story(story_id)
        print(f"Does it need docs: {story.is_doc_needed()}")
        if story.is_doc_needed():
            domain = story.get_content_labels()[0]["name"]
            await write_draft(request, domain, story.title, story.body)
