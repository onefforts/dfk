import requests
import settings
import os

result = os.popen('ps aux | grep python3').read()

quest_count = result.count('quests.py')
if quest_count < 15:
  requests.post(settings.DISCORD_URL, { 'content': f'There are some stopped dfk quest processes. quest count: {quest_count}' })
