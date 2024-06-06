from openai import OpenAI
from django.conf import settings
from dotenv import load_dotenv
import os
import time
import logging
from datetime import datetime

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


client = OpenAI(api_key=api_key)




def generate_documentation(code):
    client = OpenAI(api_key=api_key)

    assistant_id = "asst_AdBUAHz6bVXD0NiiITiNsHwd"
    thread_id = "thread_aEGmI6mba5Y1ZLeYmXoHV8kZ"
        
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=f"Generate documentation for the following code:\n\n{code}\n\nDocumentation:"
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Start the sentence with 'Here is your documentation:' "
    )
    run_id = run.id    

    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

                messages = client.beta.threads.messages.list(thread_id=thread_id)            
                last_message = messages.data[0]            
                response = last_message.content[0].text.value

                # Replace newline characters with <br> tags
                formatted_response = response.replace('\n', '<br>')

                return formatted_response
                break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            break
        time.sleep(5)