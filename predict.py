import vertexai
from vertexai.preview.language_models import ChatModel, InputOutputTextPair

def predict_large_language_model_sample(
    input:str,
    project_id: str,
    model_name: str,
    temperature: float,
    max_output_tokens: int,
    top_p: float,
    top_k: int,
    location: str = "us-central1",
    ) :
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)

    chat_model = ChatModel.from_pretrained(model_name)
    parameters = {
      "temperature": temperature,
      "max_output_tokens": max_output_tokens,
      "top_p": top_p,
      "top_k": top_k,
    }

    chat = chat_model.start_chat(
      examples=[]
    )
    request_text = input
    response=chat.send_message(request_text,**parameters)
    return response.text
