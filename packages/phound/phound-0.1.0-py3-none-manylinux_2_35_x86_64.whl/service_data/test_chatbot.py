import os
import time

from phound import Phound
from phound.handlers import BaseChatHandler


class ChatHandler(BaseChatHandler):
    def on_message(self, message):
        print(f"Got new message: {message}")
        self.show_typing()
        time.sleep(1)
        chat_history = self.get_history(depth=10)
        reply_items = [f"Initial message: {message.text}",
                       f"response: {message.text[::-1]}",
                       f"also got chat history with last {len(chat_history)} messages"]
        self.send_message(os.linesep.join(reply_items))


if __name__ == "__main__":
    with Phound() as phound:
        phound.register_chat_handler(ChatHandler)
        phound.start_listen_events()
