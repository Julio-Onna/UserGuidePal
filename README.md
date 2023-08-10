# UserGuidePal
Build user-facing docs from shortcut user stories

What's working now:   

1- In main, gets shortcut story details from the provided Story ID.  
2- Runs the story through standard GPT 3.5 (no onna training) with the defined prompt.  
3- Posts that in confluence in the 'Feature Doc' space.
4- Adds a comment in both shortcut & confluence with a link to each other


Improvements:

- Instead of getting the story manually, get it using a webhook, cronjob or something similar
- Maybe we can use an LLM model we train for ourselves? So we could use onna-specific user stories
- Currently using requests, maybe the code can be cleaner
- ?