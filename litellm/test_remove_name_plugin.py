import unittest
import asyncio
from litellm.remove_name_plugin import RemoveNamePlugin

class TestRemoveNamePlugin(unittest.TestCase):

    def setUp(self):
        self.plugin = RemoveNamePlugin()

    def test_remove_name_from_messages(self):
        data = {
            "messages": [
                {"role": "user", "content": "Hello", "name": "John"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "How are you?", "name": "Jane"}
            ]
        }
        result = asyncio.run(self.plugin.async_pre_call_hook(None, None, data, "completion"))
        for message in result["messages"]:
            self.assertNotIn("name", message)

    def test_no_name_in_messages(self):
        data = {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"}
            ]
        }
        original_data = data.copy()
        result = asyncio.run(self.plugin.async_pre_call_hook(None, None, data, "completion"))
        self.assertEqual(result, original_data)

    def test_mixed_messages(self):
        data = {
            "messages": [
                {"role": "user", "content": "Hello", "name": "John"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "How are you?"}
            ]
        }
        result = asyncio.run(self.plugin.async_pre_call_hook(None, None, data, "completion"))
        for message in result["messages"]:
            self.assertNotIn("name", message)

    def test_empty_message_list(self):
        data = {"messages": []}
        original_data = data.copy()
        result = asyncio.run(self.plugin.async_pre_call_hook(None, None, data, "completion"))
        self.assertEqual(result, original_data)

    def test_invalid_message_data(self):
        data = {"messages": "not a list"}
        original_data = data.copy()
        result = asyncio.run(self.plugin.async_pre_call_hook(None, None, data, "completion"))
        self.assertEqual(result, original_data)

if __name__ == '__main__':
    unittest.main()