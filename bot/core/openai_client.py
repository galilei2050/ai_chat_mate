from baski import clients

__all__ = ['OpenAiClient']


class OpenAiClient(clients.OpenAiClient):

    def __init__(self, telemetry=None):
        super().__init__(
            system_prompt=system_prompt_assistant, user_prompts=prompts,
            chunk_length=1024, telemetry=telemetry
        )

    def continue_chat(self, user_id, history, message, use_large=False):
        return self.from_prompt(user_id, 'continue_chat', history=history, message=message)


system_prompt_assistant = """
You are the helpful, creative, joyful, friendly, trustworthy assistant. 
You must be precise and specific in your answers. Avoid general thoughts and be concrete 
""".strip()


prompts = {
    "continue_chat": {
        "model": "gpt-4-turbo",
        "prompt": "{message}",
        "temperature": 1.1,
    },
}
