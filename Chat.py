import os
import openai
from predict import predict_large_language_model_sample

class Chat:
    def __init__(self, project_id, model_name, temperature, max_output_tokens, top_p, top_k):
        self.project_id = project_id
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.top_k = top_k

    def send_bard_message(self, message):
        response = predict_large_language_model_sample(
            input=message,
            project_id=self.project_id,
            model_name=self.model_name,
            temperature=self.temperature,
            max_output_tokens=self.max_output_tokens,
            top_p=self.top_p,
            top_k=self.top_k,
        )
        return response

    def chat_gpt_interact(self, messages):
        import configparser
        config = configparser.ConfigParser()
        config.read('config.conf')
        openai_api_key = config['OpenAI']['API_KEY']
        messages_dicts = []
        openai.api_key = openai_api_key
        # print(openai.Model.list())
        for i, message in enumerate(messages):
            if i % 2 == 0:
                messages_dicts.append({"role": "system", "content": message})
            else:
                messages_dicts.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=messages_dicts
        )
        return response['choices'][0]['message']['content']
