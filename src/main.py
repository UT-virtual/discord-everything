# Standard Library
import logging
import os
import textwrap
from logging import getLogger
from pathlib import Path

# Third Party Library
import discord
from dotenv import load_dotenv

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(filename)s:%(lineno)d] - %(message)s",
    level=logging.WARNING,
)
logger = getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv(
    dotenv_path=Path(__file__).parents[1] / ".env",
    verbose=True,
    override=True,
)


def compose_embed(message: discord.Message):
    embed = discord.Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url, url=message.jump_url)
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon.url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(url=message.attachments[0].proxy_url)
    return embed


class MyClient(discord.Client):
    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        for guild in client.guilds:
            logger.info(textwrap.dedent(f"{guild.id=}, {guild.name=}"))
            for channel in guild.channels:
                logger.info(f"\t{type(channel).__name__}\t: {channel.id},\t{channel.name}")

        self.everything_channel_id: int = int(os.environ.get("EVERYTHING_CHANNEL_ID", None))
        logger.info(f"{type(self.everything_channel_id)=}")
        self.everything_channel = self.get_channel(self.everything_channel_id)

    async def on_message(self, message: discord.Message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        logger.info(f"{message.author.name} said: {message.content}")
        if message.content:
            if message.guild.id == self.everything_channel.guild.id:
                await self.everything_channel.send(embed=compose_embed(message))


if __name__ == "__main__":
    client = MyClient()
    client.run(os.environ.get("DISCORD_TOKEN", None))
