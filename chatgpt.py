import os
from dotenv import load_dotenv
from openai import OpenAI

class Chatgpt:

    def get_answer(self, question):
        prompt = question
        
        load_dotenv()
        
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
    
            return response.choices[0].message.content
        except:
            return
