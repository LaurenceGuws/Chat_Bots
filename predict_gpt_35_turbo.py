import requests
import json

def predict_gpt_35_turbo(messages):
    api_key = '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'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    for message in messages:
      role = message["role"]
      content = message["content"]
      if role == 'Bard':
        role = 'assistant'
      data = {
          "model": "gpt-3.5-turbo",
          "messages": [{"role": role, "content": content}],
          "messages": messages,
          "temperature": 0
      }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return response.status_code

if __name__ == "__main__":
    messages = [{"role": "user", "content": "Hello!"}]
    response = predict_gpt_35_turbo(messages)
    print(response)
