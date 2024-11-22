import requests

class LlmEndpointClient:
    BASE_URL    = "https://llmendpoint.com/api/v1/completions"
    QUEUE_URL   = "https://llmendpoint.com/api/v1/qcompletions"
    STATUS_URL  = "https://llmendpoint.com/api/v1/qcompletions"

    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def generate_completion(self, messages, model, max_tokens, output_format="default", temperature=0.7, num_context=2048, stream=False):
        """
        Generate completion for the given messages
        :param messages: List of messages to generate completion for
        Example:
        [
            { 'role': 'system', 'content': 'Hello' },
            { 'role': 'user', 'content': 'Hi' }
        ]
        :param model: Model to use for completion
        :param max_tokens: Maximum tokens to generate
        :param temperature: Temperature for sampling
        :param num_context: Number of tokens to use as context
        :param output_format: Output format for completion [default, json]
        :param stream: Stream completion or not
        :return: Completion response
        """
        headers = {
            "Authorization": self.api_key
        }
        data = {
            "messages": messages,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "num_context": num_context,
            "stream": stream,
            "output_format": output_format
        }
        response = requests.post(self.BASE_URL, json=data, headers=headers, stream=stream) if stream else requests.post(self.BASE_URL, json=data, headers=headers)

        if response.status_code == 200:
            if stream:
                return response.iter_lines()
            else:
                return response.json()
        else:
            response_data = response.json()
            raise Exception(f"Error {response.status_code}: {response_data.get('message', 'Unknown error')}")
    
    def queue_completion(self, messages, model, max_tokens, output_format="default", temperature=0.7, num_context=2048):
        """
        Queue a new completion request for asynchronous processing
        :param messages: List of messages for completion
        :param model: Model to use for completion
        :param max_tokens: Maximum tokens to generate
        :param output_format: Output format for completion [default, json]
        :param temperature: Temperature for sampling
        :param num_context: Number of tokens to use as context
        :return: Response with task ID if successfully queued
        """
        headers = {
            "Authorization": self.api_key
        }
        data = {
            "messages": messages,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "num_context": num_context,
            "output_format": output_format
        }
        response = requests.post(self.QUEUE_URL, json=data, headers=headers)
        
        '''
        Failed Response:
        {
            'message': '',  // Possible error messages: 'Invalid request', ''Authorization header required', 'Invalid API key', 'Unauthorized IP address', 'Model pricing not found', 'messages, model, max_tokens, and temperature are required', ...
            'success': False
        }
        Success Response:
        {
            'success': True,
            'task_id': 'task_id',
            'message': 'Request queued successfully'
        }
        '''

        if response.status_code == 200:
            return response.json()  # Includes task_id and message
        else:
            response_data = response.json()
            raise Exception(f"Error {response.status_code}: {response_data.get('message', 'Unknown error')}")

    def check_task_status(self, task_id):
        """
        Check the status of a queued task using the task_id
        :param task_id: Task ID for the queued completion
        :return: Task status and result if completed
        """
        headers = {
            "Authorization": self.api_key
        }
        url = f"{self.STATUS_URL}/{task_id}"
        response = requests.get(url, headers=headers)
        
        '''
        Failed Response:
        {
            'message': '',  // Possible error messages: 'Authorization header required', 'Invalid API key', 'Task not found', 'Unauthorized'
            'success': False
        }
        Success Response:
        {
            'completed_at': '', 
            'created_at': '', 
            'result': '', // ai response
            'status': 'completed', // 'queued', 'processing', 'completed', 'failed'
            'success': True
        }
        '''

        if response.status_code == 200:
            return response.json()
        else:
            response_data = response.json()
            raise Exception(f"Error {response.status_code}: {response_data.get('message', 'Unknown error')}")
