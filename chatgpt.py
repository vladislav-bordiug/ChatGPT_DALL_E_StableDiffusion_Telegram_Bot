import os
import json
from dotenv import load_dotenv
from openai import OpenAI

class Chatgpt:

    def get_answer(self, question):
        prompt = question
        
        load_dotenv()
        
        client = OpenAI()
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")
        try:
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=1500,
                temperature=0.5,
            )

            json_object = response
            json_string = json.dumps(json_object)

            parsed_json = json.loads(json_string)

            text = parsed_json['choices'][0]['text']

            return text
        except:
            return
