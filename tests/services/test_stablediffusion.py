import pytest
from unittest.mock import MagicMock, AsyncMock, patch, call, ANY

from app.services.stablediffusion import StableDiffusion

class AsyncContextManager:
    def __init__(self):
        self.post = MagicMock()
        self.read = AsyncMock()

    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, traceback):
        pass

@patch('app.services.stablediffusion.aiohttp')
@pytest.mark.asyncio
async def test_get_stable_success(mock_aiohttp):
    stable = StableDiffusion('key')

    session = AsyncContextManager()

    response = AsyncContextManager()

    session.post.return_value = response

    mock_aiohttp.ClientSession.return_value = session

    response.status = 200

    response.read.return_value = b"answer"

    mock_aiohttp.FormData = MagicMock()

    answer = await stable.get_stable('question')

    response.read.assert_awaited_once_with()

    mock_aiohttp.FormData.assert_has_calls([call(),
                                            call().add_field("prompt", 'question', content_type='multipart/form-data'),
                                            call().add_field("output_format", "jpeg", content_type='multipart/form-data'),
                                            call().add_field("model", "sd3-large-turbo", content_type='multipart/form-data')])

    assert len(mock_aiohttp.FormData.mock_calls) == 4

    session.post.assert_called_once_with('https://api.stability.ai/v2beta/stable-image/generate/sd3',
                                        headers={
                                            "authorization": f"Bearer key",
                                            "accept": "image/*"
                                        },
                                        data=ANY)

    assert answer == b"answer"

@patch('app.services.stablediffusion.aiohttp')
@pytest.mark.asyncio
async def test_get_stable_error(mock_aiohttp):
    stable = StableDiffusion('key')

    session = AsyncContextManager()

    response = AsyncContextManager()

    session.post.return_value = response

    mock_aiohttp.ClientSession.return_value = session

    response.status = 500

    response.read.return_value = b"answer"

    mock_aiohttp.FormData = MagicMock()

    answer = await stable.get_stable('question')

    mock_aiohttp.FormData.assert_has_calls([call(),
                                            call().add_field("prompt", 'question', content_type='multipart/form-data'),
                                            call().add_field("output_format", "jpeg", content_type='multipart/form-data'),
                                            call().add_field("model", "sd3-large-turbo", content_type='multipart/form-data')])

    assert len(mock_aiohttp.FormData.mock_calls) == 4

    session.post.assert_called_once_with('https://api.stability.ai/v2beta/stable-image/generate/sd3',
                                        headers={
                                            "authorization": f"Bearer key",
                                            "accept": "image/*"
                                        },
                                        data=ANY)

    assert answer == None

@patch('app.services.stablediffusion.aiohttp')
@pytest.mark.asyncio
async def test_get_stable_exception(mock_aiohttp):
    stable = StableDiffusion('key')

    mock_aiohttp.ClientSession.side_effect = Exception()

    mock_aiohttp.FormData = MagicMock()

    answer = await stable.get_stable('question')

    mock_aiohttp.FormData.assert_has_calls([call(),
                                            call().add_field("prompt", 'question', content_type='multipart/form-data'),
                                            call().add_field("output_format", "jpeg", content_type='multipart/form-data'),
                                            call().add_field("model", "sd3-large-turbo", content_type='multipart/form-data')])

    assert len(mock_aiohttp.FormData.mock_calls) == 4

    assert answer == None