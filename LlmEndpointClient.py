import requests

class LlmEndpointClient:
    BASE_URL = "https://llmendpoint.com/api/v1/completions"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_completion(self, messages, model, max_tokens, temperature=0.7, num_context=2048, stream=False):
        headers = {
            "Authorization": self.api_key
        }
        data = {
            "messages": messages,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "num_context": num_context,
            "stream": stream
        }
        response = requests.post(self.BASE_URL, json=data, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response_data = response.json()
            raise Exception(f"Error {response.status_code}: {response_data.get('message', 'Unknown error')}")
