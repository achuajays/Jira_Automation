import os
import streamlit as st
import requests
import json
from groq import Groq

def send_message_to_google_chat(webhook_url, message, image_url=None):
    headers = {'Content-Type': 'application/json'}
    data = {'text': message}

    # If an image URL is provided, add it to the message payload
    if image_url:
        data['cards'] = [
            {
                "sections": [
                    {
                        "widgets": [
                            {
                                "image": {
                                    "imageUrl": image_url,
                                    "onClick": {
                                        "openLink": {
                                            "url": image_url
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        ]

    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        st.success("Message sent successfully!")
    else:
        st.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

def generate_ai_explanation(prompt):
    client = Groq()
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Provide an explanation for the following Testing Ticket: "
            },
            {
                "role": "user",
                "content": f"Create a detailed markdown message indicating the given ticket and explain about it in detail - {prompt}",
            }
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def analyze_image(image_url):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

def main():
    st.title("AI Explanation Application")

    # Input field for the prompt
    prompt = st.text_area("Enter your question or topic for AI explanation:")

    # Input field for the image URL
    image_url = st.text_input("Enter the image URL (optional):")

    # Google Chat webhook URL
    webhook_url = os.getenv("Google_Chat_Webhook_URL")

    if st.button("Generate and Send Explanation"):
        if not webhook_url:
            st.error("Please enter the Google Chat Webhook URL.")
        else:
            # Generate AI explanation
            explanation = generate_ai_explanation(prompt)

            # Analyze the image if an image URL is provided
            image_analysis = ""
            if image_url:
                image_analysis = analyze_image(image_url)
                explanation += f"\n\n**Image Analysis:**\n{image_analysis}"

            # Format the explanation as markdown
            explanation = explanation.replace("**", "").replace("#", "")

            # Send the markdown message to Google Chat
            send_message_to_google_chat(webhook_url, explanation, image_url)

            # Display the explanation in the app
            st.text_area("Generated Explanation", explanation, height=400)

if __name__ == "__main__":
    main()
