import discord
from discord.ext import commands
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import requests
from io import BytesIO


class ExtractNumbersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='extract_numbers')
    async def extract_numbers(self, ctx):
        if ctx.message.attachments:
            try:
                # 画像を取得
                attachment = ctx.message.attachments[0]
                response = requests.get(attachment.url)
                img = Image.open(BytesIO(response.content))

                # 画像をグレースケールに変換
                gray_img = img.convert('L')

                # コントラストを強調
                enhancer = ImageEnhance.Contrast(gray_img)
                enhanced_img = enhancer.enhance(2)

                # 画像を二値化（白黒に変換）
                binary_img = enhanced_img.point(
                    lambda x: 0 if x < 200 else 255, '1')

                # OCRを使用して画像からテキストを抽出
                text = pytesseract.image_to_string(
                    binary_img, config='--psm 6 digits')

                # 数字を抽出
                numbers = ''.join(filter(str.isdigit, text))

                if numbers:
                    await ctx.send(f'抽出された数字: {numbers}')
                else:
                    await ctx.send('画像から数字を抽出できませんでした。')
            except Exception as e:
                await ctx.send(f'エラーが発生しました: {e}')
        else:
            await ctx.send('画像を添付してください。')


async def setup(bot):
    await bot.add_cog(ExtractNumbersCog(bot))
