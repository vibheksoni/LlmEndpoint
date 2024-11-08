import requests

class LlmEndpointClient:
    BASE_URL = "https://api.llmendpoint.com/api/v1/completions"

    model_rates = {
        'llama3.1': {'Input Rate': 0.01, 'Output Rate': 0.02},
        'llama3': {'Input Rate': 0.015, 'Output Rate': 0.025},
        'llama2': {'Input Rate': 0.02, 'Output Rate': 0.03},
        'mistral': {'Input Rate': 0.012, 'Output Rate': 0.022},
        'qwen': {'Input Rate': 0.018, 'Output Rate': 0.028},
        'gemma2': {'Input Rate': 0.016, 'Output Rate': 0.026},
        'llama3.2': {'Input Rate': 0.014, 'Output Rate': 0.024},
        'qwen2': {'Input Rate': 0.017, 'Output Rate': 0.027},
        'zephyr': {'Input Rate': 0.019, 'Output Rate': 0.029},
        'gemma': {'Input Rate': 0.013, 'Output Rate': 0.023},
        'llava': {'Input Rate': 0.015, 'Output Rate': 0.025},
        'mistral-nemo': {'Input Rate': 0.011, 'Output Rate': 0.021},
        'phi3': {'Input Rate': 0.02, 'Output Rate': 0.03},
        'wizardlm2': {'Input Rate': 0.018, 'Output Rate': 0.028},
        'orca-mini': {'Input Rate': 0.019, 'Output Rate': 0.029},
        'codellama': {'Input Rate': 0.017, 'Output Rate': 0.027},
        'llama2-uncensored': {'Input Rate': 0.015, 'Output Rate': 0.025},
        'owl_t-lite': {'Input Rate': 0.014, 'Output Rate': 0.024},
    }

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

    def calculate_cost(self, messages, model, max_tokens):
        rates = self.model_rates.get(model)
        if not rates:
            raise ValueError("Model pricing not found")

        input_tokens = sum(len(msg['content']) for msg in messages if msg['role'] == 'user')
        output_tokens = max_tokens

        input_cost = input_tokens * rates['Input Rate'] / 1000
        output_cost = output_tokens * rates['Output Rate'] / 1000

        return {
            "input_cost": input_cost,
            "output_cost": output_cost,
            "total_cost": input_cost + output_cost,
            "credits_needed": int((input_cost + output_cost) / 0.0001)
        }
