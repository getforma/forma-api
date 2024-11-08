import os
import json
from openai import OpenAI
from app.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def generate_feedback(metrics):
    # Load configuration from JSON file
    with open('app/utils/model_config.json', 'r') as config_file:
        config = json.load(config_file)

    # Use the loaded configuration
    model_name = config['model']
    system_prompt = config['system']['prompt']

    # Stringify the metrics
    metrics_str = json.dumps(metrics)
    format_str = json.dumps(config['system']['format'])

    # Make a request to the OpenAI API using the loaded configuration
    response = client.chat.completions.create(
    model=model_name,
    messages=[
            {
                "role": "system",
                "content": system_prompt + format_str
            },
            {
                "role": "user",
                "content": metrics_str
            }
        ]
    )

    return response.choices[0].message.content.strip()