const axios = require('axios');

class LlmEndpointClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://llmendpoint.com/api/v1/completions';
    this.queueUrl = 'https://llmendpoint.com/api/v1/qcompletions';
    this.statusUrl = 'https://llmendpoint.com/api/v1/qcompletions';
  }

  // Method to generate a completion immediately
  async generateCompletion(messages, model, maxTokens, temperature = 0.7, numContext = 2048, stream = false) {
    const headers = {
      'Authorization': this.apiKey
    };
    const data = {
      messages: messages,
      model: model,
      max_tokens: maxTokens,
      temperature: temperature,
      num_context: numContext,
      stream: stream
    };

    try {
      const response = await axios.post(this.baseUrl, data, { headers: headers });
      return response.data;
    } catch (error) {
      throw new Error(`Error ${error.response.status}: ${error.response.data.message || 'Unknown error'}`);
    }
  }

  // Method to queue a completion request
  async queueCompletion(messages, model, maxTokens, temperature = 0.7, numContext = 2048, outputFormat = "default") {
    const headers = {
      'Authorization': this.apiKey
    };
    const data = {
      messages: messages,
      model: model,
      max_tokens: maxTokens,
      temperature: temperature,
      num_context: numContext,
      output_format: outputFormat
    };

    try {
      const response = await axios.post(this.queueUrl, data, { headers: headers });
      
      // Checking if the response indicates success or failure
      if (response.data.success) {
        return response.data;  // Includes task_id and message
      } else {
        throw new Error(`Error ${response.response.status}: ${response.response.data.message || 'Unknown error'}`);
      }
    } catch (error) {
      throw new Error(`Error ${error.response.status}: ${error.response.data.message || 'Unknown error'}`);
    }
  }

  // Method to check the status of a queued task
  async checkTaskStatus(taskId) {
    const headers = {
      'Authorization': this.apiKey
    };
    const url = `${this.statusUrl}/${taskId}`;

    try {
      const response = await axios.get(url, { headers: headers });
      
      if (response.data.success) {
        return response.data;  // Includes task status and result if completed
      } else {
        throw new Error(`Error ${response.response.status}: ${response.response.data.message || 'Unknown error'}`);
      }
    } catch (error) {
      throw new Error(`Error ${error.response.status}: ${error.response.data.message || 'Unknown error'}`);
    }
  }
}

module.exports = LlmEndpointClient;
