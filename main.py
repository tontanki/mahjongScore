import os
import asyncio
from dotenv import load_dotenv
from bot import bot
from keep import keep_alive

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数からトークンを取得
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# 環境変数から開発モードフラグを取得
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'False') == 'True'

if not DEVELOPMENT_MODE:
    # 本番モードの場合、Webサーバーを起動してBotを常時稼働させる
    keep_alive()

# Cogをロードする非同期関数


async def load_extensions():
    initial_extensions = ['cogs.score', 'cogs.ranking', 'cogs.register']
    for extension in initial_extensions:
        await bot.load_extension(extension)

if __name__ == '__main__':
    # 非同期関数を実行してCogをロードする
    asyncio.run(load_extensions())
    bot.run(TOKEN)
