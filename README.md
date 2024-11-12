## LlmEndpoint

LlmEndpoint is a repository for [LlmEndpoint](https://llmendpoint.com), a service offering low-cost APIs for text generation. This repository includes modules in multiple programming languages to simplify the integration with the LlmEndpoint API, along with raw API documentation for developers.

### Features
- Multi-language support: Modules in various programming languages to interact with the LlmEndpoint API.
- Easy integration: Simplified methods to make API requests and handle responses.
- Comprehensive documentation: Raw API docs to help developers understand and use the API effectively.

### Getting Started
Instructions to get started with the LlmEndpoint modules and API documentation.


# LlmEndpoint API Documentation

Welcome to the LlmEndpoint API documentation. LlmEndpoint is a low-cost text generation API designed for a wide range of applications. This documentation provides details on using the `/api/v1/completions` endpoint.

# Models Available

<div align="center">

| Model Name        |
|-------------------|
| llama3.1          |
| llama3            |
| llama2            |
| mistral           |
| qwen              |
| gemma2            |
| llama3.2          |
| qwen2             |
| zephyr            |
| gemma             |
| llava             |
| mistral-nemo      |
| phi3              |
| wizardlm2         |
| orca-mini         |
| codellama         |
| llama2-uncensored |
| owl_t-lite        |

</div>

---

## Base URL

`https://llmendpoint.com/api/v1/completions`

## Endpoint Overview

`POST /api/v1/completions`

This endpoint generates text completions based on the given parameters.

## Headers

- **Authorization** (Required): API key for authentication.

---

## Request Parameters

### JSON Body Parameters

- **messages** (Required): List of messages where each message is an object with "role" (`user`, `assistant`, or `system`) and "content".
- **num_context** (Optional, default: `2048`): Integer representing the maximum token length of context the model will consider.
- **model** (Required): String specifying the model name. Supported models are:
  - `llama3.1`, `llama3`, `llama2`, `mistral`, `qwen`, `gemma2`, `llama3.2`, `qwen2`, `zephyr`, `gemma`, `llava`, `mistral-nemo`, `phi3`, `wizardlm2`, `orca-mini`, `codellama`, `llama2-uncensored`, `owl_t-lite`
- **max_tokens** (Required): Integer specifying the maximum number of tokens to generate.
- **temperature** (Optional, default: `0.7`): Float between 0.0 and 1.0 controlling the randomness of the response.
- **stream** (Optional, default: `false`): Boolean indicating whether to stream the response.

---

## Cost Calculation

Each model has a specific rate for input and output tokens. The cost is calculated as follows:

- **Input Rate** and **Output Rate**: Specific to each model (e.g., `llama3.1` has an Input Rate of `0.01` and Output Rate of `0.02`).
- **Input Tokens**: Sum of characters in `messages` from the user.
- **Output Tokens**: Equal to `max_tokens`.
- **Credits Needed**: Total cost (in cents) divided by 0.0001.

---

## Example Request

### Request Body

```json
{
    "messages": [{"role": "user", "content": "What is the meaning of life?"}],
    "model": "llama3.1",
    "max_tokens": 100,
    "temperature": 0.7,
    "stream": false
}
```

### Response

For non-streamed responses:

```json
{
    "success": true,
    "response": "The meaning of life varies from person to person..."
}
```

For streamed responses, you will receive chunks like this:

```json
{"role": "assistant", "content": "The"}
{"role": "assistant", "content": " meaning"}
{"role": "assistant", "content": " of"}
{"role": "assistant", "content": " life"}
...
```

---

## Error Responses

| Status Code | Message                             | Description                                                   |
|-------------|-------------------------------------|---------------------------------------------------------------|
| 400         | Invalid request                     | The request payload is invalid or missing required fields.    |
| 401         | Authorization header required       | No API key was provided.                                      |
| 401         | Invalid API key                     | The provided API key is invalid.                              |
| 401         | Unauthorized IP address             | The request IP address is not whitelisted for this API key.   |
| 402         | Insufficient credits                | The user does not have enough credits to process the request. |
| 400         | messages, model, max_tokens, and temperature are required | Required fields are missing.                                  |
| 400         | Model pricing not found             | The specified model does not have defined rates.              |
| 400         | Max attempts reached - no available hosts | Could not process request due to lack of available hosts.  |

---

## Notes

- Ensure your IP is whitelisted if IP restrictions are enabled on your API key.
- Streaming responses provide partial responses, chunked by tokens.
- Each user has a credit balance; ensure sufficient credits to complete requests.

---

Thank you for using LlmEndpoint!
