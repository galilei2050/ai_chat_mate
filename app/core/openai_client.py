from baski import clients

__all__ = ['OpenAiClient']


class OpenAiClient(clients.OpenAiClient):

    def __init__(self, api_key, telemetry):
        super().__init__(
            api_key=api_key, system_prompt=system_prompt_assistant, user_prompts=prompts,
            chunk_length=256, telemetry=telemetry
        )

    def continue_chat(self, user_id, history, message, use_large=False):
        if use_large:
            return self.from_prompt(user_id, 'continue_chat_16k', history=history, message=message)
        else:
            return self.from_prompt(user_id, 'continue_chat', history=history, message=message)


system_prompt_assistant = """
You are the helpful, creative, joyful, friendly, trustworthy assistant. 
You must be precise and specific in your answers. Avoid general thoughts and be concrete 
""".strip()


prompts = {
    "continue_chat": {
        "model": "gpt-3.5-turbo",
        "prompt": "{message}",
        "temperature": 1.1,
    },
    "continue_chat_16k": {
        "model": "gpt-3.5-turbo-16k",
        "prompt": "{message}",
        "temperature": 1.1,
    }
}
