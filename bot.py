import discord
import aiohttp
import os

# Lấy token từ biến môi trường
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN environment variable is not set!")

# Khởi tạo intents với quyền đọc nội dung tin nhắn và file đính kèm
intents = discord.Intents.default()
intents.message_content = True  # Phải bật cái này trong Developer Portal

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'✅ Bot đã đăng nhập thành công với tên: {client.user}')

@client.event
async def on_message(message):
    # Không phản hồi chính nó
    if message.author == client.user:
        return

    # Trả lời với lệnh đơn giản
    if message.content.lower() == 'ping':
        await message.channel.send('🏓 Pong!')
    elif message.content.lower() == 'hello':
        await message.channel.send('👋 Xin chào bạn! Tôi là bot Python.')

    # Kiểm tra nếu có file đính kèm
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.txt'):
                await message.channel.send(f"📎 Đang tải file `{attachment.filename}`...")

                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                content = await resp.text()
                                if len(content) <= 1900:
                                    await message.channel.send(f"📄 Nội dung file:\n```{content}```")
                                else:
                                    await message.channel.send("⚠️ Nội dung file quá dài, chỉ in 200 ký tự đầu:\n```" + content[:200] + " ...```")
                            else:
                                await message.channel.send("❌ Không thể tải file.")
                except Exception as e:
                    await message.channel.send(f"❌ Lỗi khi xử lý file: {e}")

# Chạy bot
client.run(DISCORD_TOKEN)
