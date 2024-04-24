from src.chat_bot_sea.request_functions.read_news.rag_web_vi import rag_news
from src.chat_bot_sea.request_functions.read_news.news import get_news
from .function_interactive import BotFunction

import sys
from loguru import logger
logger.remove()
logger.add(sys.stdout, colorize=True, format='<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}:{function}</cyan> | <level>{message}</level>')


class UserFunction:
    def __init__(self, group_id: str):
        self.group_id = group_id

    def message_template(self, content: str = ''):
        return {
            'group_id': self.group_id,
            'message': {
                'tag': 'text',
                'text': {
                    'format': 1,  # markdown
                    'content': content,
                },
            }
        }

    def rag_news(self):
        text = rag_news()
        content = f"{text['text']}"[:2000]
        r = BotFunction(self.group_id).post(self.message_template(content))
        logger.info(f'{r.content}')

    def search_news(self):
        lst = get_news(url='https://vnexpress.net/')
        for text in lst:
            content = f"{text}"
            r = BotFunction(self.group_id).post(self.message_template(content))
        logger.info(f'{r.content}')
