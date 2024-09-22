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
            
            
            You are a character a red circle. You will see a top-down view of yourself in an image shortly.
            You are inside of a small city with a few roads and buildings. 
            The dark grey rectangle is a road. The light grey rectangles with text on them are buildings. The
            text on them represents what they are. You can move along the left and right along the road as you please.
            This image shows the area around you that you can see, which is only a small portion of the world. 

            Describe everything from your point of view as the red circle in a structured format (e.g., JSON) with the following fields:
            - description: your observations
            - buildings: list of building names
            - roads: information about the road
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
    #return response.json()
    response_data = response.json()

    # Assuming the model's response is in the 'choices' field
    if 'choices' in response_data and len(response_data['choices']) > 0:
        structured_response = response_data['choices'][0]['message']['content']
        try:
            # Attempt to convert the structured response into a dictionary
            response_dict = json.loads(structured_response)
            return response_dict
        except json.JSONDecodeError:
            return {"error": "Failed to decode response as JSON", "content": structured_response}
    else:
        return {"error": "No valid response from model"}
    