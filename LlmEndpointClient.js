const axios = require('axios');

class LlmEndpointClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://llmendpoint.com/api/v1/completions';
  }

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
}

module.exports = LlmEndpointClient;
