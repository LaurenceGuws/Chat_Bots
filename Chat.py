from predict import predict_large_language_model_sample
from predict_gpt_35_turbo import predict_gpt_35_turbo


class Chat:
    def __init__(self, project_id, model_name, temperature, max_output_tokens, top_p, top_k):
        self.project_id = project_id
        self.model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.top_p = top_p
        self.top_k = top_k

    def send_message(self, message):
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
    def predict_gpt_35_turbo_call(messages):
        response = predict_gpt_35_turbo(messages)
        return response

if __name__ == '__main__':
    chat = Chat(project_id='palm-386622',
                model_name='chat-bison@001',
                temperature=0.5,
                max_output_tokens=256,
                top_p=0.9,
                top_k=40)
    while True:
        message = input('You: ')
        response = chat.send_message(message)
        print('Bard:', response)
