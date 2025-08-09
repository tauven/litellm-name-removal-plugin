# Remove Name Plugin for LiteLLM

This plugin is designed to remove the 'name' attribute from all user messages before they are forwarded to LLM models. This addresses compatibility issues with various LLM providers that may not support or expect the 'name' field in the OpenAI chat format.

The plugin works by intercepting requests before they are sent to the LLM and removing the 'name' field from user messages, ensuring consistent message formatting across different LLM providers.

## Compatibility Issues Addressed

- OpenAI's optional 'name' field for user messages
- LLM providers that don't support the 'name' field
- API error prevention when 'name' field is unexpected
- Privacy considerations for sensitive user information

## Installation

1. Place the `remove_name_plugin.py` file in your LiteLLM project directory.
   - For local development: directly in your project directory
   - For Docker deployment: place it under `/app/litellm/` (as shown in the docker-compose.yml)
2. Ensure you have `litellm` installed.

## Usage

To use this plugin, you need to add it to your LiteLLM configuration file (e.g., `litellm_config.yaml`).

Here is an example of how to configure the plugin in your `litellm_config.yaml`:

```yaml
model_list:
  - model_name: chat
    litellm_params:
      model: openai/chat
      base_url: http://host.docker.internal:8033/v1/
      api_key: "sk-none"
      cache: true

litellm_settings:
  callbacks: ["litellm.remove_name_plugin.remove_name_handler_instance"]

logging:
  level: DEBUG
```

The plugin will automatically process all user messages and remove the `name` field before forwarding them to the LLM.

## Docker Compose Usage

To use this plugin with Docker, you can leverage the provided `docker-compose.yml` configuration. This setup mounts both the plugin file and configuration file into the container.

Here's how to set it up:

1. Make sure your `docker-compose.yml` includes:
   ```yaml
   services:
     litellm:
       image: ghcr.io/berriai/litellm:main-stable
       container_name: litellm
       ports:
         - "4000:4000"
       volumes:
         - ./litellm_config.yaml:/app/litellm_config.yaml
         - ./remove_name_plugin.py:/app/litellm/remove_name_plugin.py
       environment:
         - PYTHONPATH=/app
       working_dir: /app
       command: |
         --config /app/litellm_config.yaml --detailed_debug
       restart: unless-stopped
   ```

2. The plugin will be automatically loaded and registered when LiteLLM starts up.

3. When running requests, the plugin will intercept user messages and remove any 'name' field before forwarding to LLM providers.