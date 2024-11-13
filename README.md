## LlmEndpoint

LlmEndpoint is a repository for [LlmEndpoint](https://llmendpoint.com), a service offering low-cost APIs for text generation. This repository includes modules in multiple programming languages to simplify the integration with the LlmEndpoint API, along with raw API documentation for developers.

### Features
- Multi-language support: Modules in various programming languages to interact with the LlmEndpoint API.
- Easy integration: Simplified methods to make API requests and handle responses.
- Comprehensive documentation: Raw API docs to help developers understand and use the API effectively.

### Getting Started
Instructions to get started with the LlmEndpoint modules and API documentation.

# LlmEndpoint API Documentation

Welcome to the LlmEndpoint API documentation. LlmEndpoint is a low-cost text generation API designed for a wide range of applications. This documentation provides details on using the `/api/v1/completions` endpoint and new asynchronous task endpoints `/api/v1/qcompletions` and `/api/v1/qcompletions/<task_id>`.

## Models Available

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

`https://llmendpoint.com`

## Endpoint Overview

### 1. `POST /api/v1/completions`

This endpoint generates text completions based on the given parameters.

#### Headers

- **Authorization** (Required): API key for authentication.

#### Request Parameters

**JSON Body Parameters:**
- **messages** (Required): List of messages where each message is an object with `"role"` (`user`, `assistant`, or `system`) and `"content"`.
- **num_context** (Optional, default: `2048`): Integer representing the maximum token length of context the model will consider.
- **model** (Required): String specifying the model name.
- **max_tokens** (Required): Integer specifying the maximum number of tokens to generate.
- **temperature** (Optional, default: `0.7`): Float controlling the randomness of the response.
- **stream** (Optional, default: `false`): Boolean indicating whether to stream the response.

#### Example Request:

```json
{
    "messages": [{"role": "user", "content": "What is the meaning of life?"}],
    "model": "llama3.1",
    "max_tokens": 100,
    "temperature": 0.7,
    "stream": false
}
```

#### Example Response:

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

### 2. `POST /api/v1/qcompletions`

This endpoint queues a completion request for asynchronous processing. Once queued, the task will be processed in the background.

#### Request Parameters:

- **messages** (Required): List of messages to generate completion for.
- **model** (Required): The model to use for completion.
- **max_tokens** (Required): Maximum number of tokens to generate.
- **temperature** (Optional, default: `0.7`): Temperature for sampling.
- **num_context** (Optional, default: `2048`): Number of tokens to use as context.
- **output_format** (Optional, default: `default`): Output format for completion.

#### Example Request:

```json
{
    "messages": [{"role": "user", "content": "How does quantum computing work?"}],
    "model": "llama3.1",
    "max_tokens": 100,
    "temperature": 0.7
}
```

#### Success Response:

```json
{
    "success": true,
    "task_id": "your-task-id",
    "message": "Request queued successfully"
}
```

#### Error Response:

```json
{
    "success": false,
    "message": "Invalid request"
}
```

### 3. `GET /api/v1/qcompletions/<task_id>`

This endpoint checks the status of a queued task. The status can be `queued`, `processing`, `completed`, or `failed`. If the task has completed, the result is included in the response.

#### Example Request:

```bash
GET https://llmendpoint.com/api/v1/qcompletions/your-task-id
```

#### Example Success Response:

```json
{
    "success": true,
    "status": "completed",
    "result": "Quantum computing uses quantum-mechanical phenomena like superposition..."
}
```

#### Example Error Response:

```json
{
    "success": false,
    "message": "Task not found"
}
```

---

## Cost Calculation

Each model has a specific rate for input and output tokens. The cost is calculated as follows:

### Model Rates

Below are the rates for each available model:

| Model Name        | Input Rate | Output Rate |
|-------------------|------------|-------------|
| llama3.1          | 0.01       | 0.02        |
| llama3            | 0.015      | 0.025       |
| llama2            | 0.02       | 0.03        |
| mistral           | 0.012      | 0.022       |
| qwen              | 0.018      | 0.028       |
| gemma2            | 0.016      | 0.026       |
| llama3.2          | 0.014      | 0.024       |
| qwen2             | 0.017      | 0.027       |
| zephyr            | 0.019      | 0.029       |
| gemma             | 0.013      | 0.023       |
| llava             | 0.015      | 0.025       |
| mistral-nemo      | 0.011      | 0.021       |
| phi3              | 0.02       | 0.03        |
| wizardlm2         | 0.018      | 0.028       |
| orca-mini         | 0.019      | 0.029       |
| codellama         | 0.017      | 0.027       |
| llama2-uncensored | 0.015      | 0.025       |
| owl_t-lite        | 0.014      | 0.024       |

The cost calculation for each request is determined by the **Input Rate** and **Output Rate** for the selected model.

- **Input Tokens**: Sum of characters in `messages` from the user.
- **Output Tokens**: Equal to `max_tokens`.
- **Credits Needed**: The total cost (in cents) divided by `0.0001`.

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
- For asynchronous task handling, use `/api/v1/qcompletions` to queue tasks and `/api/v1/qcompletions/<task_id>` to check their status.

---

Thank you for using LlmEndpoint!
