import logging
import sys

from telethon import TelegramClient

from tgcf.config import CONFIG, get_SESSION
from tgcf.plugins import TgcfMessage, TgcfPlugin


class TgcfSender(TgcfPlugin):
    id_ = "sender"

    async def __ainit__(self) -> None:
        sender = TelegramClient(
            get_SESSION(CONFIG.plugin_cfgs.sender, "tgcf_sender"),
            CONFIG.login_cfg.API_ID,
            CONFIG.login_cfg.API_HASH,
        )
        if self.data.user_type == 0:
            if self.data.BOT_TOKEN == "":
                logging.warning(
                    "[Sender] Bot token not found, but login type is set to bot."
                )
                sys.exit()
            await sender.start(bot_token=self.data.BOT_TOKEN)
        else:
            await sender.start()
        self.sender = sender

    async def modify(self, tm: TgcfMessage) -> TgcfMessage:
        tm.client = self.sender
        if tm.file_type != "nofile":
            tm.new_file = await tm.get_file()
            tm.cleanup = True
        return tm
