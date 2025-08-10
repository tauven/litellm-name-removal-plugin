# Remove Name Plugin for LiteLLM

This plugin is designed to remove the 'name' attribute from all messages before they are forwarded to LLM models. This addresses compatibility issues with various LLM providers that may not support or expect the 'name' field in the OpenAI chat format.

The plugin works by intercepting requests before they are sent to the LLM and removing the 'name' field from all messages, ensuring consistent message formatting across different LLM providers.

Based on https://docs.litellm.ai/docs/proxy/call_hooks#quick-start.

## Compatibility Issues Addressed

- OpenAI's optional 'name' field for messages
- LLM providers that don't support the 'name' field
- API error prevention when 'name' field is unexpected
- Privacy considerations for sensitive user information
- Workaround for [vllm/pull/20973](https://github.com/vllm-project/vllm/pull/20973) to handle unsupported 'name' field in tool calling.

## Installation

1. Place the `remove_name_plugin.py` file in the `litellm` directory of your project.
2. Ensure you have `litellm` installed.

## Usage

To use this plugin, you need to add it to your LiteLLM configuration file (e.g., `litellm/litellm_config.yaml`).

Here is an example of how to configure the plugin in your `litellm_config.yaml`:

```yaml
model_list:
  - model_name: chat
    litellm_params:
      # prefix with openai, hosted_vllm ...
      model: hosted_vllm/chat
      # Base URL of the LLM provider (e.g. OpenAI)
      base_url: http://host.docker.internal:8033/v1/
      api_key: "sk-none"
      cache: true

litellm_settings:
  # Filename of the plugin without .py and name of method.
  callbacks: ["remove_name_plugin.remove_name_handler_instance"]

logging:
  level: DEBUG
```

The plugin will automatically process all messages and remove the `name` field before forwarding them to the LLM.

## Docker Compose Usage

To use this plugin with Docker, you can leverage the provided `docker-compose.yml` configuration. This setup mounts both the plugin file and configuration file into the container.

Here's how to set it up:

1. Make sure your `docker-compose.yml` looks like this:
   ```yaml
   services:
     litellm:
       image: ghcr.io/berriai/litellm:main-stable
       ports:
         - "4000:4000"
       volumes:
         - ./litellm/litellm_config.yaml:/app/litellm_config.yaml
         - ./litellm/remove_name_plugin.py:/app/remove_name_plugin.py
       environment:
         - PYTHONPATH=/app
       working_dir: /app
       command: |
         --config /app/litellm_config.yaml --detailed_debug
       restart: unless-stopped
     vllm-chat:
       image: vllm/vllm-openai:latest
       runtime: nvidia
       ipc: host
       deploy:
         resources:
           reservations:
             devices:
               - driver: nvidia
                 count: 1
                 capabilities: [gpu]
       volumes:
         - .cache/huggingface:/root/.cache/huggingface
       environment:
         # ADD HF_TOKEN to your .env file.
         HUGGING_FACE_HUB_TOKEN: ${HF_TOKEN}
         VLLM_ATTENTION_BACKEND: FLASHINFER
         VLLM_USE_V1: 1
         VLLM_LOGGING_LEVEL: DEBUG

       command: --served-model-name chat --port 8033 --model Qwen/Qwen2-0.5B --max-num-seqs 4 --max-model-len 2048 --enable-prefix-caching
       ports:
         - "8033:8033"
   ```

2. The plugin will be automatically loaded and registered when LiteLLM starts up.

3. When running requests, the plugin will intercept all messages and remove any 'name' field before forwarding to LLM providers.

## Environment Variables

This project uses a `.env` file to manage environment variables. This file is not checked into version control, as specified in the `.gitignore` file.

To set up your local environment, create a `.env` file in the root of the project and add the necessary environment variables. For example:

```
HF_TOKEN="your-huggingface-token"