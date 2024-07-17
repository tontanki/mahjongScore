import os
from dotenv import load_dotenv
from bot import bot  # bot.pyからbotインスタンスをインポート
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

bot.run(TOKEN)
