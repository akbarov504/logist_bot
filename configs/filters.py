from models.language import Language
from states.state import get_state, get_data
from aiogram.dispatcher.filters import Filter
from aiogram.types import Message, CallbackQuery

class CheckState(Filter):
    def __init__(self, state: str) -> None:
        super().__init__()
        self.state = state
    
    async def check(self, message: Message) -> bool:
        state = get_state(message.chat.id)
        if self.state == state:
            return True
        return False
    
class CheckStateList(Filter):
    def __init__(self, states: list) -> None:
        super().__init__()
        self.states = states
    
    async def check(self, message: Message) -> bool:
        state = get_state(message.chat.id)
        for s in self.states:
            if s == state:
                return True
        return False
    
class CheckStateWithCall(Filter):
    def __init__(self, state: str) -> None:
        super().__init__()
        self.state = state
    
    async def check(self, call: CallbackQuery) -> bool:
        state = get_state(call.message.chat.id)
        if self.state == state:
            return True
        return False

class CheckWord(Filter):
    def __init__(self, code: str) -> None:
        super().__init__()
        self.code = code
    
    async def check(self, msg: Message) -> bool:
        data = get_data(msg.chat.id)
        lang = data.get("LANG")
        text = Language.get(lang, self.code)
        if msg.text == text:
            return True
        return False
    
class CheckWordList(Filter):
    def __init__(self, codes: list) -> None:
        super().__init__()
        self.codes = codes
    
    async def check(self, msg: Message) -> bool:
        data = get_data(msg.chat.id)
        lang = data.get("LANG")
        for code in self.codes:
            text = Language.get(lang, code)
            if msg.text == text:
                return True
        return False
