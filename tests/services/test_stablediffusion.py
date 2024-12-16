import pytest
from unittest.mock import MagicMock, patch

from app.services.stablediffusion import StableDiffusion

@patch('requests.post')
@pytest.mark.asyncio
async def test_get_stable_success(mock_postrequest):
    stable = StableDiffusion('key')

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"answer"

    mock_postrequest.return_value = mock_response

    answer = await stable.get_stable('question')

    mock_postrequest.assert_called_once_with(f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer key",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": "question",
            "output_format": "jpeg",
            "model": "sd3-large-turbo",
        }
    )

    assert answer == b"answer"

@patch('requests.post')
@pytest.mark.asyncio
async def test_get_stable_response_error(mock_postrequest):
    stable = StableDiffusion('key')

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.content = b"answer"

    mock_postrequest.return_value = mock_response

    answer = await stable.get_stable('question')

    mock_postrequest.assert_called_once_with(f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer key",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": "question",
            "output_format": "jpeg",
            "model": "sd3-large-turbo",
        }
    )

    assert answer == None

@patch('requests.post')
@pytest.mark.asyncio
async def test_get_stable_error(mock_postrequest):
    stable = StableDiffusion('key')

    mock_postrequest.side_effect = Exception()

    answer = await stable.get_stable('question')

    mock_postrequest.assert_called_once_with(f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
        headers={
            "authorization": f"Bearer key",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": "question",
            "output_format": "jpeg",
            "model": "sd3-large-turbo",
        }
    )

    assert answer == None