import requests
import os
import requests
import base64
from pydantic import BaseModel
import json


api_key = os.getenv("OPENAI_API_KEY")

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

def encode_image(path):
    image = open(path, "rb")
    return base64.b64encode(image.read()).decode('utf8')


def get_llm_response(question,image_path):
    encoded_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }


    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": f"""
            
            
            You are a character represented by a red circle, positioned in a small city depicted from a top-down view. In this environment, you will navigate through a limited area with roads and buildings, where:

            - The dark grey rectangles represent roads that you can move along.
            - The light grey rectangles with text indicate buildings, with the text denoting their identities.
            - Movement is restricted to the roads; you cannot pass through buildings.
            - You can move vertically or horizontally in increments of 50 pixels.

            When you respond, provide a structured output in JSON format with the following fields:

            - **description**: A detailed account of your observations from your current position, including the layout and any notable features around you.
            - **horizontal movement**: The amount you intend to move horizontally, expressed as a positive multiple of 50, formatted as a string.
            - **horizontal direction**: The direction of your horizontal movement, either "left" or "right".
            - **vertical movement**: The amount you intend to move vertically, expressed as a positive multiple of 50, formatted as a string.
            - **vertical direction**: The direction of your vertical movement, either "up" or "down".
            - **explanation**: A comprehensive reasoning for your movement choice, detailing your observations and thought process in at least four sentences.

            Please proceed to describe your surroundings and movements accordingly.
            Answer this question: {question}

            
            """
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_image}"
            }
            }
        ]
        }
    ],

    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response)
    print("\n\n\n")
    #return response.json()
    response_data = response.json()

    # Assuming the model's response is in the 'choices' field
    if 'choices' in response_data and len(response_data['choices']) > 0:
        structured_response = response_data['choices'][0]['message']['content']
        cleaned_response = structured_response.strip('```json\n').strip('```').strip()
        try:
            # Attempt to convert the structured response into a dictionary
            response_dict = json.loads(cleaned_response)
            return response_dict
        except json.JSONDecodeError:
            return {"error": "Failed to decode response as JSON", "content": structured_response}
    else:
        return {"error": "No valid response from model"}
    