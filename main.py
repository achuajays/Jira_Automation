from fastapi import FastAPI, Request
import requests
import os
import json

app = FastAPI()

GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/lTVpAsAAAAE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_e2aYAQsL3Rk06D6-qJ7EUkvg9FaTriTDQSkQP0cQzg"

@app.post('/jira-webhook')
async def jira_webhook(request: Request):
    data = await request.json()
    issue_key = data['issue']['key']
    issue_summary = data['issue']['fields']['summary']
    issue_url = f"{data['issue']['self']}"

    message = f"Issue {issue_key} has been updated: {issue_summary}. [View Issue]({issue_url})"

    headers = {'Content-Type': 'application/json'}
    chat_data = {'text': message}

    response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, headers=headers, data=json.dumps(chat_data))

    if response.status_code == 200:
        return {'status': 'Message sent successfully!'}
    else:
        return {'status': 'Failed to send message.', 'response': response.text}

# To run the app, use the command: uvicorn your_filename:app --reload
