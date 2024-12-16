import pytest
from unittest.mock import AsyncMock, MagicMock, call, patch
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.bot.utils import encoding
from app.bot.handlers.answer_handlers import AnswerHandlers
from app.bot.utils import States
from app.services.db import DatabaseError

class TestChatGpt:
    @pytest.mark.asyncio
    async def test_chatgpt_answer_handler_success(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_chatgpt.return_value = 1

        mock_db.get_messages.return_value = [{"role": "user", "content": "question"}], 1

        mock_openai.get_chatgpt.return_value = 'answer'

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        await handlers.chatgpt_answer_handler(message, state)

        mock_db.get_chatgpt.assert_awaited_once_with(12345)

        mock_openai.get_chatgpt.assert_awaited_once_with([{"role": "user", "content": "question"}])

        mock_db.save_message.assert_has_calls([call(12345, "user", "question", len(encoding.encode("question"))), call(12345, "assistant", "answer", len(encoding.encode("answer")))])

        assert len(mock_db.save_message.mock_calls) == 2

        mock_db.get_messages.assert_awaited_once_with(12345)

        mock_db.set_chatgpt.assert_awaited_once_with(12345, 0)

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "answer",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.CHATGPT_STATE)

    @pytest.mark.asyncio
    async def test_chatgpt_safety_issue(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_chatgpt.return_value = 1

        mock_db.get_messages.return_value = [{"role": "user", "content": "question"}], 1

        mock_openai.get_chatgpt.return_value = ''

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        await handlers.chatgpt_answer_handler(message, state)

        mock_db.get_chatgpt.assert_awaited_once_with(12345)

        mock_openai.get_chatgpt.assert_awaited_once_with([{"role": "user", "content": "question"}])

        mock_db.save_message.assert_awaited_once_with(12345, "user", "question", len(encoding.encode("question")))

        mock_db.get_messages.assert_awaited_once_with(12345)

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.CHATGPT_STATE)

    @pytest.mark.asyncio
    async def test_chatgpt_zero_tokens(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_chatgpt.return_value = 0

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        await handlers.chatgpt_answer_handler(message, state)

        mock_db.get_chatgpt.assert_awaited_once_with(12345)

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "❎You have 0 ChatGPT tokens. You need to buy them to use ChatGPT.",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.CHATGPT_STATE)

    @pytest.mark.asyncio
    async def test_chatgpt_database_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_chatgpt.side_effect = DatabaseError()

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        with pytest.raises(DatabaseError):
            await handlers.chatgpt_answer_handler(message, state)

        mock_db.get_chatgpt.assert_awaited_once_with(12345)

    @pytest.mark.asyncio
    async def test_chatgpt_answer_handler_telegram_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_chatgpt.return_value = 1

        mock_db.get_messages.return_value = [{"role": "user", "content": "question"}], 1

        mock_openai.get_chatgpt.return_value = 'answer'

        message.answer.side_effect = Exception()

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        with pytest.raises(Exception):
            await handlers.chatgpt_answer_handler(message, state)

        mock_db.get_chatgpt.assert_awaited_once_with(12345)

        mock_openai.get_chatgpt.assert_awaited_once_with([{"role": "user", "content": "question"}])

        mock_db.save_message.assert_has_calls([call(12345, "user", "question", len(encoding.encode("question"))), call(12345, "assistant", "answer", len(encoding.encode("answer")))])

        assert len(mock_db.save_message.mock_calls) == 2

        mock_db.get_messages.assert_awaited_once_with(12345)

        mock_db.set_chatgpt.assert_awaited_once_with(12345, 0)

class TestDallE:
    @patch('app.bot.handlers.answer_handlers.translator.translate', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_dall_e_answer_handler_success(self, mock_translate):
        message = AsyncMock(spec=types.Message)
        message.answer_photo = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_dalle.return_value = 1

        mock_translate.return_value = MagicMock(text="question")

        mock_openai.get_dalle.return_value = 'answer'

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        await handlers.dall_e_answer_handler(message, state)

        mock_db.get_dalle.assert_awaited_once_with(12345)

        mock_openai.get_dalle.assert_awaited_once_with("question")

        mock_db.set_dalle.assert_awaited_once_with(12345, 0)

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer_photo.assert_awaited_once_with(
            photo="answer",
            reply_markup = reply_markup,
            caption="question",
        )
        state.set_state.assert_awaited_once_with(States.DALL_E_STATE)

        mock_translate.assert_awaited_once_with("question", targetlang='en')

    @patch('app.bot.handlers.answer_handlers.translator.translate', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_dall_e_safety_issue(self, mock_translate):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_dalle.return_value = 1

        mock_translate.return_value = MagicMock(text="question")

        mock_openai.get_dalle.return_value = ''

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        await handlers.dall_e_answer_handler(message, state)

        mock_db.get_dalle.assert_awaited_once_with(12345)

        mock_openai.get_dalle.assert_awaited_once_with("question")

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.DALL_E_STATE)
        mock_translate.assert_awaited_once_with("question", targetlang='en')

    @pytest.mark.asyncio
    async def test_dall_e_zero_tokens(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_dalle.return_value = 0

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        await handlers.dall_e_answer_handler(message, state)

        mock_db.get_dalle.assert_awaited_once_with(12345)

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "❎You have 0 DALL·E image generations. You need to buy them to use DALL·E.",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.DALL_E_STATE)

    @pytest.mark.asyncio
    async def test_dall_e_database_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_dalle.side_effect = DatabaseError()

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        with pytest.raises(DatabaseError):
            await handlers.dall_e_answer_handler(message, state)

        mock_db.get_dalle.assert_awaited_once_with(12345)

    @patch('app.bot.handlers.answer_handlers.translator.translate', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_dall_e_answer_handler_telegram_error(self, mock_translate):
        message = AsyncMock(spec=types.Message)
        message.answer_photo = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_openai = AsyncMock()

        mock_db.get_dalle.return_value = 1

        mock_translate.return_value = MagicMock(text="question")

        mock_openai.get_dalle.return_value = 'answer'

        message.answer_photo.side_effect = Exception()

        handlers = AnswerHandlers(mock_db, mock_openai, AsyncMock())

        with pytest.raises(Exception):
            await handlers.dall_e_answer_handler(message, state)

        mock_db.get_dalle.assert_awaited_once_with(12345)

        mock_openai.get_dalle.assert_awaited_once_with("question")

        mock_db.set_dalle.assert_awaited_once_with(12345, 0)

class TestStable:
    @patch('app.bot.handlers.answer_handlers.translator.translate', new_callable=AsyncMock)
    @patch('app.bot.handlers.answer_handlers.BufferedInputFile')
    @pytest.mark.asyncio
    async def test_stable_answer_handler_success(self, mock_buffer, mock_translate):
        message = AsyncMock(spec=types.Message)
        message.answer_photo = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_stable = AsyncMock()

        mock_db.get_stable.return_value = 1

        mock_translate.return_value = MagicMock(text="question")

        mock_stable.get_stable.return_value = 'answer'

        mock_buffer.return_value = "answer"

        handlers = AnswerHandlers(mock_db, AsyncMock(), mock_stable)

        await handlers.stable_answer_handler(message, state)

        mock_db.get_stable.assert_awaited_once_with(12345)

        mock_stable.get_stable.assert_awaited_once_with("question")

        mock_db.set_stable.assert_awaited_once_with(12345, 0)

        mock_buffer.assert_called_once_with("answer", 'image.jpeg')

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer_photo.assert_awaited_once_with(
            photo="answer",
            reply_markup = reply_markup,
            caption="question",
        )
        state.set_state.assert_awaited_once_with(States.STABLE_STATE)

        mock_translate.assert_awaited_once_with("question", targetlang='en')

    @patch('app.bot.handlers.answer_handlers.translator.translate', new_callable=AsyncMock)
    @pytest.mark.asyncio
    async def test_stable_safety_issue(self, mock_translate):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_stable = AsyncMock()

        mock_db.get_stable.return_value = 1

        mock_translate.return_value = MagicMock(text="question")

        mock_stable.get_stable.return_value = ''

        handlers = AnswerHandlers(mock_db, AsyncMock(), mock_stable)

        await handlers.stable_answer_handler(message, state)

        mock_db.get_stable.assert_awaited_once_with(12345)

        mock_stable.get_stable.assert_awaited_once_with("question")

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "❌Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again.",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.STABLE_STATE)
        mock_translate.assert_awaited_once_with("question", targetlang='en')

    @pytest.mark.asyncio
    async def test_stable_zero_tokens(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_stable = AsyncMock()

        mock_db.get_stable.return_value = 0

        handlers = AnswerHandlers(mock_db, AsyncMock(), mock_stable)

        await handlers.stable_answer_handler(message, state)

        mock_db.get_stable.assert_awaited_once_with(12345)

        button = [[KeyboardButton(text="🔙Back")]]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=button, resize_keyboard=True
        )
        message.answer.assert_awaited_once_with(
            text = "❎You have 0 Stable Diffusion image generations. You need to buy them to use Stable Diffusion.",
            reply_markup = reply_markup,
        )
        state.set_state.assert_awaited_once_with(States.STABLE_STATE)

    @pytest.mark.asyncio
    async def test_stable_database_error(self):
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_stable = AsyncMock()

        mock_db.get_stable.side_effect = DatabaseError()

        handlers = AnswerHandlers(mock_db, AsyncMock(), mock_stable)

        with pytest.raises(DatabaseError):
            await handlers.stable_answer_handler(message, state)

        mock_db.get_stable.assert_awaited_once_with(12345)

    @patch('app.bot.handlers.answer_handlers.translator.translate', new_callable=AsyncMock)
    @patch('app.bot.handlers.answer_handlers.BufferedInputFile')
    @pytest.mark.asyncio
    async def test_stable_answer_handler_telegram_error(self, mock_buffer, mock_translate):
        message = AsyncMock(spec=types.Message)
        message.answer_photo = AsyncMock()
        message.from_user = MagicMock(id=12345)
        message.text = "question"

        state = AsyncMock(spec=FSMContext)
        state.set_state = AsyncMock()

        mock_db = AsyncMock()
        mock_stable = AsyncMock()

        mock_db.get_stable.return_value = 1

        mock_translate.return_value = MagicMock(text="question")

        mock_stable.get_stable.return_value = 'answer'

        mock_buffer.return_value = "answer"

        message.answer_photo.side_effect = Exception()

        handlers = AnswerHandlers(mock_db, AsyncMock(), mock_stable)

        with pytest.raises(Exception):
            await handlers.stable_answer_handler(message, state)

        mock_db.get_stable.assert_awaited_once_with(12345)

        mock_stable.get_stable.assert_awaited_once_with("question")

        mock_db.set_stable.assert_awaited_once_with(12345, 0)

        mock_buffer.assert_called_once_with("answer", 'image.jpeg')