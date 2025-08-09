# Test Remove Name Plugin

This file contains sample HTTP requests to test the remove name plugin functionality in LiteLLM.

## Request with name field (to be removed by plugin)

```
POST http://localhost:4000/chat/completions
Content-Type: application/json

{
  "model": "chat",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "name": "John Doe",
      "content": "Hello, how can you help me today?"
    }
  ]
}
```

## Expected behavior

When this request is sent to LiteLLM with the remove_name_plugin enabled:
1. The plugin's `pre_call_hook` will intercept the request
2. It will find the user message with role "user" that has a "name" field
3. It will remove the "name" field from that message
4. The modified request will be forwarded to the LLM model
5. The response should contain the conversation without the name field

## Testing in VS Code

To test this:
1. Save this content as `test_remove_name_plugin.http` in your project directory
2. Open it in Visual Studio Code
3. Use the "Send Request" option (usually available when you hover over the request)
4. Check that the plugin properly removes the name field from the user message before sending to the LLM

## Alternative test without name field

```
POST http://localhost:4000/chat/completions
Content-Type: application/json

{
  "model": "chat",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello, how can you help me today?"
    }
  ]
}