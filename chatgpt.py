import os
import json
from dotenv import load_dotenv
from openai import OpenAI

class Chatgpt:

    def get_answer(self, question):      
        load_dotenv()
        
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        response = client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=question
        )
            
        json_object = response
        json_string = json.dumps(json_object)

        parsed_json = json.loads(json_string)

        text = parsed_json['choices'][0]['text']

        return text
