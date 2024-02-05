import os
import json
from dotenv import load_dotenv
from openai import OpenAI

class Chatgpt:

    def get_answer(self, question):
        prompt = question
        
        load_dotenv()
        
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        try:
            response = client.chat.completions.create(
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5
            )
            
            json_object = response
            json_string = json.dumps(json_object)

            parsed_json = json.loads(json_string)

            text = parsed_json['choices'][0]['text']

            return text
        except:
            return
