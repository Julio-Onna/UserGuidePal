# UserGuidePal
Build user-facing docs from shortcut user stories

What's working now:   

1- In main, gets shortcut story details from the provided Story ID, or via webhook
2- Runs the story through standard GPT 3.5 (no onna training) with the defined prompt.  
3- Posts that in confluence in the 'Feature Doc' space.   
4- Adds a comment in both shortcut & confluence with a link to each other


Improvements:

- Maybe we can use a better prompt and/or tweak the constants for better response?
- Maybe we can use an LLM model we train for ourselves? So we could use onna-specific user stories
- Currently using requests, maybe the code can be cleaner
- ?

How to enable webhook:
- First install the requirements, `python3 -m venv venv && venv/bin/pip install -r requirements.txt`
- Download ngrok, for mac `brew install ngrok/ngrok/ngrok`
- You can then start the server by typing `ngrok http 8000`, this will give you a public url
- Visit shortcut's settings and add the url you were given here https://app.shortcut.com/jcav/settings/integrations/outgoing-webhook
- Start the fastapi server that has the webhook `make run_app`
- Now you can move a stroy to done and you should see the request in the application logs