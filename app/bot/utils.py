from aiogram.fsm.state import State, StatesGroup
from tiktoken import encoding_for_model
from gpytranslate import Translator
import logging

class States(StatesGroup):
    ENTRY_STATE = State()
    CHATGPT_STATE = State()
    DALL_E_STATE = State()
    STABLE_STATE = State()
    INFO_STATE = State()
    PURCHASE_STATE = State()
    PURCHASE_CHATGPT_STATE = State()
    PURCHASE_DALL_E_STATE = State()
    PURCHASE_STABLE_STATE = State()

encoding = encoding_for_model("gpt-4o")

translator = Translator()

class TelegramError(Exception):
    def __init__(self, msg: str):
        self.msg=msg
    def output(self):
        logging.error("Telegram error:", self.msg)