import pytest
from unittest.mock import AsyncMock, MagicMock

from app.services.openaitools import OpenAiTools

class Response:
    def __init__(self, content: str):
        self.choices = [Message(content)]
        self.data = [Message(content)]

class Message:
    def __init__(self, content: str):
        self.message = Content(content)
        self.url = content

class Content:
    def __init__(self, content: str):
        self.content = content

class TestGetChatgpt:
    @pytest.mark.asyncio
    async def test_get_chatgpt_success(self):
        openai = OpenAiTools('token')
        openai.client = MagicMock()
        openai.client.chat = MagicMock()
        openai.client.chat.completions = MagicMock()
        openai.client.chat.completions.create = AsyncMock()
        openai.client.chat.completions.create.return_value = Response('answer')

        answer = await openai.get_chatgpt([])

        openai.client.chat.completions.create.assert_awaited_once_with(
            messages=[],
            model="gpt-4o",
            max_tokens=16384,
            temperature=1,
        )

        assert answer == 'answer'

    @pytest.mark.asyncio
    async def test_get_chatgpt_error(self):
        openai = OpenAiTools('token')
        openai.client = MagicMock()
        openai.client.chat = MagicMock()
        openai.client.chat.completions = MagicMock()
        openai.client.chat.completions.create = AsyncMock()
        openai.client.chat.completions.create.side_effect = Exception()

        answer = await openai.get_chatgpt([])

        openai.client.chat.completions.create.assert_awaited_once_with(
            messages=[],
            model="gpt-4o",
            max_tokens=16384,
            temperature=1,
        )

        assert answer == None

class TestGetDallE:
    @pytest.mark.asyncio
    async def test_get_dalle_success(self):
        openai = OpenAiTools('token')
        openai.client = MagicMock()
        openai.client.images = MagicMock()
        openai.client.images.generate = AsyncMock()
        openai.client.images.generate.return_value = Response('answer')

        answer = await openai.get_dalle('question')

        openai.client.images.generate.assert_awaited_once_with(
            model="dall-e-3",
            prompt='question',
            size="1024x1024",
            n=1,
        )

        assert answer == 'answer'

    @pytest.mark.asyncio
    async def test_get_dalle_error(self):
        openai = OpenAiTools('token')
        openai.client = MagicMock()
        openai.client.images = MagicMock()
        openai.client.images.generate = AsyncMock()
        openai.client.images.generate.side_effect = Exception()

        answer = await openai.get_dalle('question')

        openai.client.images.generate.assert_awaited_once_with(
            model="dall-e-3",
            prompt='question',
            size="1024x1024",
            n=1,
        )

        assert answer == None